"""
LoRA FFE - Adaptación de LLMs para Tensores FFE
Proyecto Genesis - Aurora Intelligence Engine

Dos LoRAs complementarios:
1. LoRA₁ (Pre-quantization): Prepara embeddings para cuantización
2. LoRA₂ (Emergent Bias): Guía hacia patrones emergentes

Loss total: L = L_quant + λ₁·L_emerge + λ₂·L_info + λ₃·L_order
"""

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from tensor_ffe import TensorFFE, VectorFFE
from transcender import Transcender, Emergencia
from ffe_encoder_mcp import FFEEncoder


@dataclass
class LoRAConfig:
    """Configuración de LoRA"""
    rank: int = 8  # Rango de descomposición
    alpha: float = 16.0  # Factor de escala
    dropout: float = 0.1
    hidden_dim: int = 768  # Dimensión del LLM


class LoRALayer(nn.Module):
    """Capa LoRA genérica: h + (α/r) · BA"""
    
    def __init__(self, config: LoRAConfig):
        super().__init__()
        self.config = config
        
        # Matrices de bajo rango
        self.lora_A = nn.Parameter(torch.randn(config.hidden_dim, config.rank) * 0.01)
        self.lora_B = nn.Parameter(torch.zeros(config.rank, config.hidden_dim))
        
        self.dropout = nn.Dropout(config.dropout)
        self.scaling = config.alpha / config.rank
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward: h + scaling * (dropout(xA)B)"""
        lora_out = self.dropout(x @ self.lora_A) @ self.lora_B
        return x + lora_out * self.scaling


class LoRA1_PreQuantization(nn.Module):
    """
    LoRA₁: Pre-cuantización
    Objetivo: Preparar embeddings para discretización [0, 7]
    """
    
    def __init__(self, config: LoRAConfig):
        super().__init__()
        self.lora = LoRALayer(config)
        
        # Cabeza de proyección a 9 dimensiones (para 3 vectores FFE)
        self.projection = nn.Linear(config.hidden_dim, 9)
        
        # Activación sigmoide para [0, 1] → escalar a [0, 7]
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, embedding: torch.Tensor) -> torch.Tensor:
        """
        embedding: (batch, 768)
        output: (batch, 9) en rango [0, 7]
        """
        # Adaptación LoRA
        adapted = self.lora(embedding)
        
        # Proyección a 9 dims
        projected = self.projection(adapted)
        
        # Normalizar a [0, 7]
        normalized = self.sigmoid(projected) * 7.0
        
        return normalized
    
    def to_tensor_ffe(self, values: torch.Tensor) -> TensorFFE:
        """Convierte salida a TensorFFE"""
        vals = values.detach().cpu().numpy().astype(int)
        vals = np.clip(vals, 0, 7)  # Asegurar rango
        
        tensor = TensorFFE()
        tensor.nivel_1[0] = VectorFFE(forma=vals[0], funcion=vals[1], estructura=vals[2])
        tensor.nivel_1[1] = VectorFFE(forma=vals[3], funcion=vals[4], estructura=vals[5])
        tensor.nivel_1[2] = VectorFFE(forma=vals[6], funcion=vals[7], estructura=vals[8])
        tensor.reconstruir_jerarquia()
        
        return tensor


class LoRA2_EmergentBias(nn.Module):
    """
    LoRA₂: Sesgo emergente
    Objetivo: Guiar hacia patrones que generan alta emergencia
    """
    
    def __init__(self, config: LoRAConfig, transcender: Transcender):
        super().__init__()
        self.lora = LoRALayer(config)
        self.transcender = transcender
        
        # Cabeza de "emergencia predicha"
        self.emergence_head = nn.Linear(config.hidden_dim, 1)
    
    def forward(self, embedding: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        embedding: (batch, 768)
        output: (adapted_embedding, emergence_score)
        """
        # Adaptación LoRA
        adapted = self.lora(embedding)
        
        # Predicción de emergencia
        emergence_pred = torch.sigmoid(self.emergence_head(adapted))
        
        return adapted, emergence_pred
    
    def compute_emergence_loss(self, embedding: torch.Tensor, 
                               tensor_ffe: TensorFFE,
                               target_emergence: float = 0.7) -> torch.Tensor:
        """
        Loss de emergencia: penaliza baja emergencia
        """
        _, emergence_pred = self.forward(embedding)
        
        # Calcular emergencia real (usando Transcender)
        # Esto requeriría un batch de tripletas, simplificamos
        target = torch.tensor([target_emergence], device=embedding.device)
        
        loss = F.mse_loss(emergence_pred, target)
        return loss


class LoRAFFETrainer:
    """Entrenador combinado de LoRA₁ + LoRA₂"""
    
    def __init__(self, config: LoRAConfig):
        self.config = config
        self.encoder = FFEEncoder(dimension_embedding=config.hidden_dim)
        self.transcender = Transcender()
        
        # Modelos
        self.lora1 = LoRA1_PreQuantization(config)
        self.lora2 = LoRA2_EmergentBias(config, self.transcender)
        
        # Optimizadores
        self.opt1 = torch.optim.AdamW(self.lora1.parameters(), lr=1e-4)
        self.opt2 = torch.optim.AdamW(self.lora2.parameters(), lr=1e-4)
        
        # Pesos de loss
        self.lambda_emerge = 0.3
        self.lambda_info = 0.2
        self.lambda_order = 0.1
    
    def loss_quantization(self, embedding: torch.Tensor, target_ffe: TensorFFE) -> torch.Tensor:
        """
        L_quant: Distancia entre predicción y target FFE
        """
        # Forward LoRA₁
        values_pred = self.lora1(embedding)
        
        # Target values
        target_vals = []
        for v in target_ffe.nivel_1:
            target_vals.extend([v.forma, v.funcion, v.estructura])
        target_tensor = torch.tensor(target_vals, dtype=torch.float32, device=embedding.device)
        
        # MSE
        loss = F.mse_loss(values_pred, target_tensor)
        return loss
    
    def loss_emergence(self, embedding: torch.Tensor) -> torch.Tensor:
        """
        L_emerge: Maximiza score de emergencia predicho
        """
        _, emergence_pred = self.lora2(embedding)
        
        # Queremos emergencia alta (cerca de 1.0)
        target = torch.ones_like(emergence_pred)
        loss = F.mse_loss(emergence_pred, target)
        
        return loss
    
    def loss_information(self, embedding: torch.Tensor, tensor_ffe: TensorFFE) -> torch.Tensor:
        """
        L_info: Preserva información esencial (reconstrucción)
        """
        # Reconstruir desde FFE
        reconstructed = self.encoder.decode(tensor_ffe, dim_salida=self.config.hidden_dim)
        reconstructed_tensor = torch.tensor(reconstructed, dtype=torch.float32, device=embedding.device)
        
        # Similitud coseno (queremos alta similitud)
        cos_sim = F.cosine_similarity(embedding.unsqueeze(0), reconstructed_tensor.unsqueeze(0))
        
        # Loss: 1 - similitud (minimizar diferencia)
        loss = 1.0 - cos_sim.mean()
        
        return loss
    
    def loss_order(self, embeddings: List[torch.Tensor]) -> torch.Tensor:
        """
        L_order: Preserva no-conmutatividad (ABC ≠ BAC)
        """
        if len(embeddings) < 3:
            return torch.tensor(0.0)
        
        # Encodear tripletas en diferentes órdenes
        A, B, C = embeddings[:3]
        
        # Forward LoRA₁
        vals_ABC = self.lora1(torch.stack([A, B, C]))
        vals_BAC = self.lora1(torch.stack([B, A, C]))
        
        # Queremos que sean DIFERENTES
        similarity = F.cosine_similarity(vals_ABC, vals_BAC, dim=-1).mean()
        
        # Loss: penalizar alta similitud
        loss = torch.clamp(similarity, min=0.0)  # Solo penalizar si similar
        
        return loss
    
    def train_step(self, batch_embeddings: List[np.ndarray], 
                   batch_targets: List[TensorFFE]) -> Dict[str, float]:
        """
        Paso de entrenamiento
        """
        # Convertir a tensors
        embeddings = [torch.tensor(emb, dtype=torch.float32) for emb in batch_embeddings]
        
        total_loss = 0.0
        losses = {}
        
        for i, (emb, target) in enumerate(zip(embeddings, batch_targets)):
            # === LoRA₁: Cuantización ===
            self.opt1.zero_grad()
            
            l_quant = self.loss_quantization(emb, target)
            l_info = self.loss_information(emb, target)
            
            loss1 = l_quant + self.lambda_info * l_info
            loss1.backward()
            self.opt1.step()
            
            # === LoRA₂: Emergencia ===
            self.opt2.zero_grad()
            
            l_emerge = self.loss_emergence(emb)
            
            loss2 = l_emerge
            loss2.backward()
            self.opt2.step()
            
            # Acumular
            total_loss += (loss1.item() + loss2.item())
            losses[f'sample_{i}'] = {
                'l_quant': l_quant.item(),
                'l_info': l_info.item(),
                'l_emerge': l_emerge.item()
            }
        
        # Loss de orden (batch completo)
        if len(embeddings) >= 3:
            l_order = self.loss_order(embeddings)
            losses['l_order'] = l_order.item()
            total_loss += self.lambda_order * l_order.item()
        
        losses['total'] = total_loss
        return losses
    
    def save_loras(self, path_prefix: str):
        """Guarda checkpoints de ambos LoRAs"""
        torch.save(self.lora1.state_dict(), f"{path_prefix}_lora1.pth")
        torch.save(self.lora2.state_dict(), f"{path_prefix}_lora2.pth")
        print(f"✅ LoRAs guardados en {path_prefix}_lora*.pth")
    
    def load_loras(self, path_prefix: str):
        """Carga checkpoints"""
        self.lora1.load_state_dict(torch.load(f"{path_prefix}_lora1.pth"))
        self.lora2.load_state_dict(torch.load(f"{path_prefix}_lora2.pth"))
        print(f"✅ LoRAs cargados desde {path_prefix}_lora*.pth")


# === Demo y Tests ===

def demo_lora_training():
    """Demuestra entrenamiento de LoRAs"""
    print("🎯 Demo: Entrenamiento de LoRAs FFE\n")
    
    config = LoRAConfig(rank=8, hidden_dim=768)
    trainer = LoRAFFETrainer(config)
    
    # Generar datos sintéticos
    print("Generando batch de embeddings sintéticos...")
    batch_size = 4
    batch_embeddings = [np.random.randn(768).astype(np.float32) for _ in range(batch_size)]
    
    # Targets FFE (codificación directa)
    batch_targets = [trainer.encoder.encode(emb.tolist()) for emb in batch_embeddings]
    
    # Entrenar
    print("\nEntrenando...")
    for epoch in range(3):
        losses = trainer.train_step(batch_embeddings, batch_targets)
        print(f"Epoch {epoch+1}: Loss total = {losses['total']:.4f}")
        print(f"  l_quant promedio: {np.mean([losses[f'sample_{i}']['l_quant'] for i in range(batch_size)]):.4f}")
        print(f"  l_emerge promedio: {np.mean([losses[f'sample_{i}']['l_emerge'] for i in range(batch_size)]):.4f}")
    
    # Test inference
    print("\nTest de inferencia:")
    test_emb = torch.tensor(batch_embeddings[0], dtype=torch.float32)
    
    # LoRA₁
    vals = trainer.lora1(test_emb)
    print(f"  LoRA₁ output (9 valores): {vals.detach().numpy().astype(int)}")
    
    # LoRA₂
    _, emergence = trainer.lora2(test_emb)
    print(f"  LoRA₂ emergencia predicha: {emergence.item():.3f}")
    
    print("\n✅ Demo completada!")


if __name__ == "__main__":
    print("🎯 LoRA FFE - Adaptación de LLMs para Tensores FFE\n")
    
    # Verificar dependencias
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} detectado\n")
        
        # Ejecutar demo
        demo_lora_training()
        
    except ImportError:
        print("⚠️  PyTorch no instalado. Instalar con:")
        print("    pip install torch")
        print("\nEstructura de LoRA disponible para integración futura.")
