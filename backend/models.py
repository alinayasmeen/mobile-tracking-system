from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    CITIZEN = "citizen"
    RETAILER = "retailer"
    ADMIN = "admin"

class PhoneStatus(str, enum.Enum):
    ACTIVE = "active"
    LOST = "lost"
    SNATCHED = "snatched"
    SOLD = "sold"

class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    MATCHED = "matched"
    CLEARED = "cleared"

class TransferStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    cnic = Column(String(13), unique=True, index=True, nullable=False)
    ntn = Column(String, nullable=True)  # Only for retailers
    shop_address = Column(String, nullable=True)  # Only for retailers
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    phones = relationship("Phone", back_populates="owner", foreign_keys="Phone.owner_id")
    reports = relationship("Report", back_populates="citizen")
    transfers_from = relationship("TransferRequest", back_populates="from_citizen", foreign_keys="TransferRequest.from_citizen_id")
    retailer_purchases = relationship("RetailerPurchase", back_populates="retailer")

class Phone(Base):
    __tablename__ = "phones"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    imei = Column(String(15), unique=True, index=True, nullable=False)
    sim_numbers = Column(Text, nullable=True)  # JSON string
    emails = Column(Text, nullable=True)  # JSON string
    status = Column(Enum(PhoneStatus), default=PhoneStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="phones", foreign_keys=[owner_id])
    reports = relationship("Report", back_populates="phone")
    transfer_requests = relationship("TransferRequest", back_populates="phone")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    phone_id = Column(Integer, ForeignKey("phones.id"), nullable=False)
    report_type = Column(String, nullable=False)  # "lost" or "snatched"
    description = Column(Text, nullable=True)
    culprit_description = Column(Text, nullable=True)  # For snatched cases
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    matched_purchase_id = Column(Integer, ForeignKey("retailer_purchases.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    citizen = relationship("User", back_populates="reports")
    phone = relationship("Phone", back_populates="reports")
    matched_purchase = relationship("RetailerPurchase", foreign_keys=[matched_purchase_id])

class TransferRequest(Base):
    __tablename__ = "transfer_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    from_citizen_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_citizen_cnic = Column(String(13), nullable=False)
    to_citizen_email = Column(String, nullable=False)
    phone_id = Column(Integer, ForeignKey("phones.id"), nullable=False)
    status = Column(Enum(TransferStatus), default=TransferStatus.PENDING)
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    from_citizen = relationship("User", back_populates="transfers_from", foreign_keys=[from_citizen_id])
    phone = relationship("Phone", back_populates="transfer_requests")

class RetailerPurchase(Base):
    __tablename__ = "retailer_purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    retailer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_cnic = Column(String(13), nullable=False)
    customer_email = Column(String, nullable=False)
    phone_imei = Column(String(15), index=True, nullable=False)
    phone_brand = Column(String, nullable=False)
    phone_model = Column(String, nullable=False)
    phone_emails = Column(Text, nullable=True)  # JSON string
    seller_cnic = Column(String(13), nullable=True)  # For received phones
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    retailer = relationship("User", back_populates="retailer_purchases")
