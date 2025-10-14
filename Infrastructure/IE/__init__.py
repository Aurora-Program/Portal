"""
Aurora Intelligence Engine - Package Initialization
====================================================

Exporta las interfaces principales para uso externo.

Usage:
    from Infrastructure.IE import Aurora, FractalTensor
    
    aurora = Aurora()
    aurora.learn([[1, 0, 1], [0, 1, 0]])
    result = aurora.query([1, None, None])
"""

# API de alto nivel (user-friendly)
from .aurora_engine import (
    Aurora,
    AuroraCognitiveCycle,
    MetricsCollector,
    KnowledgeBasePersistence,
    run_all_tests
)

# Core components (avanzado)
from .core import (
    FractalTensor,
    Trigate,
    TernaryLogic,
    FractalKnowledgeBase,
    Transcender,
    Evolver,
    Extender,
    Armonizador,
    RecursiveDeductionNetwork,
    TensorPoolManager,
    pattern0_create_fractal_cluster,
    CoherenceError,
    PHI
)

# Version
__version__ = "1.0.0"
__author__ = "Aurora Alliance"
__license__ = "Apache-2.0 + CC-BY-4.0"

# Public API
__all__ = [
    # High-level API
    'Aurora',
    'AuroraCognitiveCycle',
    'MetricsCollector',
    'KnowledgeBasePersistence',
    
    # Core components
    'FractalTensor',
    'Trigate',
    'TernaryLogic',
    'FractalKnowledgeBase',
    'Transcender',
    'Evolver',
    'Extender',
    'Armonizador',
    'RecursiveDeductionNetwork',
    'TensorPoolManager',
    
    # Utilities
    'pattern0_create_fractal_cluster',
    'run_all_tests',
    'CoherenceError',
    'PHI',
    
    # Metadata
    '__version__',
    '__author__',
    '__license__'
]
