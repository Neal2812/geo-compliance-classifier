"""
Evidence System Package

Centralized evidence logging, export, and monitoring for compliance decisions.
"""

from .evidence_logger import EvidenceLogger, get_evidence_logger, log_compliance_decision
from .evidence_exporter import EvidenceExporter

# Advanced features (optional dependencies)
try:
    from .evidence_monitor import EvidenceMonitor
    from .evidence_alerts import EvidenceAlertSystem
except ImportError:
    EvidenceMonitor = None
    EvidenceAlertSystem = None

__all__ = [
    'EvidenceLogger',
    'get_evidence_logger', 
    'log_compliance_decision',
    'EvidenceExporter',
    'EvidenceMonitor',
    'EvidenceAlertSystem'
]
