#!/usr/bin/python3
"""Roles class for the roles"""

from enum import Enum as PyEnum

class UserRole(PyEnum):
    """This class defines the user roles"""
    SUPER_ADMIN = "super admin"
    P_A = "personal assistant"
    ADMIN = "admin"
    DRIVER = "driver"
    BODYGUARD = "bodyguard"
    RESEARCHER = "researcher"
    COORDINATOR = "coordinator"
    SECRETARY = "secretary"
    CHIEF_SECURITY_OFFICER = "chief security officer"
    CHIEF_FIELD_OFFICER = "chief field officer"
    FIELD_OFFICER = "field officer"
    OTHER = "other"
    
