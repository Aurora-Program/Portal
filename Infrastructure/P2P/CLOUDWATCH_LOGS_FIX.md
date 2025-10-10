# 🔧 Fix: CloudWatch Logs Role Error

## Problema

```
Resource handler returned message: "CloudWatch Logs role ARN must be set 
in account settings to enable logging"
```

API Gateway requiere un rol de CloudWatch Logs configurado **a nivel de cuenta** para habilitar logging detallado.

## Soluciones

### Opción 1: Deshabilitar Logging ✅ (Ya aplicado)

**Cambio realizado:**
```yaml
ApiStage:
  Properties:
    TracingEnabled: false
    # Logging disabled
```

**Ventajas:**
- ✅ Funciona inmediatamente
- ✅ No requiere permisos adicionales
- ✅ Lambda logs siguen funcionando

**Desventajas:**
- ❌ No hay logs de API Gateway
- ❌ No puedes ver detalles de requests HTTP

### Opción 2: Configurar CloudWatch Logs Role (Recomendado para producción)

#### Paso 1: Crear rol de CloudWatch

```bash
# 1. Crear política de confianza
cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# 2. Crear rol
aws iam create-role \
  --role-name AmazonAPIGatewayPushToCloudWatchLogs \
  --assume-role-policy-document file://trust-policy.json

# 3. Adjuntar política
aws iam attach-role-policy \
  --role-name AmazonAPIGatewayPushToCloudWatchLogs \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs
```

#### Paso 2: Configurar en API Gateway

```bash
# Obtener el ARN del rol
ROLE_ARN=$(aws iam get-role \
  --role-name AmazonAPIGatewayPushToCloudWatchLogs \
  --query 'Role.Arn' \
  --output text)

# Configurar en API Gateway (a nivel de cuenta)
aws apigateway update-account \
  --patch-operations op=replace,path=/cloudwatchRoleArn,value=$ROLE_ARN
```

#### Paso 3: Actualizar CloudFormation

Una vez configurado el rol, puedes volver a habilitar logging:

```yaml
ApiStage:
  Type: AWS::ApiGateway::Stage
  Properties:
    StageName: !Ref Environment
    RestApiId: !Ref DiscoveryAPI
    DeploymentId: !Ref ApiDeployment
    TracingEnabled: true
    MethodSettings:
      - ResourcePath: '/*'
        HttpMethod: '*'
        LoggingLevel: INFO
        DataTraceEnabled: true
        MetricsEnabled: true
```

### Opción 3: CloudFormation con Rol Incluido

Si tienes permisos de IAM suficientes, puedes incluir el rol en el template:

```yaml
# Añadir al CloudFormation template

  ApiGatewayCloudWatchRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: apigateway.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs
  
  ApiGatewayAccount:
    Type: AWS::ApiGateway::Account
    Properties:
      CloudWatchRoleArn: !GetAtt ApiGatewayCloudWatchRole.Arn
```

## Deployment Actual

### Con PowerShell (sin script)

```powershell
# Configurar credenciales AWS
$env:AWS_ACCESS_KEY_ID = "tu-access-key"
$env:AWS_SECRET_ACCESS_KEY = "tu-secret-key"
$env:AWS_DEFAULT_REGION = "us-east-1"

# Desplegar stack
aws cloudformation create-stack `
  --stack-name aurora-discovery-dev `
  --template-body file://cloudformation.yaml `
  --capabilities CAPABILITY_NAMED_IAM `
  --region us-east-1
```

### Con deploy.ps1

```powershell
# Asegúrate de tener AWS CLI configurado
aws configure

# Ejecutar script de despliegue
.\deploy.ps1 -Environment dev -Region us-east-1
```

## Configurar AWS CLI

Si ves el error `InvalidClientTokenId`:

```powershell
# Opción 1: Configuración interactiva
aws configure

# Ingresar:
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: ...
# Default region: us-east-1
# Default output format: json

# Opción 2: Variables de entorno
$env:AWS_ACCESS_KEY_ID = "AKIA..."
$env:AWS_SECRET_ACCESS_KEY = "..."
$env:AWS_DEFAULT_REGION = "us-east-1"

# Verificar
aws sts get-caller-identity
```

## Verificar Deployment

```powershell
# Ver estado del stack
aws cloudformation describe-stacks `
  --stack-name aurora-discovery-dev `
  --query 'Stacks[0].StackStatus'

# Ver outputs
aws cloudformation describe-stacks `
  --stack-name aurora-discovery-dev `
  --query 'Stacks[0].Outputs'

# Ver logs de Lambda (todavía funcionan sin el rol de API Gateway)
aws logs tail /aws/lambda/aurora-discovery-dev --follow
```

## Qué funciona sin el Rol de CloudWatch

✅ **Funciona:**
- Lambda execution
- API Gateway routing
- DynamoDB operations
- Lambda CloudWatch logs
- API Gateway metrics (básicos)

❌ **No funciona:**
- API Gateway detailed logs
- Request/response logging
- Execution logs de API Gateway

## Recomendación

**Para desarrollo:** Usa Opción 1 (logging deshabilitado) ✅

**Para producción:** Configura el rol de CloudWatch (Opción 2)

## Troubleshooting

### Error: InvalidClientTokenId
```powershell
# Verificar credenciales
aws sts get-caller-identity

# Reconfigurar
aws configure
```

### Error: AccessDenied
```
# Tu usuario necesita estos permisos:
- cloudformation:*
- lambda:*
- apigateway:*
- dynamodb:*
- iam:CreateRole
- iam:AttachRolePolicy
- logs:CreateLogGroup
```

### Stack queda en ROLLBACK_COMPLETE
```powershell
# Eliminar y reintentar
aws cloudformation delete-stack --stack-name aurora-discovery-dev
aws cloudformation wait stack-delete-complete --stack-name aurora-discovery-dev

# Crear de nuevo
.\deploy.ps1
```

## Testing sin Deploy

Si no puedes desplegar a AWS ahora, puedes:

1. **Test local con Python:**
```python
# Simular Discovery Server localmente
python reputation_system.py  # ✅ Ya funciona
```

2. **Test con LocalStack (AWS local):**
```bash
# Instalar LocalStack
pip install localstack

# Iniciar
localstack start

# Desplegar a LocalStack
aws --endpoint-url=http://localhost:4566 cloudformation create-stack ...
```

3. **Test unitario:**
```bash
# Test sin AWS
cd Infrastructure/P2P
python test_client.py
```

---

**Estado actual:** ✅ CloudFormation template corregido  
**Siguiente paso:** Configurar credenciales AWS y desplegar

**Cambio aplicado:**
- Logging de API Gateway deshabilitado
- Lambda logs siguen funcionando
- Stack debería desplegar sin errores ahora
