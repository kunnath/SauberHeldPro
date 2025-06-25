"""
Internationalization (i18n) System for Aufraumenbee
Supports multiple languages with easy expansion capability
"""

import streamlit as st
from typing import Dict, Any

class TranslationManager:
    """Manages translations for the Aufraumenbee application"""
    
    def __init__(self):
        self.translations = {
            'en': {
                # Common
                'app_name': 'Aufraumenbee',
                'tagline': 'Professional Cleaning Services',
                'welcome': 'Welcome',
                'login': 'Login',
                'logout': 'Logout',
                'register': 'Register',
                'email': 'Email',
                'password': 'Password',
                'confirm_password': 'Confirm Password',
                'first_name': 'First Name',
                'last_name': 'Last Name',
                'phone': 'Phone',
                'address': 'Address',
                'save': 'Save',
                'cancel': 'Cancel',
                'submit': 'Submit',
                'delete': 'Delete',
                'edit': 'Edit',
                'view': 'View',
                'search': 'Search',
                'loading': 'Loading...',
                'success': 'Success',
                'error': 'Error',
                'warning': 'Warning',
                'info': 'Information',
                
                # Navigation
                'dashboard': 'Dashboard',
                'customer_management': 'Customer Management',
                'employee_management': 'Employee Management',
                'job_management': 'Job Management',
                'booking_requests': 'Booking Requests',
                'scheduling': 'Scheduling',
                'invoicing': 'Invoicing',
                'inventory_management': 'Inventory Management',
                'analytics': 'Analytics',
                'settings': 'Settings',
                
                # Customer Portal
                'book_cleaning': 'Book Cleaning Services',
                'my_bookings': 'My Bookings',
                'service_history': 'Service History',
                'account_settings': 'Account Settings',
                'create_account': 'Create Your Account',
                'already_have_account': 'Already have an account?',
                'dont_have_account': "Don't have an account?",
                'sign_up_here': 'Sign up here',
                'login_here': 'Login here',
                
                # Services
                'basic_cleaning': 'Basic Cleaning',
                'deep_cleaning': 'Deep Cleaning',
                'office_cleaning': 'Office Cleaning',
                'window_cleaning': 'Window Cleaning',
                'carpet_cleaning': 'Carpet Cleaning',
                'move_in_out': 'Move-in/Move-out Cleaning',
                
                # Forms
                'required_field': 'Required field',
                'optional_field': 'Optional field',
                'choose_date': 'Choose Date',
                'choose_time': 'Choose Time',
                'service_type': 'Service Type',
                'special_instructions': 'Special Instructions',
                'contact_info': 'Contact Information',
                'booking_summary': 'Booking Summary',
                
                # Messages
                'login_success': 'Login successful! Welcome back.',
                'login_failed': 'Login failed. Please check your credentials.',
                'registration_success': 'Registration successful! Welcome to Aufraumenbee!',
                'registration_failed': 'Registration failed. Please try again.',
                'booking_success': 'Booking submitted successfully!',
                'booking_failed': 'Booking failed. Please try again.',
                'invalid_email': 'Please enter a valid email address.',
                'password_mismatch': 'Passwords do not match.',
                'password_too_short': 'Password must be at least 6 characters long.',
                'required_fields_missing': 'Please fill in all required fields.',
                
                # Password Reset
                'forgot_password': 'Forgot Password?',
                'reset_password': 'Reset Password',
                'reset_password_title': 'Reset Your Password',
                'reset_instructions': 'Enter your email address and we will help you reset your password.',
                'send_reset_code': 'Send Reset Code',
                'reset_code': 'Reset Code',
                'reset_code_sent': 'A reset code has been sent to your email address.',
                'reset_code_instructions': 'Check your email for the reset code and enter it below along with your new password.',
                'new_password': 'New Password',
                'confirm_new_password': 'Confirm New Password',
                'password_reset_success': 'Password reset successful! You can now login with your new password.',
                'password_reset_failed': 'Password reset failed. Please check your reset code and try again.',
                'invalid_reset_code': 'Invalid reset code. Please check and try again.',
                'reset_code_expired': 'Reset code has expired. Please request a new one.',
                'back_to_login': 'Back to Login',
                'enter_reset_code': 'Enter the 6-digit code sent to your email',
                
                'booked_on': 'Booked on',
                'no_bookings_yet': 'No bookings yet. Book your first cleaning service!',
                'booking_details': 'Booking Details',
                'book_now': 'Book Now',
                'address_required': 'Address is required',
                'special_instructions_placeholder': 'Any special requirements or instructions...',
                
                # Dashboard
                'total_customers': 'Total Customers',
                'total_employees': 'Total Employees',
                'pending_jobs': 'Pending Jobs',
                'revenue_this_month': 'Revenue This Month',
                'recent_bookings': 'Recent Bookings',
                'upcoming_jobs': 'Upcoming Jobs',
                
                # Customer Management
                'customer_list': 'Customer List',
                'add_new_customer': 'Add New Customer',
                'customer_details': 'Customer Details',
                'total_jobs': 'Total Jobs',
                'customer_rating': 'Customer Rating',
                'joined_date': 'Joined Date',
                'no_customers_found': 'No customers found',
                'customer_name': 'Customer Name',
                'service_preferences': 'Service Preferences',
                'add_customer': 'Add Customer',
                'customer_added_successfully': 'Customer added successfully!',
                'not_provided': 'Not provided',
                'source': 'Source',
                'not_assigned': 'Not assigned',
                'no_bookings_found': 'No bookings found',
                'no_upcoming_jobs': 'No upcoming jobs',
                'username': 'Username',
                'navigation': 'Navigation',
                'feature_coming_soon': 'Feature coming soon!',
                
                # Employee Management
                'employee_list': 'Employee List',
                'add_new_employee': 'Add New Employee',
                'employee_details': 'Employee Details',
                'employee_name': 'Employee Name',
                'hourly_rate': 'Hourly Rate',
                'specialties': 'Specialties',
                'availability': 'Availability',
                'employee_status': 'Status',
                'add_employee': 'Add Employee',
                'employee_added_successfully': 'Employee added successfully!',
                'no_employees_found': 'No employees found',
                'employee_performance': 'Performance',
                'assigned_jobs': 'Assigned Jobs',
                'completed_jobs': 'Completed Jobs',
                'average_rating': 'Average Rating',
                'hire_date': 'Hire Date',
                'department': 'Department',
                'supervisor': 'Supervisor',
                'skills': 'Skills',
                'certifications': 'Certifications',
                'work_schedule': 'Work Schedule',
                'contact_emergency': 'Emergency Contact',
                'employee_id': 'Employee ID',
                'full_time': 'Full Time',
                'part_time': 'Part Time',
                'contract': 'Contract',
                'internship': 'Internship',
                'monday': 'Monday',
                'tuesday': 'Tuesday',
                'wednesday': 'Wednesday',
                'thursday': 'Thursday',
                'friday': 'Friday',
                'saturday': 'Saturday',
                'sunday': 'Sunday',
                'available': 'Available',
                'unavailable': 'Unavailable',
                'on_leave': 'On Leave',
                'sick_leave': 'Sick Leave',
                
                # Job Management
                'job_list': 'Job List',
                'add_new_job': 'Add New Job',
                'job_details': 'Job Details',
                'job_title': 'Job Title',
                'job_description': 'Job Description',
                'scheduled_date': 'Scheduled Date',
                'scheduled_time': 'Scheduled Time',
                'duration': 'Duration',
                'job_status': 'Job Status',
                'assign_employee': 'Assign Employee',
                'customer': 'Customer',
                'employee': 'Employee',
                'location': 'Location',
                'estimated_duration': 'Estimated Duration',
                'actual_duration': 'Actual Duration',
                'materials_needed': 'Materials Needed',
                'job_notes': 'Job Notes',
                'priority': 'Priority',
                'high': 'High',
                'medium': 'Medium',
                'low': 'Low',
                'urgent': 'Urgent',
                'routine': 'Routine',
                'recurring': 'Recurring',
                'one_time': 'One Time',
                'job_created_successfully': 'Job created successfully!',
                'job_updated_successfully': 'Job updated successfully!',
                'no_jobs_found': 'No jobs found',
                
                # Time and Date
                'today': 'Today',
                'tomorrow': 'Tomorrow',
                'this_week': 'This Week',
                'next_week': 'Next Week',
                'this_month': 'This Month',
                'morning': 'Morning',
                'afternoon': 'Afternoon',
                'evening': 'Evening',
                
                # Status
                'pending': 'Pending',
                'confirmed': 'Confirmed', 
                'completed': 'Completed',
                'cancelled': 'Cancelled',
                'active': 'Active',
                'inactive': 'Inactive',
                
                # Currency and Pricing
                'price': 'Price',
                'total': 'Total',
                'currency_symbol': '€',
                'per_hour': 'per hour',
                'fixed_price': 'Fixed Price',
                
                # Analytics & Reports
                'revenue_analytics': 'Revenue Analytics',
                'employee_performance_reports': 'Employee Performance Reports',
                'customer_satisfaction': 'Customer Satisfaction',
                'service_statistics': 'Service Statistics',
                'monthly_report': 'Monthly Report',
                'quarterly_report': 'Quarterly Report',
                'annual_report': 'Annual Report',
                'export_report': 'Export Report',
                'generate_report': 'Generate Report',
                'report_period': 'Report Period',
                'key_metrics': 'Key Metrics',
                'growth_rate': 'Growth Rate',
                'profit_margin': 'Profit Margin',
                'customer_retention': 'Customer Retention',
                'top_performing_employees': 'Top Performing Employees',
                'most_popular_services': 'Most Popular Services',
                'revenue_by_service': 'Revenue by Service',
                'bookings_by_month': 'Bookings by Month',
                
                # Settings
                'general_settings': 'General Settings',
                'user_management': 'User Management',
                'system_preferences': 'System Preferences',
                'backup_restore': 'Backup & Restore',
                'security_settings': 'Security Settings',
                'notification_settings': 'Notification Settings',
                'business_hours': 'Business Hours',
                'holiday_calendar': 'Holiday Calendar',
                'service_areas': 'Service Areas',
                'pricing_settings': 'Pricing Settings',
                'tax_settings': 'Tax Settings',
                'payment_methods': 'Payment Methods',
                'email_templates': 'Email Templates',
                'sms_settings': 'SMS Settings',
                'integration_settings': 'Integration Settings',
                
                # Additional terms
                'hours': 'hours',
                'minutes': 'minutes',
                'days': 'days',
                'weeks': 'weeks',
                'months': 'months',
                'years': 'years',
                
                # Footer
                'contact_us': 'Contact Us',
                'privacy_policy': 'Privacy Policy',
                'terms_of_service': 'Terms of Service',
                'about_us': 'About Us',
            },
            
            'de': {
                # Common
                'app_name': 'Aufraumenbee',
                'tagline': 'Professionelle Reinigungsdienstleistungen',
                'welcome': 'Willkommen',
                'login': 'Anmelden',
                'logout': 'Abmelden',
                'register': 'Registrieren',
                'email': 'E-Mail',
                'password': 'Passwort',
                'confirm_password': 'Passwort bestätigen',
                'first_name': 'Vorname',
                'last_name': 'Nachname',
                'phone': 'Telefon',
                'address': 'Adresse',
                'save': 'Speichern',
                'cancel': 'Abbrechen',
                'submit': 'Senden',
                'delete': 'Löschen',
                'edit': 'Bearbeiten',
                'view': 'Anzeigen',
                'search': 'Suchen',
                'loading': 'Lädt...',
                'success': 'Erfolgreich',
                'error': 'Fehler',
                'warning': 'Warnung',
                'info': 'Information',
                
                # Navigation
                'dashboard': 'Dashboard',
                'customer_management': 'Kundenverwaltung',
                'employee_management': 'Mitarbeiterverwaltung',
                'job_management': 'Auftragsverwaltung',
                'booking_requests': 'Buchungsanfragen',
                'scheduling': 'Terminplanung',
                'invoicing': 'Rechnungsstellung',
                'inventory_management': 'Lagerverwaltung',
                'analytics': 'Analysen',
                'settings': 'Einstellungen',
                
                # Customer Portal
                'book_cleaning': 'Reinigungsservice buchen',
                'my_bookings': 'Meine Buchungen',
                'service_history': 'Service-Historie',
                'account_settings': 'Kontoeinstellungen',
                'create_account': 'Konto erstellen',
                'already_have_account': 'Haben Sie bereits ein Konto?',
                'dont_have_account': 'Haben Sie noch kein Konto?',
                'sign_up_here': 'Hier registrieren',
                'login_here': 'Hier anmelden',
                
                # Services
                'basic_cleaning': 'Grundreinigung',
                'deep_cleaning': 'Tiefenreinigung',
                'office_cleaning': 'Büroreinigung',
                'window_cleaning': 'Fensterreinigung',
                'carpet_cleaning': 'Teppichreinigung',
                'move_in_out': 'Ein-/Auszugsreinigung',
                
                # Forms
                'required_field': 'Pflichtfeld',
                'optional_field': 'Optionales Feld',
                'choose_date': 'Datum wählen',
                'choose_time': 'Uhrzeit wählen',
                'service_type': 'Service-Art',
                'special_instructions': 'Besondere Anweisungen',
                'contact_info': 'Kontaktinformationen',
                'booking_summary': 'Buchungsübersicht',
                
                # Messages
                'login_success': 'Anmeldung erfolgreich! Willkommen zurück.',
                'login_failed': 'Anmeldung fehlgeschlagen. Bitte überprüfen Sie Ihre Anmeldedaten.',
                'registration_success': 'Registrierung erfolgreich! Willkommen bei Aufraumenbee!',
                'registration_failed': 'Registrierung fehlgeschlagen. Bitte versuchen Sie es erneut.',
                'booking_success': 'Buchung erfolgreich übermittelt!',
                'booking_failed': 'Buchung fehlgeschlagen. Bitte versuchen Sie es erneut.',
                'invalid_email': 'Bitte geben Sie eine gültige E-Mail-Adresse ein.',
                'password_mismatch': 'Passwörter stimmen nicht überein.',
                'password_too_short': 'Passwort muss mindestens 6 Zeichen lang sein.',
                'required_fields_missing': 'Bitte füllen Sie alle Pflichtfelder aus.',
                
                # Password Reset
                'forgot_password': 'Passwort vergessen?',
                'reset_password': 'Passwort zurücksetzen',
                'reset_password_title': 'Ihr Passwort zurücksetzen',
                'reset_instructions': 'Geben Sie Ihre E-Mail-Adresse ein und wir helfen Ihnen bei der Zurücksetzung Ihres Passworts.',
                'send_reset_code': 'Reset-Code senden',
                'reset_code': 'Reset-Code',
                'reset_code_sent': 'Ein Reset-Code wurde an Ihre E-Mail-Adresse gesendet.',
                'reset_code_instructions': 'Überprüfen Sie Ihre E-Mail auf den Reset-Code und geben Sie ihn unten zusammen mit Ihrem neuen Passwort ein.',
                'new_password': 'Neues Passwort',
                'confirm_new_password': 'Neues Passwort bestätigen',
                'password_reset_success': 'Passwort erfolgreich zurückgesetzt! Sie können sich jetzt mit Ihrem neuen Passwort anmelden.',
                'password_reset_failed': 'Passwort-Reset fehlgeschlagen. Bitte überprüfen Sie Ihren Reset-Code und versuchen Sie es erneut.',
                'invalid_reset_code': 'Ungültiger Reset-Code. Bitte überprüfen und erneut versuchen.',
                'reset_code_expired': 'Reset-Code ist abgelaufen. Bitte fordern Sie einen neuen an.',
                'back_to_login': 'Zurück zur Anmeldung',
                'enter_reset_code': 'Geben Sie den 6-stelligen Code ein, der an Ihre E-Mail gesendet wurde',
                
                'booked_on': 'Gebucht am',
                'no_bookings_yet': 'Noch keine Buchungen. Buchen Sie Ihren ersten Reinigungsservice!',
                'booking_details': 'Buchungsdetails',
                'book_now': 'Jetzt buchen',
                'address_required': 'Adresse ist erforderlich',
                'special_instructions_placeholder': 'Besondere Anforderungen oder Anweisungen...',
                
                # Dashboard
                'total_customers': 'Kunden gesamt',
                'total_employees': 'Mitarbeiter gesamt',
                'pending_jobs': 'Ausstehende Aufträge',
                'revenue_this_month': 'Umsatz diesen Monat',
                'recent_bookings': 'Neueste Buchungen',
                'upcoming_jobs': 'Anstehende Aufträge',
                
                # Customer Management
                'customer_list': 'Kundenliste',
                'add_new_customer': 'Neuen Kunden hinzufügen',
                'customer_details': 'Kundendetails',
                'total_jobs': 'Aufträge gesamt',
                'customer_rating': 'Kundenbewertung',
                'joined_date': 'Beitrittsdatum',
                'no_customers_found': 'Keine Kunden gefunden',
                'customer_name': 'Kundenname',
                'service_preferences': 'Service-Präferenzen',
                'add_customer': 'Kunde hinzufügen',
                'customer_added_successfully': 'Kunde erfolgreich hinzugefügt!',
                'not_provided': 'Nicht angegeben',
                'source': 'Quelle',
                'not_assigned': 'Nicht zugewiesen',
                'no_bookings_found': 'Keine Buchungen gefunden',
                'no_upcoming_jobs': 'Keine anstehenden Aufträge',
                'username': 'Benutzername',
                'navigation': 'Navigation',
                'feature_coming_soon': 'Feature kommt bald!',
                
                # Employee Management
                'employee_list': 'Mitarbeiterliste',
                'add_new_employee': 'Neuen Mitarbeiter hinzufügen',
                'employee_details': 'Mitarbeiterdetails',
                'employee_name': 'Mitarbeitername',
                'hourly_rate': 'Stundenlohn',
                'specialties': 'Spezialisierungen',
                'availability': 'Verfügbarkeit',
                'employee_status': 'Status',
                'add_employee': 'Mitarbeiter hinzufügen',
                'employee_added_successfully': 'Mitarbeiter erfolgreich hinzugefügt!',
                'no_employees_found': 'Keine Mitarbeiter gefunden',
                'employee_performance': 'Leistung',
                'assigned_jobs': 'Zugewiesene Aufträge',
                'completed_jobs': 'Erledigte Aufträge',
                'average_rating': 'Durchschnittsbewertung',
                'hire_date': 'Einstellungsdatum',
                'department': 'Abteilung',
                'supervisor': 'Vorgesetzter',
                'skills': 'Fähigkeiten',
                'certifications': 'Zertifizierungen',
                'work_schedule': 'Arbeitsplan',
                'contact_emergency': 'Notfallkontakt',
                'employee_id': 'Mitarbeiter-ID',
                'full_time': 'Vollzeit',
                'part_time': 'Teilzeit',
                'contract': 'Vertrag',
                'internship': 'Praktikum',
                'monday': 'Montag',
                'tuesday': 'Dienstag',
                'wednesday': 'Mittwoch',
                'thursday': 'Donnerstag',
                'friday': 'Freitag',
                'saturday': 'Samstag',
                'sunday': 'Sonntag',
                'available': 'Verfügbar',
                'unavailable': 'Nicht verfügbar',
                'on_leave': 'Im Urlaub',
                'sick_leave': 'Krankenstand',
                
                # Job Management
                'job_list': 'Auftragsliste',
                'add_new_job': 'Neuen Auftrag hinzufügen',
                'job_details': 'Auftragsdetails',
                'job_title': 'Auftragstitel',
                'job_description': 'Auftragsbeschreibung',
                'scheduled_date': 'Geplantes Datum',
                'scheduled_time': 'Geplante Uhrzeit',
                'duration': 'Dauer',
                'job_status': 'Auftragsstatus',
                'assign_employee': 'Mitarbeiter zuweisen',
                'customer': 'Kunde',
                'employee': 'Mitarbeiter',
                'location': 'Standort',
                'estimated_duration': 'Geschätzte Dauer',
                'actual_duration': 'Tatsächliche Dauer',
                'materials_needed': 'Benötigte Materialien',
                'job_notes': 'Auftragsnotizen',
                'priority': 'Priorität',
                'high': 'Hoch',
                'medium': 'Mittel',
                'low': 'Niedrig',
                'urgent': 'Dringend',
                'routine': 'Routine',
                'recurring': 'Wiederkehrend',
                'one_time': 'Einmalig',
                'job_created_successfully': 'Auftrag erfolgreich erstellt!',
                'job_updated_successfully': 'Auftrag erfolgreich aktualisiert!',
                'no_jobs_found': 'Keine Aufträge gefunden',
                
                # Time and Date
                'today': 'Heute',
                'tomorrow': 'Morgen',
                'this_week': 'Diese Woche',
                'next_week': 'Nächste Woche',
                'this_month': 'Diesen Monat',
                'morning': 'Vormittag',
                'afternoon': 'Nachmittag',
                'evening': 'Abend',
                
                # Status
                'pending': 'Ausstehend',
                'confirmed': 'Bestätigt',
                'completed': 'Abgeschlossen',
                'cancelled': 'Storniert',
                'active': 'Aktiv',
                'inactive': 'Inaktiv',
                
                # Currency and Pricing
                'price': 'Preis',
                'total': 'Gesamt',
                'currency_symbol': '€',
                'per_hour': 'pro Stunde',
                'fixed_price': 'Festpreis',
                
                # Analytics & Reports
                'revenue_analytics': 'Umsatzanalysen',
                'employee_performance_reports': 'Mitarbeiterleistungsberichte',
                'customer_satisfaction': 'Kundenzufriedenheit',
                'service_statistics': 'Service-Statistiken',
                'monthly_report': 'Monatsbericht',
                'quarterly_report': 'Quartalsbericht',
                'annual_report': 'Jahresbericht',
                'export_report': 'Bericht exportieren',
                'generate_report': 'Bericht erstellen',
                'report_period': 'Berichtszeitraum',
                'key_metrics': 'Kennzahlen',
                'growth_rate': 'Wachstumsrate',
                'profit_margin': 'Gewinnspanne',
                'customer_retention': 'Kundenbindung',
                'top_performing_employees': 'Leistungsstärkste Mitarbeiter',
                'most_popular_services': 'Beliebteste Services',
                'revenue_by_service': 'Umsatz nach Service',
                'bookings_by_month': 'Buchungen nach Monat',
                
                # Settings
                'general_settings': 'Allgemeine Einstellungen',
                'user_management': 'Benutzerverwaltung',
                'system_preferences': 'Systemeinstellungen',
                'backup_restore': 'Sicherung & Wiederherstellung',
                'security_settings': 'Sicherheitseinstellungen',
                'notification_settings': 'Benachrichtigungseinstellungen',
                'business_hours': 'Geschäftszeiten',
                'holiday_calendar': 'Feiertagskalender',
                'service_areas': 'Servicebereiche',
                'pricing_settings': 'Preiseinstellungen',
                'tax_settings': 'Steuereinstellungen',
                'payment_methods': 'Zahlungsmethoden',
                'email_templates': 'E-Mail-Vorlagen',
                'sms_settings': 'SMS-Einstellungen',
                'integration_settings': 'Integrationseinstellungen',
                
                # Additional terms
                'hours': 'Stunden',
                'minutes': 'Minuten',
                'days': 'Tage',
                'weeks': 'Wochen',
                'months': 'Monate',
                'years': 'Jahre',
                
                # Footer
                'contact_us': 'Kontakt',
                'privacy_policy': 'Datenschutz',
                'terms_of_service': 'Nutzungsbedingungen',
                'about_us': 'Über uns',
                
                # Advanced Job Management (German)
                'all_jobs': 'Alle Aufträge',
                'assign_employees': 'Mitarbeiter zuweisen',
                'job_board': 'Auftragstafel',
                'bulk_operations': 'Massenoperationen',
                'assignment_analytics': 'Zuweisungsanalyse',
                'filter_by_status': 'Nach Status filtern',
                'filter_by_employee': 'Nach Mitarbeiter filtern',
                'from_date': 'Von Datum',
                'to_date': 'Bis Datum',
                'search_jobs': 'Aufträge suchen',
                'priority': 'Priorität',
                'high_priority': 'Hohe Priorität',
                'medium_priority': 'Mittlere Priorität',
                'low_priority': 'Niedrige Priorität',
                'total_value': 'Gesamtwert',
                'assigned': 'Zugewiesen',
                'not_scheduled': 'Nicht geplant',
                'actions': 'Aktionen',
                'edit': 'Bearbeiten',
                'assign': 'Zuweisen',
                'confirm': 'Bestätigen',
                'start': 'Starten',
                'complete': 'Abschließen',
                'unassigned_jobs': 'Nicht zugewiesene Aufträge',
                'available_employees': 'Verfügbare Mitarbeiter',
                'select_employee': 'Mitarbeiter auswählen',
                'job_assigned_successfully': 'Auftrag erfolgreich zugewiesen',
                'all_jobs_assigned': 'Alle Aufträge zugewiesen',
                'no_available_employees': 'Keine verfügbaren Mitarbeiter',
                'bulk_assignment': 'Massenzuweisung',
                'select_jobs_to_assign': 'Aufträge zur Zuweisung auswählen',
                'assign_to_employee': 'Mitarbeiter zuweisen',
                'assign_selected_jobs': 'Ausgewählte Aufträge zuweisen',
                'jobs_assigned_successfully': 'Aufträge erfolgreich zugewiesen',
                'general': 'Allgemein',
                'current_jobs': 'Aktuelle Aufträge',
                'in_progress': 'In Bearbeitung',
                'select_bulk_operation': 'Massenoperation auswählen',
                'bulk_status_update': 'Massen-Statusupdate',
                'bulk_employee_assignment': 'Massen-Mitarbeiterzuweisung',
                'bulk_delete': 'Massen-Löschung',
                'bulk_reschedule': 'Massen-Umplanung',
                'bulk_price_update': 'Massen-Preisupdate',
                'selected_jobs': 'Ausgewählte Aufträge',
                'new_status': 'Neuer Status',
                'update_status': 'Status aktualisieren',
                'status_updated_successfully': 'Status erfolgreich aktualisiert',
                'assign_employee': 'Mitarbeiter zuweisen',
                'employee_assigned_successfully': 'Mitarbeiter erfolgreich zugewiesen',
                'bulk_delete_warning': 'Warnung: Diese Aktion kann nicht rückgängig gemacht werden!',
                'confirm_delete': 'Ich bestätige, dass ich diese Aufträge löschen möchte',
                'delete_selected_jobs': 'Ausgewählte Aufträge löschen',
                'jobs_deleted_successfully': 'Aufträge erfolgreich gelöscht',
                'new_date': 'Neues Datum',
                'new_time': 'Neue Zeit',
                'reschedule_jobs': 'Aufträge umplanen',
                'jobs_rescheduled_successfully': 'Aufträge erfolgreich umgeplant',
                'price_update_type': 'Preis-Update-Typ',
                'set_fixed_price': 'Festen Preis festlegen',
                'apply_percentage_change': 'Prozentuale Änderung anwenden',
                'new_price': 'Neuer Preis',
                'update_prices': 'Preise aktualisieren',
                'prices_updated_successfully': 'Preise erfolgreich aktualisiert',
                'percentage_change': 'Prozentuale Änderung',
                'no_jobs_available_for_bulk_operations': 'Keine Aufträge für Massenoperationen verfügbar',
                'key_performance_indicators': 'Wichtige Leistungsindikatoren',
                'assignment_rate': 'Zuweisungsrate',
                'completion_rate': 'Abschlussrate',
                'avg_job_value': 'Durchschnittlicher Auftragswert',
                'employee_performance_analysis': 'Mitarbeiterleistungsanalyse',
                'cancellation_rate': 'Stornierungsrate',
                'total_revenue': 'Gesamtumsatz',
                'top_performers': 'Top-Performer',
                'most_jobs_completed': 'Meiste Aufträge abgeschlossen',
                'highest_completion_rate': 'Höchste Abschlussrate',
                'highest_revenue': 'Höchster Umsatz',
                'workload_distribution': 'Arbeitsverteilung',
                'active': 'Aktiv',
                'start_date': 'Startdatum',
                'end_date': 'Enddatum',
                'edit_job': 'Auftrag bearbeiten',
                'save_changes': 'Änderungen speichern',
                'job_updated_successfully': 'Auftrag erfolgreich aktualisiert',
                'cancel': 'Abbrechen',
                'assign_employee_to_job': 'Mitarbeiter zu Auftrag zuweisen',
                'close': 'Schließen',
                'select_jobs': 'Aufträge auswählen',
                'jobs': 'Aufträge',
            }
        }
        
        # Available languages with their display names and flags
        self.available_languages = {
            'en': {'name': 'English', 'flag': '🇺🇸', 'locale': 'en_US'},
            'de': {'name': 'Deutsch', 'flag': '🇩🇪', 'locale': 'de_DE'}
        }
    
    def get_available_languages(self) -> Dict[str, Dict[str, str]]:
        """Get list of available languages"""
        return self.available_languages
    
    def get_text(self, key: str, language: str = 'en') -> str:
        """Get translated text for a given key and language"""
        try:
            # Try to get translation in requested language
            if language in self.translations and key in self.translations[language]:
                return self.translations[language][key]
            
            # Fall back to English if translation not found
            if key in self.translations['en']:
                return self.translations['en'][key]
            
            # Return key if no translation found
            return key.replace('_', ' ').title()
            
        except Exception:
            return key.replace('_', ' ').title()
    
    def get_language_from_session(self) -> str:
        """Get current language from session state"""
        return st.session_state.get('language', 'en')
    
    def set_language(self, language: str):
        """Set language in session state"""
        if language in self.available_languages:
            st.session_state.language = language
    
    def init_language_selector(self, location: str = 'sidebar') -> str:
        """Initialize language selector widget"""
        current_lang = self.get_language_from_session()
        
        # Create options for selectbox
        options = []
        option_keys = []
        for lang_code, lang_info in self.available_languages.items():
            display_text = f"{lang_info['flag']} {lang_info['name']}"
            options.append(display_text)
            option_keys.append(lang_code)
        
        # Find current selection index
        try:
            current_index = option_keys.index(current_lang)
        except ValueError:
            current_index = 0  # Default to first option (English)
        
        # Display language selector
        if location == 'sidebar':
            selected_index = st.sidebar.selectbox(
                "🌐 Language / Sprache",
                range(len(options)),
                index=current_index,
                format_func=lambda x: options[x],
                key="sidebar_language_selector"
            )
        else:
            selected_index = st.selectbox(
                "🌐 Language / Sprache",
                range(len(options)),
                index=current_index,
                format_func=lambda x: options[x],
                key="main_language_selector"
            )
        
        # Update language if changed
        selected_lang = option_keys[selected_index]
        if selected_lang != current_lang:
            self.set_language(selected_lang)
            st.rerun()
        
        return selected_lang

# Global translation manager instance
translation_manager = TranslationManager()

def t(key: str, language: str = None) -> str:
    """Shorthand function for getting translations"""
    if language is None:
        language = translation_manager.get_language_from_session()
    return translation_manager.get_text(key, language)

def init_language_selector(location: str = 'sidebar') -> str:
    """Initialize language selector - shorthand function"""
    return translation_manager.init_language_selector(location)

def get_current_language() -> str:
    """Get current language - shorthand function"""
    return translation_manager.get_language_from_session()

def add_custom_translations(language: str, translations: Dict[str, str]):
    """Add custom translations for a specific language"""
    if language not in translation_manager.translations:
        translation_manager.translations[language] = {}
    
    translation_manager.translations[language].update(translations)

# Language-specific formatting functions
def format_currency(amount: float, language: str = None) -> str:
    """Format currency based on language"""
    if language is None:
        language = get_current_language()
    
    currency_symbol = t('currency_symbol', language)
    
    if language == 'de':
        return f"{amount:.2f} {currency_symbol}"
    else:  # Default to English format
        return f"{currency_symbol}{amount:.2f}"

def format_date(date_obj, language: str = None) -> str:
    """Format date based on language"""
    if language is None:
        language = get_current_language()
    
    if language == 'de':
        return date_obj.strftime("%d.%m.%Y")
    else:  # Default to English format
        return date_obj.strftime("%m/%d/%Y")

def format_time(time_obj, language: str = None) -> str:
    """Format time based on language"""
    if language is None:
        language = get_current_language()
    
    # 24-hour format for German, 12-hour for English
    if language == 'de':
        return time_obj.strftime("%H:%M")
    else:
        return time_obj.strftime("%I:%M %p")
