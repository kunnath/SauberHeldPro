#!/usr/bin/env python3
"""
Generate completely fresh test credentials for testing registration
"""

import random
import string
import time

# Generate unique test data with timestamp
timestamp = int(time.time())
random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
test_email = f"test.celebration.{timestamp}.{random_suffix}@example.com"
test_first_name = "Test"
test_last_name = "Celebration"
test_password = "testpass123"
test_phone = "+1234567890"
test_address = "123 Test Street, Test City, TC 12345"

print("🧪 FRESH REGISTRATION TEST CREDENTIALS")
print("=" * 50)
print(f"📧 Email: {test_email}")
print(f"🔒 Password: {test_password}")
print(f"👤 First Name: {test_first_name}")
print(f"👤 Last Name: {test_last_name}")
print(f"📞 Phone: {test_phone}")
print(f"🏠 Address: {test_address}")
print("=" * 50)
print()
print("🎯 **TEST INSTRUCTIONS:**")
print("1. 🌐 Go to: http://localhost:8502")
print("2. 📝 Click on 'Register' tab")
print("3. ✍️  Fill out the form with the credentials above")
print("4. 🎬 Click 'Create Account' button")
print()
print("🎉 **EXPECTED CELEBRATION:**")
print("✅ 🎈 Balloons animation should appear")
print("✅ ❄️  Snow effect should play")
print("✅ 🎉 Multiple colorful success messages")
print("✅ 🌟 Beautiful gradient welcome banner")
print("✅ 📧 Your email should appear in the welcome message")
print("✅ 📋 Step-by-step next actions guide")
print("✅ 🔐 Prominent login button")
print()
print("📞 If celebration doesn't appear, check terminal output for errors!")
print("=" * 50)
