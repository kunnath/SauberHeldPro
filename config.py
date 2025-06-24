"""
Configuration settings for Aufraumenbee
"""

import os
from typing import Dict, Any

class Config:
    """Application configuration"""
    
    # Database settings
    DATABASE_NAME = os.getenv('DB_NAME', 'aufraumenbee.db')
    
    # Application settings
    APP_NAME = os.getenv('APP_NAME', 'Aufraumenbee')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'aufraumenbee_secret_key_2025')
    
    # Session settings
    SESSION_TIMEOUT_MINUTES = int(os.getenv('SESSION_TIMEOUT_MINUTES', '30'))
    
    # Business settings
    DEFAULT_TAX_RATE = float(os.getenv('DEFAULT_TAX_RATE', '10.0'))
    DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY', 'USD')
    BUSINESS_HOURS_START = os.getenv('BUSINESS_HOURS_START', '08:00')
    BUSINESS_HOURS_END = os.getenv('BUSINESS_HOURS_END', '18:00')
    
    # Notification settings
    ENABLE_EMAIL_NOTIFICATIONS = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'False').lower() == 'true'
    ENABLE_SMS_NOTIFICATIONS = os.getenv('ENABLE_SMS_NOTIFICATIONS', 'False').lower() == 'true'
    
    # Pagination settings
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', '10'))
    
    # File upload settings
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '5'))
    ALLOWED_FILE_TYPES = ['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx']
    
    # Service settings
    SERVICE_TYPES = [
        "Regular Cleaning",
        "Deep Cleaning",
        "Move-in/Move-out Cleaning",
        "Post-Construction Cleaning",
        "Office Cleaning",
        "Carpet Cleaning",
        "Window Cleaning",
        "Upholstery Cleaning",
        "Pressure Washing",
        "Organizing Services"
    ]
    
    JOB_STATUSES = [
        "pending",
        "approved", 
        "assigned",
        "in_progress",
        "completed",
        "cancelled"
    ]
    
    USER_ROLES = [
        "customer",
        "employee", 
        "manager",
        "admin"
    ]
    
    EMPLOYMENT_TYPES = [
        "permanent",
        "contract"
    ]
    
    # UI settings
    THEME_CONFIG = {
        'primaryColor': '#FF6B6B',
        'backgroundColor': '#FFFFFF',
        'secondaryBackgroundColor': '#F0F2F6',
        'textColor': '#262730'
    }
    
    # Map settings (for future GPS integration)
    MAP_DEFAULT_LAT = float(os.getenv('MAP_DEFAULT_LAT', '40.7128'))
    MAP_DEFAULT_LON = float(os.getenv('MAP_DEFAULT_LON', '-74.0060'))
    MAP_DEFAULT_ZOOM = int(os.getenv('MAP_DEFAULT_ZOOM', '10'))
    
    @classmethod
    def get_all_settings(cls) -> Dict[str, Any]:
        """Get all configuration settings"""
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('_') and not callable(value)
        }
    
    @classmethod
    def get_business_hours(cls) -> Dict[str, str]:
        """Get business hours"""
        return {
            'start': cls.BUSINESS_HOURS_START,
            'end': cls.BUSINESS_HOURS_END
        }
    
    @classmethod
    def is_business_hours(cls, time_str: str) -> bool:
        """Check if given time is within business hours"""
        from datetime import datetime
        
        try:
            time_obj = datetime.strptime(time_str, '%H:%M').time()
            start_time = datetime.strptime(cls.BUSINESS_HOURS_START, '%H:%M').time()
            end_time = datetime.strptime(cls.BUSINESS_HOURS_END, '%H:%M').time()
            
            return start_time <= time_obj <= end_time
        except:
            return False

# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    DATABASE_NAME = 'aufraumenbee_dev.db'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    DATABASE_NAME = 'aufraumenbee_prod.db'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    DATABASE_NAME = ':memory:'  # In-memory database for testing

# Configuration factory
def get_config() -> Config:
    """Get configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()
