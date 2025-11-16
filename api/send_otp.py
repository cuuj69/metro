from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# In-memory storage for OTPs (in production, use Redis or database)
otp_storage = {}

# Simple email sending simulation (replace with actual email service)
def send_email(to_email, otp_code):
    """
    Simulate sending email with OTP
    In production, use services like:
    - SendGrid (free tier: 100 emails/day)
    - Mailgun (free tier: 5,000 emails/month)
    - AWS SES (free tier: 62,000 emails/month)
    - EmailJS (free tier: 200 emails/month)
    """
    # For demo purposes, we'll just log it
    print(f"[EMAIL] Sending OTP to {to_email}: {otp_code}")
    # In production, integrate with email service here
    return True

@app.route('/api/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.json
        email = data.get('email') or data.get('customerNumber')
        
        if not email:
            return jsonify({'error': 'Email or customer number required'}), 400
        
        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        
        # Store OTP with expiration (5 minutes)
        otp_storage[email] = {
            'otp': otp_code,
            'expires_at': (datetime.now() + timedelta(minutes=5)).isoformat(),
            'attempts': 0
        }
        
        # Send email
        send_email(email, otp_code)
        
        return jsonify({
            'success': True,
            'message': 'OTP sent to email',
            'otp': otp_code  # Remove this in production - only for testing
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.json
        email = data.get('email') or data.get('customerNumber')
        otp = data.get('otp')
        
        if not email or not otp:
            return jsonify({'error': 'Email and OTP required'}), 400
        
        stored_otp_data = otp_storage.get(email)
        
        if not stored_otp_data:
            return jsonify({'error': 'OTP not found or expired'}), 404
        
        # Check expiration
        expires_at = datetime.fromisoformat(stored_otp_data['expires_at'])
        if datetime.now() > expires_at:
            del otp_storage[email]
            return jsonify({'error': 'OTP expired'}), 400
        
        # Check attempts (max 3)
        if stored_otp_data['attempts'] >= 3:
            del otp_storage[email]
            return jsonify({'error': 'Too many attempts'}), 400
        
        # Verify OTP
        if stored_otp_data['otp'] == otp:
            # Clean up
            del otp_storage[email]
            return jsonify({
                'success': True,
                'message': 'OTP verified successfully'
            }), 200
        else:
            stored_otp_data['attempts'] += 1
            return jsonify({'error': 'Invalid OTP'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

