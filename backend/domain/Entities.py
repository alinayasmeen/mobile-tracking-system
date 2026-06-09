"""
Domain Entities for Mobile Tracking System

This module defines the core business entities with their business rules.
"""

from abc import ABC
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    CITIZEN = "citizen"
    RETAILER = "retailer"
    ADMIN = "admin"


class PhoneStatus(str, Enum):
    ACTIVE = "active"
    LOST = "lost"
    SNATCHED = "snatched"
    SOLD = "sold"


class ReportStatus(str, Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    MATCHED = "matched"
    CLEARED = "cleared"


class TransferStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class BaseEntity(ABC):
    """Base entity with common attributes"""
    id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class User(BaseEntity):
    """User entity representing citizens, retailers, and admins"""
    email: str = ""
    password_hash: str = ""
    role: Optional[UserRole] = None
    cnic: str = ""
    ntn: Optional[str] = None
    shop_address: Optional[str] = None
    
    def __post_init__(self):
        """Validate business rules after initialization"""
        if not self.email or '@' not in self.email:
            raise ValueError("Invalid email address")
        
        if len(self.cnic) != 13 or not self.cnic.isdigit():
            raise ValueError("CNIC must be exactly 13 digits")
        
        if self.role == UserRole.RETAILER:
            if not self.ntn:
                raise ValueError("NTN is required for retailers")
            if not self.shop_address:
                raise ValueError("Shop address is required for retailers")


@dataclass
class Phone(BaseEntity):
    """Phone entity representing a mobile device"""
    owner_id: int = 0
    brand: str = ""
    model: str = ""
    imei: str = ""
    sim_numbers: Optional[List[str]] = None
    emails: Optional[List[str]] = None
    status: PhoneStatus = PhoneStatus.ACTIVE
    
    def __post_init__(self):
        """Validate business rules after initialization"""
        if len(self.imei) != 15 or not self.imei.isdigit():
            raise ValueError("IMEI must be exactly 15 digits")
        
        if not self.brand or not self.model:
            raise ValueError("Brand and model are required")


@dataclass
class Report(BaseEntity):
    """Report entity for lost/snatched phones"""
    citizen_id: int = 0
    phone_id: int = 0
    report_type: str = ""  # "lost" or "snatched"
    description: Optional[str] = None
    culprit_description: Optional[str] = None
    status: ReportStatus = ReportStatus.PENDING
    matched_purchase_id: Optional[int] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate business rules after initialization"""
        if self.report_type not in ["lost", "snatched"]:
            raise ValueError("Report type must be 'lost' or 'snatched'")
        
        if self.report_type == "snatched" and not self.culprit_description:
            raise ValueError("Culprit description is required for snatched reports")


@dataclass
class TransferRequest(BaseEntity):
    """Transfer request entity for phone ownership transfers"""
    from_citizen_id: int = 0
    to_citizen_cnic: str = ""
    to_citizen_email: str = ""
    phone_id: int = 0
    status: TransferStatus = TransferStatus.PENDING
    admin_notes: Optional[str] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validate business rules after initialization"""
        if len(self.to_citizen_cnic) != 13 or not self.to_citizen_cnic.isdigit():
            raise ValueError("Recipient CNIC must be exactly 13 digits")


@dataclass
class RetailerPurchase(BaseEntity):
    """Retailer purchase entity for phones bought from customers"""
    retailer_id: int = 0
    customer_cnic: str = ""
    customer_email: str = ""
    phone_imei: str = ""
    phone_brand: str = ""
    phone_model: str = ""
    phone_emails: Optional[List[str]] = None
    seller_cnic: Optional[str] = None
    
    def __post_init__(self):
        """Validate business rules after initialization"""
        if len(self.customer_cnic) != 13 or not self.customer_cnic.isdigit():
            raise ValueError("Customer CNIC must be exactly 13 digits")
        
        if len(self.phone_imei) != 15 or not self.phone_imei.isdigit():
            raise ValueError("Phone IMEI must be exactly 15 digits")