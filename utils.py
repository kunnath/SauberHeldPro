"""
Utility functions for Aufraumenbee cleaning service management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import uuid

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"

def format_date(date_str: str) -> str:
    """Format date string for display"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str

def format_time(time_str: str) -> str:
    """Format time string for display"""
    try:
        time_obj = datetime.strptime(time_str, '%H:%M')
        return time_obj.strftime('%I:%M %p')
    except:
        return time_str

def get_status_color(status: str) -> str:
    """Get color for job status"""
    colors = {
        'pending': '🟡',
        'approved': '🟠',
        'assigned': '🔵',
        'in_progress': '🟣',
        'completed': '🟢',
        'cancelled': '🔴'
    }
    return colors.get(status, '⚪')

def get_priority_color(priority: str) -> str:
    """Get color for priority level"""
    colors = {
        'low': '🟢',
        'medium': '🟡',
        'high': '🟠',
        'urgent': '🔴'
    }
    return colors.get(priority, '⚪')

def calculate_job_duration(start_time: str, end_time: str) -> int:
    """Calculate job duration in minutes"""
    try:
        start = datetime.strptime(start_time, '%H:%M')
        end = datetime.strptime(end_time, '%H:%M')
        
        # Handle next day scenarios
        if end < start:
            end += timedelta(days=1)
        
        duration = (end - start).total_seconds() / 60
        return int(duration)
    except:
        return 0

def generate_invoice_number() -> str:
    """Generate unique invoice number"""
    now = datetime.now()
    return f"INV-{now.strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates (simplified)"""
    # This is a simplified calculation - in production, use proper geolocation API
    import math
    
    R = 6371  # Earth's radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat/2) * math.sin(dlat/2) + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon/2) * math.sin(dlon/2))
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    return distance

def create_revenue_chart(df: pd.DataFrame) -> go.Figure:
    """Create revenue chart"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          x=0.5, y=0.5, 
                          xref="paper", yref="paper",
                          showarrow=False)
        return fig
    
    fig = px.line(df, x='month', y='revenue', 
                  title='Monthly Revenue Trend',
                  markers=True)
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        hovermode='x unified'
    )
    
    return fig

def create_job_status_chart(df: pd.DataFrame) -> go.Figure:
    """Create job status distribution chart"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          x=0.5, y=0.5, 
                          xref="paper", yref="paper",
                          showarrow=False)
        return fig
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
    
    fig = px.pie(df, values='count', names='status',
                 title='Job Status Distribution',
                 color_discrete_sequence=colors)
    
    return fig

def create_employee_performance_chart(df: pd.DataFrame) -> go.Figure:
    """Create employee performance chart"""
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          x=0.5, y=0.5, 
                          xref="paper", yref="paper",
                          showarrow=False)
        return fig
    
    fig = px.bar(df, x='employee_name', y='completed_jobs',
                 title='Employee Performance - Completed Jobs',
                 color='completed_jobs',
                 color_continuous_scale='Blues')
    
    fig.update_layout(
        xaxis_title="Employee",
        yaxis_title="Completed Jobs",
        showlegend=False
    )
    
    return fig

def send_notification(user_id: int, message: str, notification_type: str = 'info'):
    """Send notification to user (placeholder for future implementation)"""
    # This would integrate with email, SMS, or push notification service
    # For now, just log the notification
    print(f"Notification [{notification_type}] for user {user_id}: {message}")

def export_to_csv(df: pd.DataFrame, filename: str) -> bytes:
    """Export dataframe to CSV"""
    return df.to_csv(index=False).encode('utf-8')

def export_to_excel(df: pd.DataFrame, filename: str) -> bytes:
    """Export dataframe to Excel"""
    import io
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    return output.getvalue()

def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    import re
    # Simple US phone number validation
    pattern = r'^\d{3}-\d{3}-\d{4}$|^\(\d{3}\)\s\d{3}-\d{4}$|^\d{10}$'
    return re.match(pattern, phone) is not None

def get_service_types() -> List[str]:
    """Get list of available service types"""
    return [
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

def get_employee_skills() -> List[str]:
    """Get list of employee skills"""
    return [
        "Residential Cleaning",
        "Commercial Cleaning",
        "Deep Cleaning",
        "Carpet Cleaning",
        "Window Cleaning",
        "Pressure Washing",
        "Move-out Cleaning",
        "Post-Construction",
        "Green Cleaning",
        "Pet-Safe Products"
    ]

def calculate_job_price(service_type: str, duration: int, location_type: str = "residential") -> float:
    """Calculate estimated job price based on service type and duration"""
    base_rates = {
        "Regular Cleaning": 30.0,
        "Deep Cleaning": 45.0,
        "Move-in/Move-out Cleaning": 40.0,
        "Post-Construction Cleaning": 50.0,
        "Office Cleaning": 35.0,
        "Carpet Cleaning": 25.0,
        "Window Cleaning": 20.0,
        "Upholstery Cleaning": 30.0,
        "Pressure Washing": 35.0,
        "Organizing Services": 40.0
    }
    
    base_rate = base_rates.get(service_type, 30.0)
    
    # Location multiplier
    location_multiplier = 1.2 if location_type == "commercial" else 1.0
    
    # Calculate price based on duration (in hours)
    hours = duration / 60
    estimated_price = base_rate * hours * location_multiplier
    
    return round(estimated_price, 2)

class NotificationManager:
    """Manage notifications and alerts"""
    
    @staticmethod
    def show_success(message: str):
        st.success(f"✅ {message}")
    
    @staticmethod
    def show_error(message: str):
        st.error(f"❌ {message}")
    
    @staticmethod
    def show_warning(message: str):
        st.warning(f"⚠️ {message}")
    
    @staticmethod
    def show_info(message: str):
        st.info(f"ℹ️ {message}")

class DataValidator:
    """Validate data inputs"""
    
    @staticmethod
    def validate_required_fields(data: Dict, required_fields: List[str]) -> bool:
        """Check if all required fields are provided"""
        return all(data.get(field) for field in required_fields)
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> bool:
        """Validate date range"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            return start <= end
        except:
            return False
    
    @staticmethod
    def validate_positive_number(value: float) -> bool:
        """Validate positive number"""
        return value > 0
