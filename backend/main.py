from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import timedelta
import json

from database import engine, get_db, Base
from models import User, Phone, Report, TransferRequest, RetailerPurchase  # Import database models
from domain.Entities import User as DomainUser, Phone as DomainPhone, Report as DomainReport, TransferRequest as DomainTransferRequest, RetailerPurchase as DomainRetailerPurchase, UserRole, PhoneStatus, ReportStatus, TransferStatus
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    require_role,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from imei_matching_agent import IMEIMatchingAgent
from agents.agent_models import AgentInput, EventType
from interface_adapters.Repositories import UserRepository, PhoneRepository, ReportRepository, TransferRequestRepository, RetailerPurchaseRepository
from interface_adapters.Controllers import UserController, PhoneController, ReportController, AdminController, TransferController, RetailerController
from application.UseCases import UserRegistrationUseCase, PhoneRegistrationUseCase, ReportCreationUseCase, IMEIMatchingUseCase, TransferRequestUseCase, RetailerPurchaseUseCase


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mobile Tracking System API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= Pydantic Models =============

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    cnic: str = Field(..., min_length=13, max_length=13)
    ntn: Optional[str] = None
    shop_address: Optional[str] = None
    role: UserRole

    @validator('cnic')
    def validate_cnic(cls, v):
        if not v.isdigit():
            raise ValueError('CNIC must contain only digits')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class PhoneRegisterRequest(BaseModel):
    brand: str
    model: str
    imei: str = Field(..., min_length=15, max_length=15)
    sim_numbers: Optional[List[str]] = []
    emails: Optional[List[str]] = []
    
    @validator('imei')
    def validate_imei(cls, v):
        if not v.isdigit():
            raise ValueError('IMEI must contain only digits')
        return v

class ReportCreateRequest(BaseModel):
    phone_id: int
    report_type: str  # "lost" or "snatched"
    description: Optional[str] = None
    culprit_description: Optional[str] = None
    
    @validator('report_type')
    def validate_report_type(cls, v):
        if v not in ["lost", "snatched"]:
            raise ValueError('Report type must be "lost" or "snatched"')
        return v

class TransferRequestCreate(BaseModel):
    phone_id: int
    to_citizen_cnic: str = Field(..., min_length=13, max_length=13)
    to_citizen_email: EmailStr
    
    @validator('to_citizen_cnic')
    def validate_cnic(cls, v):
        if not v.isdigit():
            raise ValueError('CNIC must contain only digits')
        return v

class RetailerPurchaseCreate(BaseModel):
    customer_cnic: str = Field(..., min_length=13, max_length=13)
    customer_email: EmailStr
    phone_imei: str = Field(..., min_length=15, max_length=15)
    phone_brand: str
    phone_model: str
    phone_emails: Optional[List[str]] = []
    
    @validator('customer_cnic')
    def validate_cnic(cls, v):
        if not v.isdigit():
            raise ValueError('CNIC must contain only digits')
        return v
    
    @validator('phone_imei')
    def validate_imei(cls, v):
        if not v.isdigit():
            raise ValueError('IMEI must contain only digits')
        return v

class ReceivedPhoneCreate(BaseModel):
    seller_cnic: str = Field(..., min_length=13, max_length=13)
    phone_imei: str = Field(..., min_length=15, max_length=15)
    phone_brand: str
    phone_model: str
    phone_emails: Optional[List[str]] = []
    
    @validator('seller_cnic')
    def validate_cnic(cls, v):
        if not v.isdigit():
            raise ValueError('CNIC must contain only digits')
        return v
    
    @validator('phone_imei')
    def validate_imei(cls, v):
        if not v.isdigit():
            raise ValueError('IMEI must contain only digits')
        return v

class ReportStatusUpdate(BaseModel):
    status: ReportStatus

class TransferStatusUpdate(BaseModel):
    status: TransferStatus
    admin_notes: Optional[str] = None

# ============= Helper Functions =============

def domain_user_to_dict(user: DomainUser) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.value,
        "cnic": user.cnic,
        "ntn": user.ntn,
        "shop_address": user.shop_address,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

def domain_phone_to_dict(phone: DomainPhone) -> dict:
    import json
    return {
        "id": phone.id,
        "owner_id": phone.owner_id,
        "brand": phone.brand,
        "model": phone.model,
        "imei": phone.imei,
        "sim_numbers": json.loads(phone.sim_numbers) if phone.sim_numbers else [],
        "emails": json.loads(phone.emails) if phone.emails else [],
        "status": phone.status.value,
        "created_at": phone.created_at.isoformat() if phone.created_at else None
    }

def domain_report_to_dict(report: DomainReport, db: Session) -> dict:
    # Get phone from repository
    phone_repo = PhoneRepository(db)
    phone = phone_repo.get_phone_by_id(report.phone_id)
    return {
        "id": report.id,
        "citizen_id": report.citizen_id,
        "phone_id": report.phone_id,
        "phone": domain_phone_to_dict(phone) if phone else None,
        "report_type": report.report_type,
        "description": report.description,
        "culprit_description": report.culprit_description,
        "status": report.status.value,
        "matched_purchase_id": report.matched_purchase_id,
        "created_at": report.created_at.isoformat() if report.created_at else None,
        "updated_at": report.updated_at.isoformat() if report.updated_at else None
    }

def domain_transfer_to_dict(transfer: DomainTransferRequest, db: Session) -> dict:
    # Get phone from repository
    phone_repo = PhoneRepository(db)
    phone = phone_repo.get_phone_by_id(transfer.phone_id)
    return {
        "id": transfer.id,
        "from_citizen_id": transfer.from_citizen_id,
        "to_citizen_cnic": transfer.to_citizen_cnic,
        "to_citizen_email": transfer.to_citizen_email,
        "phone_id": transfer.phone_id,
        "phone": domain_phone_to_dict(phone) if phone else None,
        "status": transfer.status.value,
        "admin_notes": transfer.admin_notes,
        "created_at": transfer.created_at.isoformat() if transfer.created_at else None,
        "updated_at": transfer.updated_at.isoformat() if transfer.updated_at else None
    }

def domain_purchase_to_dict(purchase: DomainRetailerPurchase) -> dict:
    import json
    return {
        "id": purchase.id,
        "retailer_id": purchase.retailer_id,
        "customer_cnic": purchase.customer_cnic,
        "customer_email": purchase.customer_email,
        "phone_imei": purchase.phone_imei,
        "phone_brand": purchase.phone_brand,
        "phone_model": purchase.phone_model,
        "phone_emails": json.loads(purchase.phone_emails) if purchase.phone_emails else [],
        "seller_cnic": purchase.seller_cnic,
        "created_at": purchase.created_at.isoformat() if purchase.created_at else None
    }

# Helper functions to convert database models to dictionaries
def user_to_dict(user) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role.value,
        "cnic": user.cnic,
        "ntn": user.ntn,
        "shop_address": user.shop_address,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

def phone_to_dict(phone) -> dict:
    import json
    return {
        "id": phone.id,
        "owner_id": phone.owner_id,
        "brand": phone.brand,
        "model": phone.model,
        "imei": phone.imei,
        "sim_numbers": json.loads(phone.sim_numbers) if phone.sim_numbers else [],
        "emails": json.loads(phone.emails) if phone.emails else [],
        "status": phone.status.value,
        "created_at": phone.created_at.isoformat() if phone.created_at else None
    }

def report_to_dict(report, db: Session) -> dict:
    # Get phone from database
    phone = db.query(Phone).filter(Phone.id == report.phone_id).first()
    return {
        "id": report.id,
        "citizen_id": report.citizen_id,
        "phone_id": report.phone_id,
        "phone": phone_to_dict(phone) if phone else None,
        "report_type": report.report_type,
        "description": report.description,
        "culprit_description": report.culprit_description,
        "status": report.status.value,
        "matched_purchase_id": report.matched_purchase_id,
        "created_at": report.created_at.isoformat() if report.created_at else None,
        "updated_at": report.updated_at.isoformat() if report.updated_at else None
    }

def transfer_to_dict(transfer, db: Session) -> dict:
    # Get phone from database
    phone = db.query(Phone).filter(Phone.id == transfer.phone_id).first()
    return {
        "id": transfer.id,
        "from_citizen_id": transfer.from_citizen_id,
        "to_citizen_cnic": transfer.to_citizen_cnic,
        "to_citizen_email": transfer.to_citizen_email,
        "phone_id": transfer.phone_id,
        "phone": phone_to_dict(phone) if phone else None,
        "status": transfer.status.value,
        "admin_notes": transfer.admin_notes,
        "created_at": transfer.created_at.isoformat() if transfer.created_at else None,
        "updated_at": transfer.updated_at.isoformat() if transfer.updated_at else None
    }

def purchase_to_dict(purchase) -> dict:
    import json
    return {
        "id": purchase.id,
        "retailer_id": purchase.retailer_id,
        "customer_cnic": purchase.customer_cnic,
        "customer_email": purchase.customer_email,
        "phone_imei": purchase.phone_imei,
        "phone_brand": purchase.phone_brand,
        "phone_model": purchase.phone_model,
        "phone_emails": json.loads(purchase.phone_emails) if purchase.phone_emails else [],
        "seller_cnic": purchase.seller_cnic,
        "created_at": purchase.created_at.isoformat() if purchase.created_at else None
    }

def check_imei_matches(db: Session):
    """Check for IMEI matches between snatched reports and retailer purchases using the OpenAI agent service"""
    # Create repositories
    report_repo = ReportRepository(db)
    phone_repo = PhoneRepository(db)
    purchase_repo = RetailerPurchaseRepository(db)
    
    # Create use case
    imei_matching_use_case = IMEIMatchingUseCase(report_repo, purchase_repo, phone_repo)
    
    # Run the matching use case
    matches = imei_matching_use_case.execute()
    
    # The use case already updates the reports, so we just return
    return matches

# ============= Authentication Routes =============

@app.post("/auth/signup", response_model=TokenResponse)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    # Create repositories
    user_repo = UserRepository(db)
    
    # Create use cases
    user_registration_use_case = UserRegistrationUseCase(user_repo)
    
    # Create controller
    user_controller = UserController(user_registration_use_case)
    
    # Prevent admin signup through this endpoint
    if request.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Admin accounts cannot be created through signup")

    # Validate NTN for retailers
    if request.role == UserRole.RETAILER and not request.ntn:
        raise HTTPException(status_code=400, detail="NTN is required for retailer accounts")

    # Prepare user data for use case
    user_data = {
        'email': request.email,
        'password_hash': get_password_hash(request.password),
        'role': request.role,
        'cnic': request.cnic,
        'ntn': request.ntn if request.role == UserRole.RETAILER else None,
        'shop_address': request.shop_address if request.role == UserRole.RETAILER else None
    }

    # Use the controller to register the user
    domain_user = user_controller.register_user(user_data, db)

    # Create access token
    access_token = create_access_token(
        data={"sub": domain_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Convert domain user to dict representation
    user_dict = {
        "id": domain_user.id,
        "email": domain_user.email,
        "role": domain_user.role.value,
        "cnic": domain_user.cnic,
        "ntn": domain_user.ntn,
        "shop_address": domain_user.shop_address,
        "created_at": domain_user.created_at.isoformat() if domain_user.created_at else None
    }

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_dict
    }

@app.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_to_dict(user)
    }

@app.get("/auth/me")
def get_me(current_user: User = Depends(get_current_user)):
    return user_to_dict(current_user)

# ============= Citizen Routes =============

@app.post("/citizen/phones")
def register_phone(
    request: PhoneRegisterRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CITIZEN))
):
    # Check if IMEI already exists
    existing_phone = db.query(Phone).filter(Phone.imei == request.imei).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone with this IMEI already registered")
    
    phone = Phone(
        owner_id=current_user.id,
        brand=request.brand,
        model=request.model,
        imei=request.imei,
        sim_numbers=json.dumps(request.sim_numbers),
        emails=json.dumps(request.emails),
        status=PhoneStatus.ACTIVE
    )
    
    db.add(phone)
    db.commit()
    db.refresh(phone)
    
    return phone_to_dict(phone)

@app.get("/citizen/phones")
def get_my_phones(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CITIZEN))
):
    phones = db.query(Phone).filter(Phone.owner_id == current_user.id).all()
    return [phone_to_dict(phone) for phone in phones]

@app.post("/citizen/reports")
def create_report(
    request: ReportCreateRequest,
    db: Session = Depends(get_db),
    current_user: DomainUser = Depends(require_role(UserRole.CITIZEN))
):
    # Create repositories
    report_repo = ReportRepository(db)
    phone_repo = PhoneRepository(db)
    user_repo = UserRepository(db)
    
    # Create use case
    report_creation_use_case = ReportCreationUseCase(report_repo, phone_repo, user_repo)
    
    # Create controller
    report_controller = ReportController(report_creation_use_case)
    
    # Prepare report data
    report_data = {
        'phone_id': request.phone_id,
        'report_type': request.report_type,
        'description': request.description,
        'culprit_description': request.culprit_description
    }
    
    # Create report using the controller
    domain_report = report_controller.create_report(report_data, current_user.id, db)
    
    # Get phone to retrieve IMEI
    phone_repo = PhoneRepository(db)
    phone = phone_repo.get_phone_by_id(request.phone_id)
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    
    # Use the OpenAI agent service to check for matches
    agent = IMEIMatchingAgent()
    agent_input = AgentInput(
        event_type=EventType.REPORT_LOST_SNATCHED,
        imei=phone.imei,  # Get IMEI from phone
        report_id=domain_report.id,
        report_status=ReportStatus.PENDING.value,  # Convert enum to string for OpenAI
        user_role="citizen"
    )

    response = agent.process_event(agent_input)

    # Process the agent's recommendations
    for match in response.matches:
        if match.match_found and match.confidence_score >= 0.9:
            # Update report status and matched purchase ID
            domain_report.status = ReportStatus.MATCHED
            domain_report.matched_purchase_id = match.matched_purchase_id
            report_repo.update_report(domain_report)
            break  # Exit loop after first match

    return domain_report_to_dict(domain_report, db)

@app.get("/citizen/reports")
def get_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CITIZEN))
):
    reports = db.query(Report).filter(Report.citizen_id == current_user.id).all()
    return [report_to_dict(report, db) for report in reports]

@app.post("/citizen/transfer-request")
def create_transfer_request(
    request: TransferRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CITIZEN))
):
    # Verify phone belongs to user
    phone = db.query(Phone).filter(
        Phone.id == request.phone_id,
        Phone.owner_id == current_user.id
    ).first()
    
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found or does not belong to you")
    
    # Create transfer request
    transfer = TransferRequest(
        from_citizen_id=current_user.id,
        to_citizen_cnic=request.to_citizen_cnic,
        to_citizen_email=request.to_citizen_email,
        phone_id=request.phone_id,
        status=TransferStatus.PENDING
    )
    
    db.add(transfer)
    db.commit()
    db.refresh(transfer)
    
    return transfer_to_dict(transfer, db)

@app.get("/citizen/transfer-requests")
def get_my_transfer_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.CITIZEN))
):
    transfers = db.query(TransferRequest).filter(
        TransferRequest.from_citizen_id == current_user.id
    ).all()
    return [transfer_to_dict(transfer, db) for transfer in transfers]

# ============= Retailer Routes =============

@app.post("/retailer/purchases")
def register_purchase(
    request: RetailerPurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.RETAILER))
):
    purchase = RetailerPurchase(
        retailer_id=current_user.id,
        customer_cnic=request.customer_cnic,
        customer_email=request.customer_email,
        phone_imei=request.phone_imei,
        phone_brand=request.phone_brand,
        phone_model=request.phone_model,
        phone_emails=json.dumps(request.phone_emails)
    )

    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    # Use the OpenAI agent service to check for matches
    agent = IMEIMatchingAgent()
    agent_input = AgentInput(
        event_type=EventType.RETAILER_PURCHASE,
        imei=request.phone_imei,
        purchase_id=purchase.id,
        report_status=None,  # Not applicable for purchase events
        user_role="retailer"
    )
    
    response = agent.process_event(agent_input)
    
    # Process the agent's recommendations
    for match in response.matches:
        if match.match_found and match.confidence_score >= 0.9:
            # Update the corresponding report if found
            if match.matched_report_id:
                report = db.query(Report).filter(Report.id == match.matched_report_id).first()
                if report:
                    report.status = ReportStatus.MATCHED
                    report.matched_purchase_id = purchase.id
                    db.commit()
            break  # Exit loop after first match

    return purchase_to_dict(purchase)

@app.get("/retailer/purchases")
def get_my_purchases(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.RETAILER))
):
    purchases = db.query(RetailerPurchase).filter(
        RetailerPurchase.retailer_id == current_user.id
    ).all()
    return [purchase_to_dict(purchase) for purchase in purchases]

@app.post("/retailer/received-phone")
def submit_received_phone(
    request: ReceivedPhoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.RETAILER))
):
    purchase = RetailerPurchase(
        retailer_id=current_user.id,
        customer_cnic="",  # Will be filled when sold
        customer_email="",
        phone_imei=request.phone_imei,
        phone_brand=request.phone_brand,
        phone_model=request.phone_model,
        phone_emails=json.dumps(request.phone_emails),
        seller_cnic=request.seller_cnic
    )

    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    # Use the OpenAI agent service to check for matches
    agent = IMEIMatchingAgent()
    agent_input = AgentInput(
        event_type=EventType.RECEIVED_PHONE,
        imei=request.phone_imei,
        purchase_id=purchase.id,
        report_status=None,  # Not applicable for received phone events
        user_role="retailer"
    )
    
    response = agent.process_event(agent_input)
    
    # Process the agent's recommendations
    for match in response.matches:
        if match.match_found and match.confidence_score >= 0.9:
            # Update the corresponding report if found
            if match.matched_report_id:
                report = db.query(Report).filter(Report.id == match.matched_report_id).first()
                if report:
                    report.status = ReportStatus.MATCHED
                    report.matched_purchase_id = purchase.id
                    db.commit()
            break  # Exit loop after first match

    return purchase_to_dict(purchase)

# ============= Admin Routes =============

@app.get("/admin/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    users = db.query(User).all()
    return [user_to_dict(user) for user in users]

@app.get("/admin/phones")
def get_all_phones(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    phones = db.query(Phone).all()
    return [phone_to_dict(phone) for phone in phones]

@app.get("/admin/reports")
def get_all_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    reports = db.query(Report).all()
    return [report_to_dict(report, db) for report in reports]

@app.get("/admin/purchases")
def get_all_purchases(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    purchases = db.query(RetailerPurchase).all()
    return [purchase_to_dict(purchase) for purchase in purchases]

@app.get("/admin/transfer-requests")
def get_all_transfer_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    transfers = db.query(TransferRequest).all()
    return [transfer_to_dict(transfer, db) for transfer in transfers]

@app.put("/admin/reports/{report_id}")
def update_report_status(
    report_id: int,
    request: ReportStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report.status = request.status
    db.commit()
    db.refresh(report)
    
    return report_to_dict(report, db)

@app.put("/admin/transfer-requests/{transfer_id}")
def update_transfer_status(
    transfer_id: int,
    request: TransferStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    transfer = db.query(TransferRequest).filter(TransferRequest.id == transfer_id).first()
    if not transfer:
        raise HTTPException(status_code=404, detail="Transfer request not found")
    
    transfer.status = request.status
    if request.admin_notes:
        transfer.admin_notes = request.admin_notes
    
    # If approved, update phone ownership
    if request.status == TransferStatus.APPROVED:
        # Find or create the recipient user
        recipient = db.query(User).filter(User.cnic == transfer.to_citizen_cnic).first()
        if recipient:
            phone = db.query(Phone).filter(Phone.id == transfer.phone_id).first()
            if phone:
                phone.owner_id = recipient.id
                phone.status = PhoneStatus.ACTIVE
    
    db.commit()
    db.refresh(transfer)
    
    return transfer_to_dict(transfer, db)

@app.get("/admin/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    total_users = db.query(User).count()
    total_citizens = db.query(User).filter(User.role == UserRole.CITIZEN).count()
    total_retailers = db.query(User).filter(User.role == UserRole.RETAILER).count()
    total_phones = db.query(Phone).count()
    total_reports = db.query(Report).count()
    snatched_reports = db.query(Report).filter(Report.report_type == "snatched").count()
    matched_reports = db.query(Report).filter(Report.status == ReportStatus.MATCHED).count()
    pending_reports = db.query(Report).filter(Report.status == ReportStatus.PENDING).count()
    pending_transfers = db.query(TransferRequest).filter(
        TransferRequest.status == TransferStatus.PENDING
    ).count()
    total_purchases = db.query(RetailerPurchase).count()
    
    return {
        "total_users": total_users,
        "total_citizens": total_citizens,
        "total_retailers": total_retailers,
        "total_phones": total_phones,
        "total_reports": total_reports,
        "snatched_reports": snatched_reports,
        "matched_reports": matched_reports,
        "pending_reports": pending_reports,
        "pending_transfers": pending_transfers,
        "total_purchases": total_purchases
    }

@app.get("/admin/matches")
def get_matches(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    matched_reports = db.query(Report).filter(
        Report.status == ReportStatus.MATCHED
    ).all()

    matches = []
    for report in matched_reports:
        phone = db.query(Phone).filter(Phone.id == report.phone_id).first()
        purchase = db.query(RetailerPurchase).filter(
            RetailerPurchase.id == report.matched_purchase_id
        ).first()

        if phone and purchase:
            retailer = db.query(User).filter(User.id == purchase.retailer_id).first()
            citizen = db.query(User).filter(User.id == report.citizen_id).first()

            matches.append({
                "report": report_to_dict(report, db),
                "purchase": purchase_to_dict(purchase),
                "retailer": user_to_dict(retailer) if retailer else None,
                "citizen": user_to_dict(citizen) if citizen else None,
                "phone": phone_to_dict(phone)
            })

    return matches

@app.get("/admin/imei-analysis")
def run_imei_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Run system-wide IMEI matching analysis using the OpenAI agent service"""
    agent = IMEIMatchingAgent()
    response = agent.run_system_wide_analysis()
    
    return response

@app.get("/")
def root():
    return {
        "message": "Mobile Tracking System API",
        "version": "1.0.0",
        "docs": "/docs"
    }
