"""
Application Use Cases for Mobile Tracking System

This module defines the business logic use cases for the application.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.Entities import User, Phone, Report, TransferRequest, RetailerPurchase, ReportStatus
from domain.Interfaces import UserRepositoryInterface, PhoneRepositoryInterface, ReportRepositoryInterface, \
    TransferRequestRepositoryInterface, RetailerPurchaseRepositoryInterface


class UseCase(ABC):
    """Base use case interface"""
    pass


class UserRegistrationUseCase(UseCase):
    """Use case for user registration"""
    
    def __init__(
        self,
        user_repo: UserRepositoryInterface
    ):
        self.user_repo = user_repo

    def execute(self, user_data: dict) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = self.user_repo.get_user_by_email(user_data['email'])
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_cnic = self.user_repo.get_user_by_cnic(user_data['cnic'])
        if existing_cnic:
            raise ValueError("CNIC already registered")
        
        # Create user instance
        user = User(
            email=user_data['email'],
            password_hash=user_data['password_hash'],
            role=user_data['role'],
            cnic=user_data['cnic'],
            ntn=user_data.get('ntn'),
            shop_address=user_data.get('shop_address')
        )
        
        # Save user
        return self.user_repo.create_user(user)


class PhoneRegistrationUseCase(UseCase):
    """Use case for phone registration"""
    
    def __init__(
        self,
        phone_repo: PhoneRepositoryInterface,
        user_repo: UserRepositoryInterface
    ):
        self.phone_repo = phone_repo
        self.user_repo = user_repo

    def execute(self, phone_data: dict, user_id: int) -> Phone:
        """Register a new phone for a user"""
        # Verify user exists
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Check if IMEI already exists
        existing_phone = self.phone_repo.get_phone_by_imei(phone_data['imei'])
        if existing_phone:
            raise ValueError("Phone with this IMEI already registered")
        
        # Create phone instance
        phone = Phone(
            owner_id=user_id,
            brand=phone_data['brand'],
            model=phone_data['model'],
            imei=phone_data['imei'],
            sim_numbers=phone_data.get('sim_numbers', []),
            emails=phone_data.get('emails', [])
        )
        
        # Save phone
        return self.phone_repo.create_phone(phone)


class ReportCreationUseCase(UseCase):
    """Use case for creating reports"""
    
    def __init__(
        self,
        report_repo: ReportRepositoryInterface,
        phone_repo: PhoneRepositoryInterface,
        user_repo: UserRepositoryInterface
    ):
        self.report_repo = report_repo
        self.phone_repo = phone_repo
        self.user_repo = user_repo

    def execute(self, report_data: dict, user_id: int) -> Report:
        """Create a new report for a user's phone"""
        # Verify user and phone exist
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        phone = self.phone_repo.get_phone_by_id(report_data['phone_id'])
        if not phone or phone.owner_id != user_id:
            raise ValueError("Phone not found or does not belong to user")
        
        # Create report instance
        report = Report(
            citizen_id=user_id,
            phone_id=report_data['phone_id'],
            report_type=report_data['report_type'],
            description=report_data.get('description'),
            culprit_description=report_data.get('culprit_description') if report_data['report_type'] == "snatched" else None
        )
        
        # Save report
        return self.report_repo.create_report(report)


class IMEIMatchingUseCase(UseCase):
    """Use case for IMEI matching between reports and purchases"""
    
    def __init__(
        self,
        report_repo: ReportRepositoryInterface,
        purchase_repo: RetailerPurchaseRepositoryInterface,
        phone_repo: PhoneRepositoryInterface
    ):
        self.report_repo = report_repo
        self.purchase_repo = purchase_repo
        self.phone_repo = phone_repo

    def execute(self) -> List[dict]:
        """Find all IMEI matches between reports and purchases"""
        matches = []
        
        # Get all pending/verified snatched reports
        reports = self.report_repo.get_all_reports()
        reports = [r for r in reports if r.report_type == "snatched" and r.status in [ReportStatus.PENDING, ReportStatus.VERIFIED]]
        
        for report in reports:
            # Get phone associated with report
            phone = self.phone_repo.get_phone_by_id(report.phone_id)
            if not phone:
                continue
            
            # Check if this IMEI appears in retailer purchases
            purchases = self.purchase_repo.get_all_purchases()
            for purchase in purchases:
                if purchase.phone_imei == phone.imei:
                    matches.append({
                        "report": report,
                        "purchase": purchase,
                        "phone": phone
                    })
                    
                    # Update report status to MATCHED
                    report.status = ReportStatus.MATCHED
                    report.matched_purchase_id = purchase.id
                    self.report_repo.update_report(report)
        
        return matches


class TransferRequestUseCase(UseCase):
    """Use case for creating transfer requests"""
    
    def __init__(
        self,
        transfer_repo: TransferRequestRepositoryInterface,
        phone_repo: PhoneRepositoryInterface,
        user_repo: UserRepositoryInterface
    ):
        self.transfer_repo = transfer_repo
        self.phone_repo = phone_repo
        self.user_repo = user_repo

    def execute(self, transfer_data: dict, from_user_id: int) -> TransferRequest:
        """Create a new transfer request"""
        # Verify phone belongs to requesting user
        phone = self.phone_repo.get_phone_by_id(transfer_data['phone_id'])
        if not phone or phone.owner_id != from_user_id:
            raise ValueError("Phone not found or does not belong to user")
        
        # Verify recipient exists
        to_user = self.user_repo.get_user_by_cnic(transfer_data['to_citizen_cnic'])
        if not to_user:
            raise ValueError("Recipient with provided CNIC not found")
        
        # Create transfer request
        transfer_request = TransferRequest(
            from_citizen_id=from_user_id,
            to_citizen_cnic=transfer_data['to_citizen_cnic'],
            to_citizen_email=transfer_data['to_citizen_email'],
            phone_id=transfer_data['phone_id']
        )
        
        # Save transfer request
        return self.transfer_repo.create_transfer_request(transfer_request)


class RetailerPurchaseUseCase(UseCase):
    """Use case for registering retailer purchases"""
    
    def __init__(
        self,
        purchase_repo: RetailerPurchaseRepositoryInterface,
        user_repo: UserRepositoryInterface
    ):
        self.purchase_repo = purchase_repo
        self.user_repo = user_repo

    def execute(self, purchase_data: dict, retailer_id: int) -> RetailerPurchase:
        """Register a new purchase by a retailer"""
        # Verify retailer exists
        retailer = self.user_repo.get_user_by_id(retailer_id)
        if not retailer or retailer.role != "retailer":
            raise ValueError("Invalid retailer")
        
        # Create purchase instance
        purchase = RetailerPurchase(
            retailer_id=retailer_id,
            customer_cnic=purchase_data['customer_cnic'],
            customer_email=purchase_data['customer_email'],
            phone_imei=purchase_data['phone_imei'],
            phone_brand=purchase_data['phone_brand'],
            phone_model=purchase_data['phone_model'],
            phone_emails=purchase_data.get('phone_emails', [])
        )
        
        # Save purchase
        return self.purchase_repo.create_purchase(purchase)