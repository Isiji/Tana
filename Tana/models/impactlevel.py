#!/usr/bin/python3
"""ImpactLevel class for the impact levels"""
from enum import Enum as PyEnum

class ImpactLevel(PyEnum):
    High = "High"
    Medium = "Medium"
    Low = "Low"