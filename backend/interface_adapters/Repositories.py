"""
Repository Implementations for Mobile Tracking System

This module implements the repository interfaces using SQLAlchemy ORM.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from domain.Entities import User, Phone, Report, TransferRequest, RetailerPurchase
from domain.Interfaces import (
    UserRepositoryInterface,
    PhoneRepositoryInterface,
    ReportRepositoryInterface,
    TransferRequestRepositoryInterface,
    RetailerPurchaseRepositoryInterface
)
from models import (
    User as UserModel,
    Phone as PhoneModel,
    Report as ReportModel,
    TransferRequest as TransferRequestModel,
    RetailerPurchase as RetailerPurchaseModel
)


class UserRepository(UserRepositoryInterface):
    """Implementation of user repository using SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_user(self, user: User) -> User:
        """Create a new user"""
        db_user = UserModel(
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            cnic=user.cnic,
            ntn=user.ntn,
            shop_address=user.shop_address
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        # Update the entity with the generated ID
        user.id = db_user.id
        user.created_at = db_user.created_at
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            return User(
                id=db_user.id,
                email=db_user.email,
                password_hash=db_user.password_hash,
                role=db_user.role,
                cnic=db_user.cnic,
                ntn=db_user.ntn,
                shop_address=db_user.shop_address,
                created_at=db_user.created_at
            )
        return None

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
        if db_user:
            return User(
                id=db_user.id,
                email=db_user.email,
                password_hash=db_user.password_hash,
                role=db_user.role,
                cnic=db_user.cnic,
                ntn=db_user.ntn,
                shop_address=db_user.shop_address,
                created_at=db_user.created_at
            )
        return None

    def get_user_by_cnic(self, cnic: str) -> Optional[User]:
        """Get user by CNIC"""
        db_user = self.db.query(UserModel).filter(UserModel.cnic == cnic).first()
        if db_user:
            return User(
                id=db_user.id,
                email=db_user.email,
                password_hash=db_user.password_hash,
                role=db_user.role,
                cnic=db_user.cnic,
                ntn=db_user.ntn,
                shop_address=db_user.shop_address,
                created_at=db_user.created_at
            )
        return None

    def update_user(self, user: User) -> User:
        """Update user"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if db_user:
            db_user.email = user.email
            db_user.password_hash = user.password_hash
            db_user.role = user.role
            db_user.cnic = user.cnic
            db_user.ntn = user.ntn
            db_user.shop_address = user.shop_address
            self.db.commit()
            self.db.refresh(db_user)
            
            user.created_at = db_user.created_at
        return user

    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False

    def get_all_users(self) -> List[User]:
        """Get all users"""
        db_users = self.db.query(UserModel).all()
        users = []
        for db_user in db_users:
            users.append(User(
                id=db_user.id,
                email=db_user.email,
                password_hash=db_user.password_hash,
                role=db_user.role,
                cnic=db_user.cnic,
                ntn=db_user.ntn,
                shop_address=db_user.shop_address,
                created_at=db_user.created_at
            ))
        return users


class PhoneRepository(PhoneRepositoryInterface):
    """Implementation of phone repository using SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_phone(self, phone: Phone) -> Phone:
        """Create a new phone"""
        import json
        db_phone = PhoneModel(
            owner_id=phone.owner_id,
            brand=phone.brand,
            model=phone.model,
            imei=phone.imei,
            sim_numbers=json.dumps(phone.sim_numbers) if phone.sim_numbers else None,
            emails=json.dumps(phone.emails) if phone.emails else None,
            status=phone.status
        )
        self.db.add(db_phone)
        self.db.commit()
        self.db.refresh(db_phone)
        
        # Update the entity with the generated ID
        phone.id = db_phone.id
        phone.created_at = db_phone.created_at
        return phone

    def get_phone_by_id(self, phone_id: int) -> Optional[Phone]:
        """Get phone by ID"""
        import json
        db_phone = self.db.query(PhoneModel).filter(PhoneModel.id == phone_id).first()
        if db_phone:
            return Phone(
                id=db_phone.id,
                owner_id=db_phone.owner_id,
                brand=db_phone.brand,
                model=db_phone.model,
                imei=db_phone.imei,
                sim_numbers=json.loads(db_phone.sim_numbers) if db_phone.sim_numbers else None,
                emails=json.loads(db_phone.emails) if db_phone.emails else None,
                status=db_phone.status,
                created_at=db_phone.created_at
            )
        return None

    def get_phone_by_imei(self, imei: str) -> Optional[Phone]:
        """Get phone by IMEI"""
        import json
        db_phone = self.db.query(PhoneModel).filter(PhoneModel.imei == imei).first()
        if db_phone:
            return Phone(
                id=db_phone.id,
                owner_id=db_phone.owner_id,
                brand=db_phone.brand,
                model=db_phone.model,
                imei=db_phone.imei,
                sim_numbers=json.loads(db_phone.sim_numbers) if db_phone.sim_numbers else None,
                emails=json.loads(db_phone.emails) if db_phone.emails else None,
                status=db_phone.status,
                created_at=db_phone.created_at
            )
        return None

    def get_phones_by_owner(self, owner_id: int) -> List[Phone]:
        """Get phones by owner ID"""
        import json
        db_phones = self.db.query(PhoneModel).filter(PhoneModel.owner_id == owner_id).all()
        phones = []
        for db_phone in db_phones:
            phones.append(Phone(
                id=db_phone.id,
                owner_id=db_phone.owner_id,
                brand=db_phone.brand,
                model=db_phone.model,
                imei=db_phone.imei,
                sim_numbers=json.loads(db_phone.sim_numbers) if db_phone.sim_numbers else None,
                emails=json.loads(db_phone.emails) if db_phone.emails else None,
                status=db_phone.status,
                created_at=db_phone.created_at
            ))
        return phones

    def update_phone(self, phone: Phone) -> Phone:
        """Update phone"""
        import json
        db_phone = self.db.query(PhoneModel).filter(PhoneModel.id == phone.id).first()
        if db_phone:
            db_phone.owner_id = phone.owner_id
            db_phone.brand = phone.brand
            db_phone.model = phone.model
            db_phone.imei = phone.imei
            db_phone.sim_numbers = json.dumps(phone.sim_numbers) if phone.sim_numbers else None
            db_phone.emails = json.dumps(phone.emails) if phone.emails else None
            db_phone.status = phone.status
            self.db.commit()
            self.db.refresh(db_phone)
            
            phone.created_at = db_phone.created_at
        return phone

    def delete_phone(self, phone_id: int) -> bool:
        """Delete phone"""
        db_phone = self.db.query(PhoneModel).filter(PhoneModel.id == phone_id).first()
        if db_phone:
            self.db.delete(db_phone)
            self.db.commit()
            return True
        return False


class ReportRepository(ReportRepositoryInterface):
    """Implementation of report repository using SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_report(self, report: Report) -> Report:
        """Create a new report"""
        db_report = ReportModel(
            citizen_id=report.citizen_id,
            phone_id=report.phone_id,
            report_type=report.report_type,
            description=report.description,
            culprit_description=report.culprit_description,
            status=report.status,
            matched_purchase_id=report.matched_purchase_id
        )
        self.db.add(db_report)
        self.db.commit()
        self.db.refresh(db_report)
        
        # Update the entity with the generated ID
        report.id = db_report.id
        report.created_at = db_report.created_at
        report.updated_at = db_report.updated_at
        return report

    def get_report_by_id(self, report_id: int) -> Optional[Report]:
        """Get report by ID"""
        db_report = self.db.query(ReportModel).filter(ReportModel.id == report_id).first()
        if db_report:
            return Report(
                id=db_report.id,
                citizen_id=db_report.citizen_id,
                phone_id=db_report.phone_id,
                report_type=db_report.report_type,
                description=db_report.description,
                culprit_description=db_report.culprit_description,
                status=db_report.status,
                matched_purchase_id=db_report.matched_purchase_id,
                created_at=db_report.created_at,
                updated_at=db_report.updated_at
            )
        return None

    def get_reports_by_citizen(self, citizen_id: int) -> List[Report]:
        """Get reports by citizen ID"""
        db_reports = self.db.query(ReportModel).filter(ReportModel.citizen_id == citizen_id).all()
        reports = []
        for db_report in db_reports:
            reports.append(Report(
                id=db_report.id,
                citizen_id=db_report.citizen_id,
                phone_id=db_report.phone_id,
                report_type=db_report.report_type,
                description=db_report.description,
                culprit_description=db_report.culprit_description,
                status=db_report.status,
                matched_purchase_id=db_report.matched_purchase_id,
                created_at=db_report.created_at,
                updated_at=db_report.updated_at
            ))
        return reports

    def get_all_reports(self) -> List[Report]:
        """Get all reports"""
        db_reports = self.db.query(ReportModel).all()
        reports = []
        for db_report in db_reports:
            reports.append(Report(
                id=db_report.id,
                citizen_id=db_report.citizen_id,
                phone_id=db_report.phone_id,
                report_type=db_report.report_type,
                description=db_report.description,
                culprit_description=db_report.culprit_description,
                status=db_report.status,
                matched_purchase_id=db_report.matched_purchase_id,
                created_at=db_report.created_at,
                updated_at=db_report.updated_at
            ))
        return reports

    def update_report(self, report: Report) -> Report:
        """Update report"""
        db_report = self.db.query(ReportModel).filter(ReportModel.id == report.id).first()
        if db_report:
            db_report.citizen_id = report.citizen_id
            db_report.phone_id = report.phone_id
            db_report.report_type = report.report_type
            db_report.description = report.description
            db_report.culprit_description = report.culprit_description
            db_report.status = report.status
            db_report.matched_purchase_id = report.matched_purchase_id
            self.db.commit()
            self.db.refresh(db_report)
            
            report.created_at = db_report.created_at
            report.updated_at = db_report.updated_at
        return report

    def delete_report(self, report_id: int) -> bool:
        """Delete report"""
        db_report = self.db.query(ReportModel).filter(ReportModel.id == report_id).first()
        if db_report:
            self.db.delete(db_report)
            self.db.commit()
            return True
        return False


class TransferRequestRepository(TransferRequestRepositoryInterface):
    """Implementation of transfer request repository using SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_transfer_request(self, transfer_request: TransferRequest) -> TransferRequest:
        """Create a new transfer request"""
        db_transfer = TransferRequestModel(
            from_citizen_id=transfer_request.from_citizen_id,
            to_citizen_cnic=transfer_request.to_citizen_cnic,
            to_citizen_email=transfer_request.to_citizen_email,
            phone_id=transfer_request.phone_id,
            status=transfer_request.status,
            admin_notes=transfer_request.admin_notes
        )
        self.db.add(db_transfer)
        self.db.commit()
        self.db.refresh(db_transfer)
        
        # Update the entity with the generated ID
        transfer_request.id = db_transfer.id
        transfer_request.created_at = db_transfer.created_at
        transfer_request.updated_at = db_transfer.updated_at
        return transfer_request

    def get_transfer_request_by_id(self, request_id: int) -> Optional[TransferRequest]:
        """Get transfer request by ID"""
        db_transfer = self.db.query(TransferRequestModel).filter(TransferRequestModel.id == request_id).first()
        if db_transfer:
            return TransferRequest(
                id=db_transfer.id,
                from_citizen_id=db_transfer.from_citizen_id,
                to_citizen_cnic=db_transfer.to_citizen_cnic,
                to_citizen_email=db_transfer.to_citizen_email,
                phone_id=db_transfer.phone_id,
                status=db_transfer.status,
                admin_notes=db_transfer.admin_notes,
                created_at=db_transfer.created_at,
                updated_at=db_transfer.updated_at
            )
        return None

    def get_transfer_requests_by_citizen(self, citizen_id: int) -> List[TransferRequest]:
        """Get transfer requests by citizen ID"""
        db_transfers = self.db.query(TransferRequestModel).filter(TransferRequestModel.from_citizen_id == citizen_id).all()
        transfers = []
        for db_transfer in db_transfers:
            transfers.append(TransferRequest(
                id=db_transfer.id,
                from_citizen_id=db_transfer.from_citizen_id,
                to_citizen_cnic=db_transfer.to_citizen_cnic,
                to_citizen_email=db_transfer.to_citizen_email,
                phone_id=db_transfer.phone_id,
                status=db_transfer.status,
                admin_notes=db_transfer.admin_notes,
                created_at=db_transfer.created_at,
                updated_at=db_transfer.updated_at
            ))
        return transfers

    def get_all_transfer_requests(self) -> List[TransferRequest]:
        """Get all transfer requests"""
        db_transfers = self.db.query(TransferRequestModel).all()
        transfers = []
        for db_transfer in db_transfers:
            transfers.append(TransferRequest(
                id=db_transfer.id,
                from_citizen_id=db_transfer.from_citizen_id,
                to_citizen_cnic=db_transfer.to_citizen_cnic,
                to_citizen_email=db_transfer.to_citizen_email,
                phone_id=db_transfer.phone_id,
                status=db_transfer.status,
                admin_notes=db_transfer.admin_notes,
                created_at=db_transfer.created_at,
                updated_at=db_transfer.updated_at
            ))
        return transfers

    def update_transfer_request(self, transfer_request: TransferRequest) -> TransferRequest:
        """Update transfer request"""
        db_transfer = self.db.query(TransferRequestModel).filter(TransferRequestModel.id == transfer_request.id).first()
        if db_transfer:
            db_transfer.from_citizen_id = transfer_request.from_citizen_id
            db_transfer.to_citizen_cnic = transfer_request.to_citizen_cnic
            db_transfer.to_citizen_email = transfer_request.to_citizen_email
            db_transfer.phone_id = transfer_request.phone_id
            db_transfer.status = transfer_request.status
            db_transfer.admin_notes = transfer_request.admin_notes
            self.db.commit()
            self.db.refresh(db_transfer)
            
            transfer_request.created_at = db_transfer.created_at
            transfer_request.updated_at = db_transfer.updated_at
        return transfer_request

    def delete_transfer_request(self, request_id: int) -> bool:
        """Delete transfer request"""
        db_transfer = self.db.query(TransferRequestModel).filter(TransferRequestModel.id == request_id).first()
        if db_transfer:
            self.db.delete(db_transfer)
            self.db.commit()
            return True
        return False


class RetailerPurchaseRepository(RetailerPurchaseRepositoryInterface):
    """Implementation of retailer purchase repository using SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_purchase(self, purchase: RetailerPurchase) -> RetailerPurchase:
        """Create a new purchase"""
        import json
        db_purchase = RetailerPurchaseModel(
            retailer_id=purchase.retailer_id,
            customer_cnic=purchase.customer_cnic,
            customer_email=purchase.customer_email,
            phone_imei=purchase.phone_imei,
            phone_brand=purchase.phone_brand,
            phone_model=purchase.phone_model,
            phone_emails=json.dumps(purchase.phone_emails) if purchase.phone_emails else None,
            seller_cnic=purchase.seller_cnic
        )
        self.db.add(db_purchase)
        self.db.commit()
        self.db.refresh(db_purchase)
        
        # Update the entity with the generated ID
        purchase.id = db_purchase.id
        purchase.created_at = db_purchase.created_at
        return purchase

    def get_purchase_by_id(self, purchase_id: int) -> Optional[RetailerPurchase]:
        """Get purchase by ID"""
        import json
        db_purchase = self.db.query(RetailerPurchaseModel).filter(RetailerPurchaseModel.id == purchase_id).first()
        if db_purchase:
            return RetailerPurchase(
                id=db_purchase.id,
                retailer_id=db_purchase.retailer_id,
                customer_cnic=db_purchase.customer_cnic,
                customer_email=db_purchase.customer_email,
                phone_imei=db_purchase.phone_imei,
                phone_brand=db_purchase.phone_brand,
                phone_model=db_purchase.phone_model,
                phone_emails=json.loads(db_purchase.phone_emails) if db_purchase.phone_emails else None,
                seller_cnic=db_purchase.seller_cnic,
                created_at=db_purchase.created_at
            )
        return None

    def get_purchases_by_retailer(self, retailer_id: int) -> List[RetailerPurchase]:
        """Get purchases by retailer ID"""
        import json
        db_purchases = self.db.query(RetailerPurchaseModel).filter(RetailerPurchaseModel.retailer_id == retailer_id).all()
        purchases = []
        for db_purchase in db_purchases:
            purchases.append(RetailerPurchase(
                id=db_purchase.id,
                retailer_id=db_purchase.retailer_id,
                customer_cnic=db_purchase.customer_cnic,
                customer_email=db_purchase.customer_email,
                phone_imei=db_purchase.phone_imei,
                phone_brand=db_purchase.phone_brand,
                phone_model=db_purchase.phone_model,
                phone_emails=json.loads(db_purchase.phone_emails) if db_purchase.phone_emails else None,
                seller_cnic=db_purchase.seller_cnic,
                created_at=db_purchase.created_at
            ))
        return purchases

    def get_all_purchases(self) -> List[RetailerPurchase]:
        """Get all purchases"""
        import json
        db_purchases = self.db.query(RetailerPurchaseModel).all()
        purchases = []
        for db_purchase in db_purchases:
            purchases.append(RetailerPurchase(
                id=db_purchase.id,
                retailer_id=db_purchase.retailer_id,
                customer_cnic=db_purchase.customer_cnic,
                customer_email=db_purchase.customer_email,
                phone_imei=db_purchase.phone_imei,
                phone_brand=db_purchase.phone_brand,
                phone_model=db_purchase.phone_model,
                phone_emails=json.loads(db_purchase.phone_emails) if db_purchase.phone_emails else None,
                seller_cnic=db_purchase.seller_cnic,
                created_at=db_purchase.created_at
            ))
        return purchases

    def update_purchase(self, purchase: RetailerPurchase) -> RetailerPurchase:
        """Update purchase"""
        import json
        db_purchase = self.db.query(RetailerPurchaseModel).filter(RetailerPurchaseModel.id == purchase.id).first()
        if db_purchase:
            db_purchase.retailer_id = purchase.retailer_id
            db_purchase.customer_cnic = purchase.customer_cnic
            db_purchase.customer_email = purchase.customer_email
            db_purchase.phone_imei = purchase.phone_imei
            db_purchase.phone_brand = purchase.phone_brand
            db_purchase.phone_model = purchase.phone_model
            db_purchase.phone_emails = json.dumps(purchase.phone_emails) if purchase.phone_emails else None
            db_purchase.seller_cnic = purchase.seller_cnic
            self.db.commit()
            self.db.refresh(db_purchase)
            
            purchase.created_at = db_purchase.created_at
        return purchase

    def delete_purchase(self, purchase_id: int) -> bool:
        """Delete purchase"""
        db_purchase = self.db.query(RetailerPurchaseModel).filter(RetailerPurchaseModel.id == purchase_id).first()
        if db_purchase:
            self.db.delete(db_purchase)
            self.db.commit()
            return True
        return False