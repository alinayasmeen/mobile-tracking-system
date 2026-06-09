"""
Controllers for Mobile Tracking System

This module implements the controllers that connect the API endpoints to use cases.
"""

from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from domain.Entities import User, Phone, Report, TransferRequest, RetailerPurchase
from application.UseCases import (
    UserRegistrationUseCase,
    PhoneRegistrationUseCase,
    ReportCreationUseCase,
    IMEIMatchingUseCase,
    TransferRequestUseCase,
    RetailerPurchaseUseCase
)
from database import get_db
from auth import get_current_user, require_role, UserRole


class UserController:
    """Controller for user-related operations"""
    
    def __init__(self, user_registration_use_case: UserRegistrationUseCase):
        self.user_registration_use_case = user_registration_use_case

    def register_user(self, user_data: dict, db: Session) -> User:
        """Register a new user"""
        try:
            return self.user_registration_use_case.execute(user_data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


class PhoneController:
    """Controller for phone-related operations"""
    
    def __init__(self, phone_registration_use_case: PhoneRegistrationUseCase):
        self.phone_registration_use_case = phone_registration_use_case

    def register_phone(self, phone_data: dict, user_id: int, db: Session) -> Phone:
        """Register a new phone for a user"""
        try:
            return self.phone_registration_use_case.execute(phone_data, user_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


class ReportController:
    """Controller for report-related operations"""
    
    def __init__(self, report_creation_use_case: ReportCreationUseCase):
        self.report_creation_use_case = report_creation_use_case

    def create_report(self, report_data: dict, user_id: int, db: Session) -> Report:
        """Create a new report for a user"""
        try:
            return self.report_creation_use_case.execute(report_data, user_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


class AdminController:
    """Controller for admin operations"""
    
    def __init__(
        self,
        imei_matching_use_case: IMEIMatchingUseCase
    ):
        self.imei_matching_use_case = imei_matching_use_case

    def run_imei_analysis(self, db: Session) -> List[dict]:
        """Run system-wide IMEI matching analysis"""
        try:
            return self.imei_matching_use_case.execute()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error running IMEI analysis: {str(e)}")


class TransferController:
    """Controller for transfer-related operations"""
    
    def __init__(self, transfer_request_use_case: TransferRequestUseCase):
        self.transfer_request_use_case = transfer_request_use_case

    def create_transfer_request(self, transfer_data: dict, from_user_id: int, db: Session) -> TransferRequest:
        """Create a new transfer request"""
        try:
            return self.transfer_request_use_case.execute(transfer_data, from_user_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


class RetailerController:
    """Controller for retailer-related operations"""
    
    def __init__(self, retailer_purchase_use_case: RetailerPurchaseUseCase):
        self.retailer_purchase_use_case = retailer_purchase_use_case

    def register_purchase(self, purchase_data: dict, retailer_id: int, db: Session) -> RetailerPurchase:
        """Register a new purchase by a retailer"""
        try:
            return self.retailer_purchase_use_case.execute(purchase_data, retailer_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))