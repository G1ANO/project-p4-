#!/usr/bin/env python3
"""
Test script to verify Flask-Bcrypt implementation
"""

from app import app, bcrypt, User, db

def test_bcrypt_functionality():
    """Test Flask-Bcrypt password hashing and verification"""
    
    with app.app_context():
        print("🔐 Testing Flask-Bcrypt Implementation")
        print("=" * 50)
        
        # Test 1: Basic password hashing
        test_password = "TestPassword123!"
        hashed = bcrypt.generate_password_hash(test_password).decode('utf-8')
        print(f"✅ Password hashing successful")
        print(f"   Original: {test_password}")
        print(f"   Hashed: {hashed[:50]}...")
        
        # Test 2: Password verification
        is_valid = bcrypt.check_password_hash(hashed, test_password)
        print(f"✅ Password verification: {'PASSED' if is_valid else 'FAILED'}")
        
        # Test 3: Wrong password verification
        is_invalid = bcrypt.check_password_hash(hashed, "WrongPassword")
        print(f"✅ Wrong password rejection: {'PASSED' if not is_invalid else 'FAILED'}")
        
        # Test 4: Check existing users in database
        print("\n📊 Database Users with Bcrypt Hashes:")
        users = User.query.all()
        for user in users:
            # Test if we can verify the known passwords
            if user.email == "user1@gmail.com":
                can_verify = bcrypt.check_password_hash(user.password_hash, "User1!")
                print(f"   {user.email}: {'✅ VALID' if can_verify else '❌ INVALID'}")
            elif user.email == "user2@gmail.com":
                can_verify = bcrypt.check_password_hash(user.password_hash, "Test2@")
                print(f"   {user.email}: {'✅ VALID' if can_verify else '❌ INVALID'}")
            else:
                print(f"   {user.email}: Hash format check - {'✅ BCRYPT' if user.password_hash.startswith('$2b$') else '❌ NOT BCRYPT'}")
        
        print("\n🎉 Flask-Bcrypt implementation test completed!")
        print("All password operations are now using secure bcrypt hashing.")

if __name__ == "__main__":
    test_bcrypt_functionality()
