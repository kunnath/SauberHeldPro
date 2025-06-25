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
                'customer_list': 'Customer List',
                'add_new_customer': 'Add New Customer',
                'customer_details': 'Customer Details',
                'total_jobs': 'Total Jobs',
                'customer_rating': 'Customer Rating',
                'joined_date': 'Joined Date',
                'no_customers_found': 'No customers found',
                
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
                'in_progress': 'In Progress',
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
                'in_progress': 'In Bearbeitung',
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
                
                # Footer
                'contact_us': 'Kontakt',
                'privacy_policy': 'Datenschutz',
                'terms_of_service': 'Nutzungsbedingungen',
                'about_us': 'Über uns',
            },
            
            # Template for easy addition of new languages
            'fr': {
                'app_name': 'Aufraumenbee',
                'tagline': 'Services de Nettoyage Professionnels',
                'welcome': 'Bienvenue',
                'login': 'Connexion',
                'register': 'S\'inscrire',
                # Add more French translations as needed
            },
            
            'es': {
                'app_name': 'Aufraumenbee',
                'tagline': 'Servicios de Limpieza Profesionales',
                'welcome': 'Bienvenido',
                'login': 'Iniciar Sesión',
                'register': 'Registrarse',
                # Add more Spanish translations as needed
            },
            
            'it': {
                'app_name': 'Aufraumenbee',
                'tagline': 'Servizi di Pulizia Professionale',
                'welcome': 'Benvenuto',
                'login': 'Accedi',
                'register': 'Registrati',
                # Add more Italian translations as needed
            }
        }
        
        # Available languages with their display names and flags
        self.available_languages = {
            'en': {'name': 'English', 'flag': '🇺🇸', 'locale': 'en_US'},
            'de': {'name': 'Deutsch', 'flag': '🇩🇪', 'locale': 'de_DE'},
            'fr': {'name': 'Français', 'flag': '🇫🇷', 'locale': 'fr_FR'},
            'es': {'name': 'Español', 'flag': '🇪🇸', 'locale': 'es_ES'},
            'it': {'name': 'Italiano', 'flag': '🇮🇹', 'locale': 'it_IT'}
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
