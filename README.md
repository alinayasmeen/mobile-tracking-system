# Mobile Snatching Prevention & Tracking System

A comprehensive web application for preventing mobile phone theft and tracking stolen devices through a collaborative ecosystem of citizens, retailers, and administrators.

## 🚀 Tech Stack

- **Frontend**: Next.js 14 (React) with TypeScript
- **Styling**: Tailwind CSS with custom animations
- **Backend**: FastAPI (Python)
- **Database**: NeonDB (PostgreSQL)
- **Authentication**: JWT-based with Better Auth
- **Password Hashing**: bcrypt

## 📋 Features

### Citizen Dashboard
- Register mobile phones (IMEI, brand, model, SIM numbers)
- Report lost/snatched phones with culprit descriptions
- Request phone ownership transfer (requires admin approval)
- Track report status (Pending/Verified/Matched)

### Retailer Dashboard
- Register purchased phones from customers
- Submit received phone details for verification
- View purchase history

### Admin Dashboard
- Manage all users (citizens, retailers)
- View all registered phones and reports
- Automatic IMEI matching between snatched reports and retailer records
- Update case statuses
- Analytics dashboard with alerts

## 🛠️ Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- PostgreSQL database (NeonDB account)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
DATABASE_URL=postgresql://user:password@host/database
SECRET_KEY=your-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run database migrations (tables auto-create on first run)

6. Create admin user:
```bash
python create_admin.py
```

7. Start the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start development server:
```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 🔐 Default Admin Credentials

After running `create_admin.py`:
- Email: admin@system.com
- Password: Admin@123456

**⚠️ Change these credentials immediately in production!**

## 📁 Project Structure

```
mobile-tracking-system/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── auth.py              # Authentication utilities
│   ├── database.py          # Database connection
│   ├── create_admin.py      # Admin creation script
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js app directory
│   │   ├── components/     # React components
│   │   ├── lib/           # Utilities
│   │   └── types/         # TypeScript types
│   ├── public/            # Static assets
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## 🔒 Security Features

- JWT-based authentication with httpOnly cookies
- bcrypt password hashing
- Role-based access control (RBAC)
- Protected API routes
- Input validation (CNIC: 13 digits, IMEI: 15 digits)
- SQL injection prevention with parameterized queries

## 🎨 UI Features

- Modern, animated interface
- Loading states and error handling
- Responsive design
- Form validation with real-time feedback
- Dashboard analytics
- Status badges and alerts

## 📊 Database Schema

### Users Table
- id, email, password_hash, role, cnic, ntn (retailers only), created_at

### Phones Table
- id, owner_id, brand, model, imei, sim_numbers, emails, status, created_at

### Reports Table
- id, citizen_id, phone_id, report_type, description, culprit_description, status, created_at

### Transfer Requests Table
- id, from_citizen_id, to_citizen_cnic, to_citizen_email, phone_id, status, admin_notes, created_at

### Retailer Purchases Table
- id, retailer_id, customer_cnic, customer_email, phone_imei, phone_brand, phone_model, phone_emails, created_at

## 🚨 Matching Logic

The system automatically:
1. Flags phones when IMEI in snatched reports matches retailer purchase records
2. Updates report status to "Matched"
3. Creates alerts in admin dashboard
4. Links retailer purchase records to snatched reports

## 📝 API Endpoints

### Authentication
- POST `/auth/signup` - Citizen/Retailer registration
- POST `/auth/login` - User login
- POST `/auth/logout` - User logout
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

## 🧪 Testing

Test the matching logic:
1. Citizen reports phone as snatched (with IMEI)
2. Retailer registers purchase with same IMEI
3. System automatically flags match in admin dashboard
4. Admin can see linked records

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 Support

For issues and questions, please open an issue in the repository.
