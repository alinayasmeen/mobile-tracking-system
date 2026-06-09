# Mobile Snatching Prevention & Tracking System - Development Context

## Project Overview

This is a comprehensive web application designed to prevent mobile phone theft and track stolen devices through a collaborative ecosystem of citizens, retailers, and administrators. The system enables citizens to register their mobile phones, report lost/stolen devices, and facilitates automatic matching when retailers purchase phones from individuals who may be selling stolen devices.

### Architecture

- **Frontend**: Next.js 14 (React) with TypeScript and Tailwind CSS
- **Backend**: FastAPI (Python) with SQLAlchemy ORM
- **Database**: PostgreSQL (NeonDB)
- **Authentication**: JWT-based with custom authentication system
- **Password Hashing**: bcrypt

### Key Features

1. **Citizen Dashboard**: Register mobile phones (IMEI, brand, model), report lost/snatched phones, request ownership transfers
2. **Retailer Dashboard**: Register purchased phones from customers, submit received phone details for verification
3. **Admin Dashboard**: Manage users, view all registered phones/reports, automatic IMEI matching between reports and retailer records
4. **Automated IMEI Matching Agent**: Intelligent system for automated IMEI matching and report state evaluation with confidence scoring. The system uses a separate OpenAI agent service running as a microservice to handle complex matching logic.

### Core Components

#### Backend Structure (`/backend`)

- `main.py`: FastAPI application with all API routes and business logic (refactored to clean architecture)
- `domain/`: Domain layer with entities and business rules
  - `Entities.py`: Core business entities with validation rules
  - `Interfaces.py`: Abstract interfaces for repositories and services
- `application/`: Application layer with use cases and business logic
  - `UseCases.py`: Business logic use cases
- `interface_adapters/`: Interface adapters layer (controllers, presenters, gateways)
  - `Controllers.py`: Controllers connecting API endpoints to use cases
  - `Repositories.py`: Repository implementations using SQLAlchemy
- `infrastructure/`: Infrastructure layer (frameworks and drivers)
  - `models.py`: SQLAlchemy database models defining the schema
  - `auth.py`: Authentication utilities (JWT, password hashing, role-based access)
  - `database.py`: Database connection and session management
  - `create_admin.py`: Script to create the default admin user
  - `imei_matching_agent.py`: Interface to communicate with the OpenAI agent service for IMEI matching
  - `openai_imei_agent_client.py`: HTTP client to communicate with the agent service

#### Agent Services Structure (`/agents`)
- `agent_service.py`: FastAPI application for the OpenAI agent service microservice
- `openai_imei_agent_service.py`: OpenAI agent service for intelligent IMEI matching
- `agent_models.py`: Shared data models for the agent system

#### Frontend Structure (`/frontend`)

- Next.js app directory with React components
- API integration for all backend services
- Role-based routing and protected pages
- Modern UI with Tailwind CSS and Framer Motion animations

### Database Schema

- **Users**: Stores citizen, retailer, and admin accounts with role-based access (includes shop_address for retailers)
- **Phones**: Mobile device registrations with IMEI, brand, model, and ownership
- **Reports**: Lost/snatched phone reports with status tracking
- **Transfer Requests**: Ownership transfer requests between citizens
- **Retailer Purchases**: Records of phones purchased by retailers from customers

### Security Features

- JWT-based authentication with httpOnly cookie-like implementation
- bcrypt password hashing
- Role-based access control (RBAC)
- Input validation (CNIC: 13 digits, IMEI: 15 digits)
- SQL injection prevention with parameterized queries

### Key Business Logic

1. **Automatic IMEI Matching**: System automatically flags phones when IMEI in snatched reports matches retailer purchase records
2. **Status Management**: Reports transition through PENDING → VERIFIED → MATCHED states
3. **Ownership Transfers**: Citizens can request phone ownership transfers requiring admin approval

## Building and Running

### Backend Setup

1. Navigate to backend directory: `cd backend`
2. Create virtual environment: `python -m venv venv` and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Create `.env` file with database URL and secret key
5. Run admin creation script: `python create_admin.py`
6. Start server: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

### Frontend Setup

1. Navigate to frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Create `.env.local` with API URL
4. Start development server: `npm run dev`

## Development Conventions

### Backend (Python/FastAPI)

- Follow RESTful API design principles
- Use Pydantic models for request/response validation
- Implement role-based access control using decorators
- Store sensitive data in environment variables
- Use SQLAlchemy ORM for database operations

### Frontend (Next.js/React)

- Use TypeScript for type safety
- Implement responsive design with Tailwind CSS
- Follow Next.js app directory structure
- Use proper error handling and loading states
- Implement form validation before API calls

### Database Design

- Maintain referential integrity with foreign keys
- Use enums for status fields to ensure consistency
- Index frequently queried columns (email, IMEI, CNIC)
- Store JSON data as text fields with serialization

## Important Files and Directories

### Backend

- `main.py`: Contains all API endpoints and core business logic
- `models.py`: Defines database schema and relationships
- `auth.py`: Authentication and authorization functions
- `requirements.txt`: Python dependencies

### Frontend

- `package.json`: Node.js dependencies and scripts
- `src/app/`: Next.js app router pages
- `src/components/`: Reusable React components
- `src/lib/`: Utility functions and API helpers

## API Endpoints

### Authentication

- POST `/auth/signup` - Citizen/Retailer registration (now includes shop_address for retailers)
- POST `/auth/login` - User login
- GET `/auth/me` - Get current user

### Citizens

- POST `/citizen/phones` - Register phone
- GET `/citizen/phones` - Get my phones
- POST `/citizen/reports` - Create lost/snatched report
- GET `/citizen/reports` - Get my reports
- POST `/citizen/transfer-request` - Request ownership transfer

### Retailers

- POST `/retailer/purchases` - Register purchase
- GET `/retailer/purchases` - Get purchase history
- POST `/retailer/received-phone` - Submit received phone

### Admin

- GET `/admin/users` - Get all users
- GET `/admin/phones` - Get all phones
- GET `/admin/reports` - Get all reports
- GET `/admin/purchases` - Get all purchases
- PUT `/admin/reports/{id}` - Update report status
- PUT `/admin/transfer-requests/{id}` - Approve/reject transfer
- GET `/admin/stats` - Get dashboard statistics
- GET `/admin/matches` - Get IMEI matches
- GET `/admin/imei-analysis` - Run system-wide IMEI matching analysis using AI agent

## Testing and Validation

The system includes automatic matching logic that can be tested by:

1. Creating a citizen account and registering a phone with IMEI
2. Reporting the phone as snatched
3. Having a retailer register a purchase with the same IMEI
4. Verifying that the system automatically flags the match in the admin dashboard
