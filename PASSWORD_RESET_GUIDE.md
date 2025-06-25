# 🔐 Password Reset Feature - User Guide

## Overview
The Aufraumenbee customer portal now includes a comprehensive password reset feature that allows customers to securely reset their passwords when they forget them.

## Features ✨

### 🌍 **Multilingual Support**
- Available in both English and German
- Seamless language switching
- Localized messages and instructions

### 🔒 **Security Features**
- 6-digit verification codes
- 15-minute expiration time
- One-time use codes
- Secure password hashing
- Automatic cleanup of expired codes

### 📱 **User-Friendly Interface**
- Simple 2-step process
- Clear instructions
- Real-time validation
- Visual feedback and success animations

## How to Use 🚀

### **Step 1: Access Password Reset**
1. Go to the Customer Portal: `http://localhost:8503`
2. On the login page, click **"🔑 Forgot Password?"**
3. You'll be taken to the password reset form

### **Step 2: Request Reset Code**
1. Enter your registered email address
2. Click **"Send Reset Code"**
3. A 6-digit code will be generated (displayed on screen for demo)
4. You'll see a success message confirming the code was sent

### **Step 3: Reset Your Password**
1. Enter the 6-digit reset code you received
2. Enter your new password (minimum 6 characters)
3. Confirm your new password
4. Click **"Reset Password"**
5. Success! You can now login with your new password

## Demo Instructions 🧪

### **Test Account**
- **Email**: `test.reset@aufraumenbee.com`
- **Current Password**: `newpassword456`

### **Full Demo Flow**
1. **Forget Password Simulation**:
   - Go to login page
   - Click "Forgot Password?"
   - Enter: `test.reset@aufraumenbee.com`
   - Click "Send Reset Code"

2. **Reset Code Entry**:
   - A 6-digit code will be displayed (demo mode)
   - Enter the displayed code
   - Set new password: `mynewpassword123`
   - Confirm password and submit

3. **Login with New Password**:
   - Click "Back to Login" or wait for automatic redirect
   - Login with email and new password

## Technical Details ⚙️

### **Database Tables**

#### **password_reset_codes**
```sql
CREATE TABLE password_reset_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    reset_code TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE
);
```

### **Security Measures**
- **Code Expiration**: 15 minutes from generation
- **One-time Use**: Codes are marked as used after successful reset
- **Email Validation**: Only registered emails can request codes
- **Password Validation**: Minimum 6 characters required
- **Automatic Cleanup**: Expired codes are automatically removed

### **Translations Available**

#### **English**
- `forgot_password`: "Forgot Password?"
- `reset_password`: "Reset Password"
- `reset_password_title`: "Reset Your Password"
- `send_reset_code`: "Send Reset Code"
- `reset_code_sent`: "A reset code has been sent to your email address."
- `password_reset_success`: "Password reset successful! You can now login with your new password."
- `back_to_login`: "Back to Login"

#### **German**
- `forgot_password`: "Passwort vergessen?"
- `reset_password`: "Passwort zurücksetzen"
- `reset_password_title`: "Ihr Passwort zurücksetzen"
- `send_reset_code`: "Reset-Code senden"
- `reset_code_sent`: "Ein Reset-Code wurde an Ihre E-Mail-Adresse gesendet."
- `password_reset_success`: "Passwort erfolgreich zurückgesetzt! Sie können sich jetzt mit Ihrem neuen Passwort anmelden."
- `back_to_login`: "Zurück zur Anmeldung"

## Error Handling 🚨

### **Common Error Messages**
- **Invalid Email**: "Please enter a valid email address."
- **Email Not Found**: System shows generic message for security
- **Invalid Reset Code**: "Invalid reset code. Please check and try again."
- **Code Expired**: "Reset code has expired. Please request a new one."
- **Password Mismatch**: "Passwords do not match."
- **Password Too Short**: "Password must be at least 6 characters long."

### **Error Resolution**
1. **Code Not Working**: Request a new reset code
2. **Code Expired**: Start the process again
3. **Email Issues**: Verify email spelling and registration
4. **Password Issues**: Ensure passwords match and meet requirements

## Testing Tools 🧪

### **Automated Testing**
```bash
python test_password_reset.py
```

### **Manual Testing Steps**
1. Create test customer
2. Request password reset
3. Use reset code
4. Verify new password works
5. Verify old password rejected

### **Database Inspection**
```bash
python db_viewer.py users
```

## Troubleshooting 🔧

### **Reset Not Working**
1. Check if customer email is registered
2. Verify reset code hasn't expired
3. Ensure database has password_reset_codes table
4. Check for any JavaScript console errors

### **Database Issues**
```bash
# Reset database if needed
python migrate_db.py
python init_sample_data.py
```

### **Portal Access Issues**
```bash
# Restart customer portal
pkill -f streamlit.*customer_portal
streamlit run customer_portal_multilingual.py --server.port 8503
```

## Future Enhancements 🚀

### **Planned Features**
- **Email Integration**: Send actual emails via SMTP
- **SMS Verification**: Alternative verification method
- **Account Lockout**: Prevent brute force attacks
- **Password Strength Meter**: Visual password strength indicator
- **Security Questions**: Additional verification method

### **Security Improvements**
- **Rate Limiting**: Limit reset requests per hour
- **IP Tracking**: Monitor suspicious activity
- **Audit Logging**: Track all password reset attempts
- **2FA Integration**: Two-factor authentication support

---

## Summary ✅

The password reset feature is now fully functional with:
- ✅ Multilingual support (English/German)
- ✅ Secure 6-digit verification codes
- ✅ 15-minute expiration for security
- ✅ User-friendly 2-step process
- ✅ Comprehensive error handling
- ✅ Automated testing suite
- ✅ Database integration
- ✅ Session state management

**Ready for production use!** 🎉

The feature seamlessly integrates with the existing customer portal and provides a secure, user-friendly way for customers to regain access to their accounts.
