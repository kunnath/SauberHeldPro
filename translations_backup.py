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
                
                # Dashboard
                'total_customers': 'Total Customers',
                'total_employees': 'Total Employees',
                'pending_jobs': 'Pending Jobs',
                'revenue_this_month': 'Revenue This Month',
                'recent_bookings': 'Recent Bookings',
                'upcoming_jobs': 'Upcoming Jobs',
                
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
                'job_title': 'Aufragstitel',
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
                
                # Inventory Management
                'inventory_list': 'Inventarliste',
                'add_new_item': 'Neues Element hinzufügen',
                'item_name': 'Artikelname',
                'item_description': 'Artikelbeschreibung',
                'quantity_in_stock': 'Lagerbestand',
                'minimum_stock_level': 'Mindestlagerbestand',
                'unit_cost': 'Stückkosten',
                'supplier': 'Lieferant',
                'category': 'Kategorie',
                'cleaning_supplies': 'Reinigungsmittel',
                'equipment': 'Ausrüstung',
                'safety_gear': 'Sicherheitsausrüstung',
                'tools': 'Werkzeuge',
                'low_stock_alert': 'Niedrigbestand-Warnung',
                'out_of_stock': 'Nicht auf Lager',
                'reorder_needed': 'Nachbestellung erforderlich',
                'last_updated': 'Zuletzt aktualisiert',
                'expiry_date': 'Ablaufdatum',
                'storage_location': 'Lagerort',
                
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
            }
        }
    
    def translate(self, key: str, lang: str = 'en') -> str:
        """Translates a given key to the specified language"""
        return self.translations.get(lang, {}).get(key, key)

    def add_translation(self, lang: str, key: str, translation: str):
        """Adds a new translation for a specific key"""
        if lang not in self.translations:
            self.translations[lang] = {}
        self.translations[lang][key] = translation

    def remove_translation(self, lang: str, key: str):
        """Removes a translation for a specific key"""
        if lang in self.translations and key in self.translations[lang]:
            del self.translations[lang][key]

    def get_supported_languages(self) -> list:
        """Returns a list of supported languages"""
        return list(self.translations.keys())

    def is_language_supported(self, lang: str) -> bool:
        """Checks if a language is supported"""
        return lang in self.translations

    def get_translation_keys(self, lang: str) -> list:
        """Returns a list of all translation keys for a specific language"""
        return list(self.translations.get(lang, {}).keys())

    def get_translation_values(self, lang: str) -> list:
        """Returns a list of all translation values for a specific language"""
        return list(self.translations.get(lang, {}).values())

    def export_translations(self, lang: str) -> Dict[str, Any]:
        """Exports translations for a specific language"""
        return self.translations.get(lang, {})

    def import_translations(self, lang: str, translations: Dict[str, Any]):
        """Imports translations for a specific language"""
        if lang not in self.translations:
            self.translations[lang] = {}
        self.translations[lang].update(translations)

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
