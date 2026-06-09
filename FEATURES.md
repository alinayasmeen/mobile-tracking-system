# Mobile Snatching Prevention & Tracking System - Features Documentation

## 🎯 Complete Feature List

### Authentication & Authorization

#### User Roles
- **Citizen**: Register phones, report lost/snatched devices, request ownership transfers
- **Retailer**: Register purchases, submit received phones, view purchase history
- **Admin**: Full system access, manage users, approve transfers, monitor matches

#### Security Features
- ✅ JWT token-based authentication
- ✅ bcrypt password hashing (industry standard)
- ✅ Role-based access control (RBAC)
- ✅ Protected API routes with middleware
- ✅ Secure session management
- ✅ CORS configuration for API security

### Citizen Features

#### Phone Registration
- Brand and model tracking
- IMEI validation (exactly 15 digits, numeric only)
- Multiple SIM numbers support
- Multiple email addresses tracking
- Automatic status management (active/lost/snatched/sold)

#### Lost/Snatched Reporting
- Two report types: Lost or Snatched
- Optional description field
- Culprit description for snatched cases
- Status tracking:
  - **Pending**: Initial state
  - **Verified**: Admin verified the report
  - **Matched**: IMEI found in retailer records (automatic)
  - **Cleared**: Case resolved
- Automatic phone status update on report creation

#### Ownership Transfer
- Request transfer to another citizen
- Requires recipient's CNIC (13 digits) and email
- Admin approval required
- Status tracking (Pending/Approved/Rejected)
- Admin notes support
- Automatic ownership update on approval

#### Dashboard Features
- View all registered phones
- Active reports count
- Pending transfers count
- Real-time status updates
- Match alerts when phone found in retailer records

### Retailer Features

#### Purchase Registration
- Customer CNIC validation (13 digits)
- Customer email tracking
- Phone IMEI validation (15 digits)
- Phone brand and model
- Multiple emails associated with phone
- Purchase timestamp

#### Received Phone Submission
- For phones bought from sellers (second-hand market)
- Seller CNIC tracking
- Phone details (IMEI, brand, model, emails)
- Automatic IMEI verification against snatched reports

#### Dashboard Features
- Total purchases counter
- Received phones counter
- Complete purchase history
- Two-tab interface (New Purchase / Received Phone)

### Admin Features

#### User Management
- View all citizens
- View all retailers
- User details (email, CNIC, NTN for retailers)
- Role badges for quick identification

#### Phone Management
- View all registered phones
- Phone status tracking
- Owner information
- SIM and email details

#### Report Management
- View all reports (lost & snatched)
- Update report status:
  - Verify pending reports
  - Clear resolved cases
  - Mark matched reports
- View culprit descriptions
- Filter by status

#### Transfer Request Management
- View all transfer requests
- Approve transfers (automatic ownership update)
- Reject transfers
- Add admin notes
- Status tracking

#### IMEI Matching System (Core Feature)
- **Automatic matching** when:
  - Citizen reports phone as snatched
  - Retailer registers purchase with same IMEI
- Match details include:
  - Original owner information
  - Snatched report details
  - Culprit description
  - Retailer information (email, CNIC, NTN)
  - Purchase details (customer/seller info)
- Visual alerts for matches
- One-click resolution

#### Analytics Dashboard
- Total users count
- Citizens count
- Retailers count
- Registered phones count
- Total reports
- Snatched reports count
- Matched cases count
- Pending reports count
- Pending transfers count
- Total purchases count

#### Alert System
- Red alerts for IMEI matches
- Yellow alerts for pending transfers
- Direct navigation to relevant sections

### Technical Features

#### Frontend (Next.js + React)
- **Modern UI/UX**:
  - Animated components (fade-in, slide-up, scale-in)
  - Floating background elements
  - Gradient buttons with shadows
  - Hover effects on cards
  - Loading states with spinners
  - Toast notifications (success/error)

- **Responsive Design**:
  - Mobile-first approach
  - Grid layouts (1-4 columns)
  - Flexible cards
  - Adaptive navigation

- **Form Validation**:
  - Real-time CNIC validation (13 digits, numeric)
  - Real-time IMEI validation (15 digits, numeric)
  - Email validation
  - Password strength (min 8 characters)
  - Required field checking
  - Error messages with animations

- **Component Library**:
  - Button (5 variants: primary, secondary, danger, success, outline)
  - Input (with icons, labels, errors)
  - Card (with hover effects)
  - Badge (5 variants for different statuses)
  - Loading (spinner with message)
  - Modal dialogs

- **State Management**:
  - React hooks (useState, useEffect)
  - Context API for authentication
  - Local storage for tokens
  - Axios interceptors for API calls

#### Backend (FastAPI + Python)
- **RESTful API**:
  - 25+ endpoints
  - Automatic API documentation (Swagger)
  - JSON request/response
  - Proper HTTP status codes
  - Error handling with details

- **Database (NeonDB/PostgreSQL)**:
  - 5 main tables:
    - Users (with roles)
    - Phones (with status)
    - Reports (with matching)
    - Transfer Requests (with approval)
    - Retailer Purchases (with seller tracking)
  - Relationships and foreign keys
  - Indexes for performance
  - Automatic timestamps

- **Authentication System**:
  - JWT token generation
  - Token expiration (configurable)
  - Password hashing (bcrypt)
  - Role-based decorators
  - Protected endpoints

- **Business Logic**:
  - Automatic IMEI matching algorithm
  - Status cascade updates
  - Transfer approval workflow
  - Report verification system

#### Data Validation
- **CNIC Validation**:
  - Exactly 13 digits
  - Numeric only
  - Unique per user
  - Frontend + Backend validation

- **IMEI Validation**:
  - Exactly 15 digits
  - Numeric only
  - Unique per phone
  - Checked against snatched database

- **Email Validation**:
  - RFC compliant
  - Unique for users
  - Multiple allowed per phone

- **Password Validation**:
  - Minimum 8 characters
  - Hashed with bcrypt
  - Never stored in plain text

### User Experience Features

#### Landing Page
- Hero section with animated background
- Feature cards with icons
- Statistics section
- Call-to-action buttons
- Responsive footer

#### Dashboard Features
- Role-specific layouts
- Color-coded by role:
  - Citizen: Blue theme
  - Retailer: Green theme
  - Admin: Purple theme
- Tab-based navigation
- Modal forms for actions
- Inline editing where appropriate

#### Notifications
- Success messages (green)
- Error messages (red)
- Loading states
- 4-second auto-dismiss
- Custom styling

#### Error Handling
- User-friendly error messages
- Automatic logout on 401
- Form validation errors
- API error display
- Network error handling

### Security Best Practices

1. **Password Security**:
   - bcrypt hashing
   - No plain text storage
   - Minimum length requirement

2. **API Security**:
   - JWT tokens
   - HTTP-only best practices
   - Token expiration
   - Protected routes

3. **Input Validation**:
   - Frontend validation
   - Backend validation
   - SQL injection prevention
   - XSS prevention

4. **Role-Based Access**:
   - Middleware enforcement
   - Route protection
   - Action authorization

### Deployment Ready

- Environment variable configuration
- Production-ready code
- Scalable architecture
- Database migration support
- CORS configuration
- Error logging
- API documentation

### Future Enhancement Possibilities

- Email notifications
- SMS alerts
- QR code generation for phones
- Bulk phone registration
- Export reports to PDF
- Search and filter functionality
- Date range filtering
- Image upload for phones
- Multi-language support
- Mobile app version
- Push notifications
- Advanced analytics
- Integration with law enforcement databases

## 📊 System Flow Example

1. **Citizen** registers phone (iPhone 14, IMEI: 123456789012345)
2. Phone gets **snatched**, citizen reports it with culprit description
3. **System** marks phone status as "snatched", report status as "pending"
4. **Retailer** receives the same phone, registers it as received
5. **System automatically matches** IMEI 123456789012345
6. Report status changes to **"matched"**
7. **Admin** sees alert in dashboard
8. Admin views:
   - Original owner details
   - Culprit description
   - Retailer who received it
   - Seller CNIC
9. Admin can mark case as **cleared** after investigation

## 🎓 Learning Value

This project demonstrates:
- Full-stack development
- RESTful API design
- JWT authentication
- Role-based access control
- Database relationships
- Form validation
- State management
- Modern UI/UX
- Security best practices
- Production deployment

Perfect for portfolio, learning, or as a foundation for real-world deployment!
