# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (update with your NeonDB credentials)

cp .env.example .env
# Edit .env with your database URL and secret key

# Create admin account
python create_admin.py

# Start backend server
uvicorn main:app --reload
```

Backend runs at: <http://localhost:8000>
API Documentation: <http://localhost:8000/docs>

### Step 2: Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Start development server
npm run dev
```

Frontend runs at: <http://localhost:3000>

### Step 3: Login

**Or create a new account:**

- Go to <http://localhost:3000/signup>
- Choose Citizen or Retailer
- Fill in the form

## 📊 Test the System

### As a Citizen

1. Register a phone with IMEI
2. Report it as lost/snatched
3. View reports status

### As a Retailer

1. Register a purchase with the same IMEI
2. System automatically matches it

### As Admin

1. View the match in the "Matches" tab
2. See all system statistics
3. Approve transfer requests

## 🔧 NeonDB Setup

1. Create a free account at <https://neon.tech>
2. Create a new project
3. Copy the connection string
4. Update `DATABASE_URL` in backend/.env

Example:

```
DATABASE_URL=postgresql://username:password@ep-cool-night-12345.us-east-2.aws.neon.tech/neondb?sslmode=require
```

## 🎨 Features Overview

- ✅ JWT Authentication with bcrypt
- ✅ Role-based access control
- ✅ Automatic IMEI matching
- ✅ Real-time notifications
- ✅ Modern animated UI
- ✅ Form validation
- ✅ Protected routes
- ✅ PostgreSQL database

## 🐛 Troubleshooting

**Backend won't start:**

- Check if virtual environment is activated
- Verify DATABASE_URL in .env
- Ensure PostgreSQL is accessible

**Frontend won't start:**

- Run `npm install` again
- Check if port 3000 is available
- Verify NEXT_PUBLIC_API_URL in .env.local

**Database errors:**

- Tables auto-create on first run
- Check NeonDB connection string
- Verify database is active (NeonDB suspends after inactivity)

## 📝 Important Notes

- Change admin password in production
- Use strong SECRET_KEY in production
- Enable HTTPS for production deployment
- Update CORS origins for production

## 🎯 Next Steps

1. Deploy backend to Railway/Render/Fly.io
2. Deploy frontend to Vercel/Netlify
3. Configure production environment variables
4. Set up monitoring and logging
5. Enable rate limiting
6. Add email notifications

For detailed information, see the main README.md
