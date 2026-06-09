"""
Domain Interfaces for Mobile Tracking System

This module defines the abstract interfaces for repositories and services.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.Entities import User, Phone, Report, TransferRequest, RetailerPurchase


class UserRepositoryInterface(ABC):
    """Abstract interface for user repository"""
    
    @abstractmethod
    def create_user(self, user: User) -> User:
        """Create a new user"""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass

    @abstractmethod
    def get_user_by_cnic(self, cnic: str) -> Optional[User]:
        """Get user by CNIC"""
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        """Update user"""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Get all users"""
        pass


class PhoneRepositoryInterface(ABC):
    """Abstract interface for phone repository"""
    
    @abstractmethod
    def create_phone(self, phone: Phone) -> Phone:
        """Create a new phone"""
        pass

    @abstractmethod
    def get_phone_by_id(self, phone_id: int) -> Optional[Phone]:
        """Get phone by ID"""
        pass

    @abstractmethod
    def get_phone_by_imei(self, imei: str) -> Optional[Phone]:
        """Get phone by IMEI"""
        pass

    @abstractmethod
    def get_phones_by_owner(self, owner_id: int) -> List[Phone]:
        """Get phones by owner ID"""
        pass

    @abstractmethod
    def update_phone(self, phone: Phone) -> Phone:
        """Update phone"""
        pass

    @abstractmethod
    def delete_phone(self, phone_id: int) -> bool:
        """Delete phone"""
        pass


class ReportRepositoryInterface(ABC):
    """Abstract interface for report repository"""
    
    @abstractmethod
    def create_report(self, report: Report) -> Report:
        """Create a new report"""
        pass

    @abstractmethod
    def get_report_by_id(self, report_id: int) -> Optional[Report]:
        """Get report by ID"""
        pass

    @abstractmethod
    def get_reports_by_citizen(self, citizen_id: int) -> List[Report]:
        """Get reports by citizen ID"""
        pass

    @abstractmethod
    def get_all_reports(self) -> List[Report]:
        """Get all reports"""
        pass

    @abstractmethod
    def update_report(self, report: Report) -> Report:
        """Update report"""
        pass

    @abstractmethod
    def delete_report(self, report_id: int) -> bool:
        """Delete report"""
        pass


class TransferRequestRepositoryInterface(ABC):
    """Abstract interface for transfer request repository"""
    
    @abstractmethod
    def create_transfer_request(self, transfer_request: TransferRequest) -> TransferRequest:
        """Create a new transfer request"""
        pass

    @abstractmethod
    def get_transfer_request_by_id(self, request_id: int) -> Optional[TransferRequest]:
        """Get transfer request by ID"""
        pass

    @abstractmethod
    def get_transfer_requests_by_citizen(self, citizen_id: int) -> List[TransferRequest]:
        """Get transfer requests by citizen ID"""
        pass

    @abstractmethod
    def get_all_transfer_requests(self) -> List[TransferRequest]:
        """Get all transfer requests"""
        pass

    @abstractmethod
    def update_transfer_request(self, transfer_request: TransferRequest) -> TransferRequest:
        """Update transfer request"""
        pass

    @abstractmethod
    def delete_transfer_request(self, request_id: int) -> bool:
        """Delete transfer request"""
        pass


class RetailerPurchaseRepositoryInterface(ABC):
    """Abstract interface for retailer purchase repository"""
    
    @abstractmethod
    def create_purchase(self, purchase: RetailerPurchase) -> RetailerPurchase:
        """Create a new purchase"""
        pass

    @abstractmethod
    def get_purchase_by_id(self, purchase_id: int) -> Optional[RetailerPurchase]:
        """Get purchase by ID"""
        pass

    @abstractmethod
    def get_purchases_by_retailer(self, retailer_id: int) -> List[RetailerPurchase]:
        """Get purchases by retailer ID"""
        pass

    @abstractmethod
    def get_all_purchases(self) -> List[RetailerPurchase]:
        """Get all purchases"""
        pass

    @abstractmethod
    def update_purchase(self, purchase: RetailerPurchase) -> RetailerPurchase:
        """Update purchase"""
        pass

    @abstractmethod
    def delete_purchase(self, purchase_id: int) -> bool:
        """Delete purchase"""
        pass