# Metro Bank Web App - Setup Guide

## Overview

This is a Metro Bank web application with:
- OTP-based login authentication
- Transaction management (processing → pending → completed)
- Transfer money functionality
- Responsive dashboard

## Project Structure

```
mtro/
├── api/                    # Python backend
│   ├── send_otp.py         # OTP service
│   ├── transactions.py     # Transaction service
│   ├── requirements.txt   # Python dependencies
│   └── README.md          # API documentation
├── metro-bank-local/        # Frontend
│   ├── index.html         # Homepage
│   ├── login.html         # Login with OTP
│   ├── dashboard.html     # User dashboard
│   └── ...
└── SETUP.md               # This file
```

## Quick Start

### 1. Backend Setup (Python)

```bash
cd api
pip install -r requirements.txt

# Terminal 1: Run OTP service
python send_otp.py

# Terminal 2: Run Transactions service  
python transactions.py
```

### 2. Frontend Setup

1. Open `metro-bank-local/login.html` in a browser
2. Enter any customer number/username
3. Enter the OTP code (check console/terminal for the code in demo mode)
4. You'll be redirected to the dashboard

### 3. Testing the Flow

1. **Login**: Enter customer number → Receive OTP → Enter OTP → Login
2. **Transfer Money**: Click "Make a Payment" → Fill form → Submit
3. **Watch Transaction**: 
   - Starts as "Processing" (3-5 seconds)
   - Moves to "Pending"
   - Can be completed later

## API Configuration

Update the API base URL in:
- `metro-bank-local/login.html` (line ~716)
- `metro-bank-local/dashboard.html` (add API_BASE constant)

```javascript
// Local development
const API_BASE = 'http://localhost:5000';

// Production (after deploying to Vercel)
const API_BASE = 'https://your-app.vercel.app';
```

## Vercel Deployment

### Option 1: Python Serverless Functions

Vercel supports Python, but it's limited. Better options:

### Option 2: Separate Backend Deployment

1. Deploy Python backend to:
   - **Railway** (recommended - free tier)
   - **Render** (free tier)
   - **Heroku** (paid)
   - **PythonAnywhere** (free tier)

2. Update frontend API_BASE to point to deployed backend

3. Deploy frontend to Vercel:
   ```bash
   vercel --prod
   ```

## Email Service Setup

For production OTP emails, choose a service:

1. **SendGrid** (Recommended - 100 emails/day free)
   - Sign up at sendgrid.com
   - Get API key
   - Update `send_otp.py` to use SendGrid

2. **EmailJS** (200 emails/month free)
   - Good for simple use cases
   - Client-side email sending

3. **AWS SES** (62,000 emails/month free)
   - Best for scale
   - Requires AWS account setup

## Features Implemented

✅ OTP login flow
✅ Account type: Joint Account
✅ Transfer money functionality
✅ Transaction states: Processing → Pending
✅ Previous successful transactions display
✅ Responsive dashboard

## Next Steps

1. Integrate real email service for OTP
2. Add database (PostgreSQL/MongoDB) for persistence
3. Add authentication tokens (JWT)
4. Deploy backend to cloud service
5. Deploy frontend to Vercel

## Troubleshooting

**OTP not sending?**
- Check backend is running on port 5000
- Check browser console for errors
- In demo mode, OTP is logged to terminal

**Transactions not updating?**
- Ensure transactions.py is running on port 5001
- Check API_BASE URL in dashboard.html
- Check browser console for API errors

**CORS errors?**
- Backend has CORS enabled
- If issues persist, check Flask-CORS configuration

