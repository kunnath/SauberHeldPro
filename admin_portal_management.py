"""
Admin interface for managing time slots and services for the customer portal
This extends the main app.py with slot management features
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
from typing import List, Dict

def init_admin_database():
    """Initialize database connection for admin operations"""
    return sqlite3.connect('aufraumenbee.db', check_same_thread=False)

def add_slot_management_to_main_app():
    """Add slot management functions to the main admin interface"""
    
    def show_slot_management():
        """Show time slot management interface"""
        st.subheader("📅 Time Slot Management")
        
        tab1, tab2, tab3 = st.tabs(["View Slots", "Add Slots", "Manage Bookings"])
        
        with tab1:
            show_existing_slots()
        
        with tab2:
            show_add_slots_form()
            
        with tab3:
            show_customer_bookings_admin()
    
    def show_existing_slots():
        """Show existing time slots"""
        st.markdown("### Current Time Slots")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From Date", value=date.today())
        with col2:
            end_date = st.date_input("To Date", value=date.today() + timedelta(days=14))
        
        if start_date <= end_date:
            conn = init_admin_database()
            
            query = '''
                SELECT ts.id, ts.date, ts.start_time, ts.end_time, 
                       ts.current_bookings, ts.max_bookings, ts.available,
                       e.name as employee_name
                FROM time_slots ts
                LEFT JOIN employees e ON ts.employee_id = e.id
                WHERE ts.date BETWEEN ? AND ?
                ORDER BY ts.date, ts.start_time
            '''
            
            df = pd.read_sql_query(query, conn, params=(start_date, end_date))
            conn.close()
            
            if not df.empty:
                # Add status column
                df['status'] = df.apply(lambda row: 
                    'Full' if row['current_bookings'] >= row['max_bookings'] 
                    else f"{row['current_bookings']}/{row['max_bookings']}", axis=1)
                
                df['available_status'] = df['available'].apply(lambda x: '✅ Active' if x else '❌ Inactive')
                
                # Display with better formatting
                display_df = df[['date', 'start_time', 'end_time', 'status', 'available_status', 'employee_name']].copy()
                display_df.columns = ['Date', 'Start Time', 'End Time', 'Bookings', 'Status', 'Assigned Employee']
                
                st.dataframe(display_df, use_container_width=True)
                
                # Bulk actions
                st.markdown("### Bulk Actions")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Deactivate All Slots in Range"):
                        update_slots_status(start_date, end_date, False)
                        st.success("Slots deactivated!")
                        st.rerun()
                
                with col2:
                    if st.button("Activate All Slots in Range"):
                        update_slots_status(start_date, end_date, True)
                        st.success("Slots activated!")
                        st.rerun()
                        
                with col3:
                    if st.button("Delete Empty Slots in Range"):
                        delete_empty_slots(start_date, end_date)
                        st.success("Empty slots deleted!")
                        st.rerun()
            else:
                st.info("No time slots found for the selected date range.")
        else:
            st.error("End date must be after start date.")
    
    def show_add_slots_form():
        """Show form to add new time slots"""
        st.markdown("### Add New Time Slots")
        
        with st.form("add_slots_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                slot_date = st.date_input(
                    "Date",
                    value=date.today() + timedelta(days=1),
                    min_value=date.today()
                )
                start_time = st.time_input("Start Time", value=datetime.strptime("09:00", "%H:%M").time())
                max_bookings = st.number_input("Max Bookings per Slot", min_value=1, max_value=5, value=1)
            
            with col2:
                # Get employees for assignment
                conn = init_admin_database()
                employees_df = pd.read_sql_query("SELECT id, name FROM employees", conn)
                conn.close()
                
                if not employees_df.empty:
                    employee_options = ["No Assignment"] + employees_df['name'].tolist()
                    employee_names_to_ids = dict(zip(employees_df['name'], employees_df['id']))
                    
                    selected_employee = st.selectbox("Assign Employee (Optional)", employee_options)
                    employee_id = employee_names_to_ids.get(selected_employee, None)
                else:
                    st.info("No employees found. Add employees first.")
                    employee_id = None
                
                end_time = st.time_input("End Time", value=datetime.strptime("11:00", "%H:%M").time())
                
            # Bulk creation options
            st.markdown("### Bulk Creation Options")
            
            col1, col2 = st.columns(2)
            with col1:
                create_multiple_days = st.checkbox("Create for multiple days")
                if create_multiple_days:
                    num_days = st.number_input("Number of days", min_value=1, max_value=30, value=7)
            
            with col2:
                create_recurring = st.checkbox("Create recurring weekly slots")
                if create_recurring:
                    num_weeks = st.number_input("Number of weeks", min_value=1, max_value=12, value=4)
            
            submitted = st.form_submit_button("Create Time Slots")
            
            if submitted:
                if start_time >= end_time:
                    st.error("End time must be after start time.")
                    return
                
                dates_to_create = [slot_date]
                
                # Handle multiple days
                if create_multiple_days:
                    dates_to_create = [slot_date + timedelta(days=i) for i in range(num_days)]
                
                # Handle recurring
                if create_recurring:
                    recurring_dates = []
                    for week in range(num_weeks):
                        week_offset = timedelta(weeks=week)
                        if create_multiple_days:
                            for day_offset in range(num_days):
                                recurring_dates.append(slot_date + week_offset + timedelta(days=day_offset))
                        else:
                            recurring_dates.append(slot_date + week_offset)
                    dates_to_create = recurring_dates
                
                # Create slots
                success_count = 0
                for create_date in dates_to_create:
                    if create_time_slot(create_date, start_time.strftime("%H:%M"), 
                                      end_time.strftime("%H:%M"), max_bookings, employee_id):
                        success_count += 1
                
                st.success(f"Created {success_count} time slots successfully!")
                if success_count < len(dates_to_create):
                    st.warning(f"{len(dates_to_create) - success_count} slots were not created (may already exist).")
    
    def show_customer_bookings_admin():
        """Show customer bookings for admin management"""
        st.markdown("### Customer Bookings Management")
        
        conn = init_admin_database()
        
        query = '''
            SELECT cb.id, cu.first_name, cu.last_name, cu.email,
                   st.name as service_name, cb.date, cb.start_time, cb.end_time,
                   cb.address, cb.total_price, cb.status, cb.created_at
            FROM customer_bookings cb
            JOIN customer_users cu ON cb.customer_user_id = cu.id
            JOIN service_types st ON cb.service_type_id = st.id
            ORDER BY cb.date DESC, cb.start_time DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All"] + df['status'].unique().tolist())
            
            with col2:
                date_filter = st.date_input("Filter by Date (Optional)")
            
            with col3:
                service_filter = st.selectbox("Filter by Service", ["All"] + df['service_name'].unique().tolist())
            
            # Apply filters
            filtered_df = df.copy()
            
            if status_filter != "All":
                filtered_df = filtered_df[filtered_df['status'] == status_filter]
            
            if date_filter:
                filtered_df = filtered_df[filtered_df['date'] == date_filter.strftime('%Y-%m-%d')]
            
            if service_filter != "All":
                filtered_df = filtered_df[filtered_df['service_name'] == service_filter]
            
            # Display bookings
            for _, booking in filtered_df.iterrows():
                with st.expander(f"{booking['first_name']} {booking['last_name']} - {booking['service_name']} - {booking['date']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Customer:** {booking['first_name']} {booking['last_name']}")
                        st.write(f"**Email:** {booking['email']}")
                        st.write(f"**Service:** {booking['service_name']}")
                        st.write(f"**Date:** {booking['date']}")
                        st.write(f"**Time:** {booking['start_time']} - {booking['end_time']}")
                    
                    with col2:
                        st.write(f"**Address:** {booking['address']}")
                        st.write(f"**Price:** ${booking['total_price']}")
                        st.write(f"**Status:** {booking['status']}")
                        st.write(f"**Booked:** {booking['created_at']}")
                    
                    # Status update buttons
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button("Confirm", key=f"confirm_{booking['id']}"):
                            update_booking_status(booking['id'], 'confirmed')
                            st.success("Booking confirmed!")
                            st.rerun()
                    
                    with col2:
                        if st.button("Complete", key=f"complete_{booking['id']}"):
                            update_booking_status(booking['id'], 'completed')
                            st.success("Booking marked as completed!")
                            st.rerun()
                    
                    with col3:
                        if st.button("Cancel", key=f"cancel_{booking['id']}"):
                            update_booking_status(booking['id'], 'cancelled')
                            st.warning("Booking cancelled!")
                            st.rerun()
                    
                    with col4:
                        if st.button("Delete", key=f"delete_{booking['id']}"):
                            delete_booking(booking['id'])
                            st.error("Booking deleted!")
                            st.rerun()
        else:
            st.info("No customer bookings found.")
    
    def create_time_slot(slot_date: date, start_time: str, end_time: str, 
                        max_bookings: int, employee_id: int = None) -> bool:
        """Create a new time slot"""
        conn = init_admin_database()
        try:
            conn.execute('''
                INSERT INTO time_slots (date, start_time, end_time, max_bookings, employee_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (slot_date.strftime('%Y-%m-%d'), start_time, end_time, max_bookings, employee_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def update_slots_status(start_date: date, end_date: date, available: bool):
        """Update availability status for slots in date range"""
        conn = init_admin_database()
        conn.execute('''
            UPDATE time_slots 
            SET available = ?
            WHERE date BETWEEN ? AND ?
        ''', (available, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
    
    def delete_empty_slots(start_date: date, end_date: date):
        """Delete empty slots in date range"""
        conn = init_admin_database()
        conn.execute('''
            DELETE FROM time_slots 
            WHERE date BETWEEN ? AND ? AND current_bookings = 0
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
    
    def update_booking_status(booking_id: int, status: str):
        """Update booking status"""
        conn = init_admin_database()
        conn.execute('''
            UPDATE customer_bookings 
            SET status = ?
            WHERE id = ?
        ''', (status, booking_id))
        conn.commit()
        conn.close()
    
    def delete_booking(booking_id: int):
        """Delete a booking and update slot availability"""
        conn = init_admin_database()
        
        # Get slot_id before deleting booking
        cursor = conn.execute('SELECT slot_id FROM customer_bookings WHERE id = ?', (booking_id,))
        result = cursor.fetchone()
        
        if result:
            slot_id = result[0]
            
            # Delete booking
            conn.execute('DELETE FROM customer_bookings WHERE id = ?', (booking_id,))
            
            # Update slot booking count
            conn.execute('''
                UPDATE time_slots 
                SET current_bookings = current_bookings - 1
                WHERE id = ? AND current_bookings > 0
            ''', (slot_id,))
            
            conn.commit()
        
        conn.close()
    
    def show_service_management():
        """Show service management interface"""
        st.subheader("🧹 Service Management")
        
        tab1, tab2 = st.tabs(["View Services", "Add/Edit Services"])
        
        with tab1:
            show_existing_services()
        
        with tab2:
            show_service_form()
    
    def show_existing_services():
        """Show existing services"""
        conn = init_admin_database()
        df = pd.read_sql_query('''
            SELECT id, name, description, base_price, duration_minutes, category, active
            FROM service_types
            ORDER BY category, name
        ''', conn)
        conn.close()
        
        if not df.empty:
            # Group by category
            for category in df['category'].unique():
                st.markdown(f"### {category} Services")
                category_df = df[df['category'] == category]
                
                for _, service in category_df.iterrows():
                    with st.expander(f"{service['name']} - ${service['base_price']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Description:** {service['description']}")
                            st.write(f"**Duration:** {service['duration_minutes']} minutes")
                            st.write(f"**Category:** {service['category']}")
                        
                        with col2:
                            st.write(f"**Price:** ${service['base_price']}")
                            status = "Active" if service['active'] else "Inactive"
                            st.write(f"**Status:** {status}")
                        
                        # Action buttons
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if service['active']:
                                if st.button("Deactivate", key=f"deactivate_{service['id']}"):
                                    update_service_status(service['id'], False)
                                    st.success("Service deactivated!")
                                    st.rerun()
                            else:
                                if st.button("Activate", key=f"activate_{service['id']}"):
                                    update_service_status(service['id'], True)
                                    st.success("Service activated!")
                                    st.rerun()
                        
                        with col2:
                            if st.button("Edit", key=f"edit_{service['id']}"):
                                st.session_state.edit_service_id = service['id']
                                st.rerun()
                        
                        with col3:
                            if st.button("Delete", key=f"delete_{service['id']}"):
                                delete_service(service['id'])
                                st.error("Service deleted!")
                                st.rerun()
        else:
            st.info("No services found.")
    
    def show_service_form():
        """Show form to add/edit services"""
        edit_mode = 'edit_service_id' in st.session_state
        
        if edit_mode:
            st.markdown("### Edit Service")
            service_id = st.session_state.edit_service_id
            
            # Get existing service data
            conn = init_admin_database()
            cursor = conn.execute('''
                SELECT name, description, base_price, duration_minutes, category
                FROM service_types WHERE id = ?
            ''', (service_id,))
            service_data = cursor.fetchone()
            conn.close()
            
            if not service_data:
                st.error("Service not found!")
                del st.session_state.edit_service_id
                st.rerun()
                return
        else:
            st.markdown("### Add New Service")
            service_data = None
        
        with st.form("service_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    "Service Name",
                    value=service_data[0] if service_data else ""
                )
                base_price = st.number_input(
                    "Base Price ($)",
                    min_value=0.0,
                    value=float(service_data[2]) if service_data else 50.0,
                    step=5.0
                )
                category = st.selectbox(
                    "Category",
                    ["Residential", "Commercial", "Specialty"],
                    index=["Residential", "Commercial", "Specialty"].index(service_data[4]) if service_data else 0
                )
            
            with col2:
                duration_minutes = st.number_input(
                    "Duration (minutes)",
                    min_value=30,
                    max_value=480,
                    value=service_data[3] if service_data else 120,
                    step=30
                )
                
            description = st.text_area(
                "Description",
                value=service_data[1] if service_data else "",
                placeholder="Describe what this service includes..."
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                submitted = st.form_submit_button(
                    "Update Service" if edit_mode else "Add Service",
                    use_container_width=True
                )
            
            with col2:
                if edit_mode:
                    if st.form_submit_button("Cancel Edit", use_container_width=True):
                        del st.session_state.edit_service_id
                        st.rerun()
            
            if submitted:
                if not all([name, description, base_price, duration_minutes]):
                    st.error("Please fill in all fields.")
                    return
                
                if edit_mode:
                    if update_service(service_id, name, description, base_price, duration_minutes, category):
                        st.success("Service updated successfully!")
                        del st.session_state.edit_service_id
                        st.rerun()
                    else:
                        st.error("Failed to update service.")
                else:
                    if create_service(name, description, base_price, duration_minutes, category):
                        st.success("Service created successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to create service. Service name may already exist.")
    
    def create_service(name: str, description: str, base_price: float, 
                      duration_minutes: int, category: str) -> bool:
        """Create a new service"""
        conn = init_admin_database()
        try:
            conn.execute('''
                INSERT INTO service_types (name, description, base_price, duration_minutes, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, description, base_price, duration_minutes, category))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def update_service(service_id: int, name: str, description: str, 
                      base_price: float, duration_minutes: int, category: str) -> bool:
        """Update an existing service"""
        conn = init_admin_database()
        try:
            conn.execute('''
                UPDATE service_types 
                SET name = ?, description = ?, base_price = ?, duration_minutes = ?, category = ?
                WHERE id = ?
            ''', (name, description, base_price, duration_minutes, category, service_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def update_service_status(service_id: int, active: bool):
        """Update service active status"""
        conn = init_admin_database()
        conn.execute('UPDATE service_types SET active = ? WHERE id = ?', (active, service_id))
        conn.commit()
        conn.close()
    
    def delete_service(service_id: int):
        """Delete a service"""
        conn = init_admin_database()
        conn.execute('DELETE FROM service_types WHERE id = ?', (service_id,))
        conn.commit()
        conn.close()
    
    # Return the functions to be added to main app
    return {
        'show_slot_management': show_slot_management,
        'show_service_management': show_service_management
    }

# This would be integrated into the main app.py navigation
def add_customer_portal_management():
    """Add customer portal management to main app navigation"""
    functions = add_slot_management_to_main_app()
    
    # These would be added as new menu items in the main app
    st.sidebar.markdown("### Customer Portal Management")
    
    if st.sidebar.button("Manage Time Slots"):
        functions['show_slot_management']()
    
    if st.sidebar.button("Manage Services"):
        functions['show_service_management']()

if __name__ == "__main__":
    st.title("Admin - Customer Portal Management")
    functions = add_slot_management_to_main_app()
    
    menu = st.selectbox("Select Management Area", ["Time Slots", "Services"])
    
    if menu == "Time Slots":
        functions['show_slot_management']()
    elif menu == "Services":
        functions['show_service_management']()
