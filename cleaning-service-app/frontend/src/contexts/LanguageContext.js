import React, { createContext, useContext, useState, useEffect } from 'react';

const LanguageContext = createContext();

// Valid language codes
const VALID_LANGUAGES = ['en', 'de'];
const DEFAULT_LANGUAGE = 'en';

// Translation dictionary
const translations = {
  en: {
    // General
    'loading': 'Loading...',
    'error': 'Error',
    'success': 'Success',
    'cancel': 'Cancel',
    'save': 'Save',
    'edit': 'Edit',
    'delete': 'Delete',
    'confirm': 'Confirm',

    // Header and Navigation
    'english-german-support': 'English-German speaking support 7 days/week',
    'home': 'Home',
    'services': 'Services',
    'book-now': 'Book Now',
    'booking': 'Booking',
    'contact': 'Contact',
    'login': 'Login',
    'register': 'Register',
    'dashboard': 'Dashboard',
    'logout': 'Logout',
    'my-bookings': 'My Bookings',
    'my-profile': 'My Profile',

    // Home Page
    'hero-title': 'Professional Cleaning Services in Berlin',
    'hero-subtitle': 'Experience top-quality cleaning services for your home and office',
    'welcome-heading': 'Professional Cleaning Services in Berlin',
    'welcome-subheading': 'Your trusted partner for a cleaner home and office',
    'our-services-heading': 'Our Services',
    'why-choose-us': 'Why Choose Us',
    'professional-team': 'Professional Team',
    'professional-team-desc': 'Experienced and trained cleaning professionals',
    'quality-service': 'Quality Service',
    'quality-service-desc': 'Guaranteed satisfaction with every cleaning',
    'flexible-booking': 'Flexible Booking',
    'flexible-booking-desc': 'Easy online booking with flexible scheduling',
    'eco-friendly': 'Eco-Friendly',
    'eco-friendly-desc': 'Using environmentally safe cleaning products',
    'get-started': 'Get Started',
    'learn-more': 'Learn More',

    // Services Page
    'our-services-intro': 'We offer a wide range of professional cleaning services',
    'service-includes': 'Service Includes',
    'pricing': 'Pricing',
    'per-hour': 'per hour',
    'minimum-hours': 'Minimum {0} hours',
    'service-area': 'Service Area',
    'available-in': 'Available in Berlin and surrounding areas',
    'book-this-service': 'Book This Service',
    
    // Service Descriptions
    'regular-cleaning-desc': 'Regular maintenance cleaning for your home or office',
    'deep-cleaning-desc': 'Thorough deep cleaning for a complete refresh',
    'move-in-out-desc': 'Comprehensive cleaning for moving in or out',
    'office-cleaning-desc': 'Professional cleaning services for businesses',
    'window-cleaning-desc': 'Professional window and glass cleaning',
    'carpet-cleaning-desc': 'Deep carpet and upholstery cleaning',

    // Booking Page
    'booking-title': 'Book Your Cleaning Service',
    'select-service': 'Select Service',
    'select-date': 'Select Date',
    'select-time': 'Select Time',
    'enter-details': 'Enter Your Details',
    'address': 'Address',
    'postal-code': 'Postal Code',
    'city': 'City',
    'special-instructions': 'Special Instructions',
    'review-booking': 'Review Booking',
    'confirm-booking': 'Confirm Booking',
    'booking-success': 'Booking Successful',
    'booking-confirmation': 'Your booking has been confirmed',

    // Contact Page
    'contact-us': 'Contact Us',
    'contact-page-subtitle': 'Get in touch with our team for questions or support',
    'get-in-touch': 'Get in Touch',
    'phone-support': 'Phone Support',
    'phone-support-desc': 'Call us for immediate assistance',
    'contact-phone-info': 'Available Monday - Sunday (8:00 AM - 6:00 PM)',
    'email-support': 'Email Support',
    'email-support-desc': 'Send us an email anytime',
    'email-response-time': 'We typically respond within 24 hours',
    'live-chat': 'Live Chat',
    'live-chat-desc': 'Chat with our support team',
    'contact-chat-info': 'Available during business hours',
    'chat-instructions': 'Click the chat icon in the bottom right',
    'our-address': 'Our Address',
    'service-areas': 'Service Areas',
    'service-areas-desc': 'We provide our services in Berlin and surrounding areas',
    'view-all-areas': 'View all service areas',
    'business-hours': 'Business Hours',
    'customer-support-hours': 'Customer Support: Mon-Sun 8:00 AM - 6:00 PM',
    'cleaning-service-hours': 'Cleaning Service: Mon-Sun 7:00 AM - 8:00 PM',
    'emergency-service': 'Emergency service available upon request',
    'contact-form-title': 'Send us a Message',
    'message-sent': 'Your message has been sent successfully! We will get back to you soon.',
    'first-name': 'First Name',
    'last-name': 'Last Name',
    'email': 'Email',
    'phone': 'Phone',
    'inquiry-type': 'Select Inquiry Type',
    'booking-inquiry': 'Booking Inquiry',
    'general-question': 'General Question',
    'service-feedback': 'Service Feedback',
    'technical-support': 'Technical Support',
    'partnership': 'Partnership Inquiry',
    'message': 'Message',
    'message-placeholder': 'Tell us how we can help you...',
    'sending': 'Sending...',
    'send-message': 'Send Message',

    // FAQ Section
    'frequently-asked-questions': 'Frequently Asked Questions',
    'faq-1-question': 'How do I book a cleaning service?',
    'faq-1-answer': 'You can easily book our services online through our website. Simply select your desired service, choose a date and time, and provide your contact details. We will confirm your booking within minutes.',
    'faq-2-question': 'How far in advance should I book?',
    'faq-2-answer': 'We recommend booking 24-48 hours in advance for regular cleaning. For same-day or next-day service, please call us directly at +49 1577 2526898.',
    'faq-3-question': 'What if I need to cancel or reschedule?',
    'faq-3-answer': 'You can cancel or reschedule your appointment up to 24 hours before the scheduled time without any fees. Cancellations with less than 24 hours notice may incur a small fee.',
    'faq-4-question': 'Do I need to provide cleaning supplies?',
    'faq-4-answer': 'No, our cleaning professionals bring all necessary supplies and equipment. If you have specific products you would like us to use, just let us know during booking.',
    'faq-5-question': 'Are your cleaners insured and background-checked?',
    'faq-5-answer': 'Yes, all our cleaning professionals are thoroughly background-checked, insured, and bonded. We prioritize your safety and security.',
    'faq-6-question': 'What payment methods do you accept?',
    'faq-6-answer': 'We accept credit cards, debit cards, bank transfers, and digital wallets. A deposit for the first hour is required to confirm your booking.',

    // Services
    'regular-cleaning': 'Regular Cleaning',
    'deep-cleaning': 'Deep Cleaning',
    'move-in-out': 'Move In/Out Cleaning',
    'office-cleaning': 'Office Cleaning',
    'window-cleaning': 'Window Cleaning',
    'carpet-cleaning': 'Carpet Cleaning',
    'book-service': 'Book Service',

    // Home Page Translations
    'postal-code-title': 'Enter your postal code',
    'postal-code-placeholder': 'Enter postal code...',
    'how-it-works': 'How It Works',
    'step-1-title': 'Book Online',
    'step-1-desc': 'Select your service and preferred time',
    'step-2-title': 'Confirm Booking',
    'step-2-desc': 'Receive instant confirmation',
    'step-3-title': 'Get Service',
    'step-3-desc': 'Our professionals arrive on time',
    'services-title': 'Our Services',
    'basic-cleaning': 'Basic Cleaning',
    'basic-cleaning-price': 'From €20/hour',
    'basic-cleaning-desc': 'Regular home cleaning service',
    'basic-feature-1': 'Dusting and wiping surfaces',
    'basic-feature-2': 'Vacuum cleaning',
    'basic-feature-3': 'Bathroom cleaning',
    'basic-feature-4': 'Kitchen cleaning',
    'basic-feature-5': 'Floor mopping',
    'deep-cleaning': 'Deep Cleaning',
    'deep-cleaning-price': 'From €25/hour',
    'deep-cleaning-desc': 'Thorough deep cleaning service',
    'deep-feature-1': 'All basic cleaning services',
    'deep-feature-2': 'Window cleaning',
    'deep-feature-3': 'Cabinet interior cleaning',
    'deep-feature-4': 'Wall cleaning',
    'deep-feature-5': 'Deep furniture cleaning',
    'office-cleaning': 'Office Cleaning',
    'office-cleaning-price': 'From €22/hour',
    'office-cleaning-desc': 'Professional office cleaning',
    'office-feature-1': 'Workspace cleaning',
    'office-feature-2': 'Meeting room service',
    'office-feature-3': 'Kitchen and break room',
    'office-feature-4': 'Restroom sanitation',
    'office-feature-5': 'Waste management',
    'contact-section-title': 'Contact Us',
    'contact-section-subtitle': 'We\'re here to help',
    'contact-phone-title': 'Phone Support',
    'contact-phone-info': '+49 1577 2526898',
    'contact-email-title': 'Email Support',
    'contact-email-info': 'support@sauberheld.de',
    'contact-chat-title': 'Live Chat',
    'contact-chat-info': 'Available 8 AM - 8 PM',
    'features-title': 'Why Choose Us',
    'easy-booking-title': 'Easy Online Booking',
    'easy-booking-desc': 'Book your cleaning service in minutes',
    'background-checked-title': 'Verified Professionals',
    'background-checked-desc': 'All cleaners are background checked',
    'english-speaking-title': 'English Speaking',
    'english-speaking-desc': 'Communication in English & German',
    'testimonials-title': 'What Our Customers Say',
    'testimonials-subtitle': 'Trusted by thousands of satisfied customers',
    'testimonial-1': 'Excellent service! The cleaners were professional and thorough.',
    'testimonial-1-author': 'Sarah M.',
    'testimonial-2': 'Very reliable and always on time. Highly recommended!',
    'testimonial-2-author': 'Michael K.',
    'testimonial-3': 'Great attention to detail and friendly service.',
    'testimonial-3-author': 'Lisa B.',
  },
  de: {
    // General
    'loading': 'Laden...',
    'error': 'Fehler',
    'success': 'Erfolg',
    'cancel': 'Abbrechen',
    'save': 'Speichern',
    'edit': 'Bearbeiten',
    'delete': 'Löschen',
    'confirm': 'Bestätigen',

    // Header and Navigation
    'english-german-support': 'Deutsch-Englisch sprechender Support 7 Tage/Woche',
    'home': 'Startseite',
    'services': 'Dienstleistungen',
    'book-now': 'Jetzt Buchen',
    'booking': 'Buchung',
    'contact': 'Kontakt',
    'login': 'Anmelden',
    'register': 'Registrieren',
    'dashboard': 'Dashboard',
    'logout': 'Abmelden',
    'my-bookings': 'Meine Buchungen',
    'my-profile': 'Mein Profil',

    // Home Page
    'hero-title': 'Professionelle Reinigungsservices in Berlin',
    'hero-subtitle': 'Erleben Sie erstklassige Reinigungsservices für Ihr Zuhause und Büro',
    'welcome-heading': 'Professionelle Reinigungsservices in Berlin',
    'welcome-subheading': 'Ihr vertrauenswürdiger Partner für ein sauberes Zuhause und Büro',
    'our-services-heading': 'Unsere Dienstleistungen',
    'why-choose-us': 'Warum Uns Wählen',
    'professional-team': 'Professionelles Team',
    'professional-team-desc': 'Erfahrene und geschulte Reinigungskräfte',
    'quality-service': 'Qualitätsservice',
    'quality-service-desc': 'Garantierte Zufriedenheit bei jeder Reinigung',
    'flexible-booking': 'Flexible Buchung',
    'flexible-booking-desc': 'Einfache Online-Buchung mit flexibler Terminplanung',
    'eco-friendly': 'Umweltfreundlich',
    'eco-friendly-desc': 'Verwendung umweltschonender Reinigungsprodukte',
    'get-started': 'Jetzt Starten',
    'learn-more': 'Mehr Erfahren',

    // Services Page
    'our-services-intro': 'Wir bieten eine breite Palette professioneller Reinigungsdienstleistungen',
    'service-includes': 'Service beinhaltet',
    'pricing': 'Preise',
    'per-hour': 'pro Stunde',
    'minimum-hours': 'Mindestens {0} Stunden',
    'service-area': 'Servicegebiet',
    'available-in': 'Verfügbar in Berlin und Umgebung',
    'book-this-service': 'Diesen Service Buchen',
    
    // Service Descriptions
    'regular-cleaning-desc': 'Regelmäßige Unterhaltsreinigung für Ihr Zuhause oder Büro',
    'deep-cleaning-desc': 'Gründliche Tiefenreinigung für eine komplette Auffrischung',
    'move-in-out-desc': 'Umfassende Reinigung beim Ein- oder Auszug',
    'office-cleaning-desc': 'Professionelle Reinigungsservices für Unternehmen',
    'window-cleaning-desc': 'Professionelle Fenster- und Glasreinigung',
    'carpet-cleaning-desc': 'Teppich- und Polsterreinigung',

    // Booking Page
    'booking-title': 'Buchen Sie Ihren Reinigungsservice',
    'select-service': 'Service Auswählen',
    'select-date': 'Datum Auswählen',
    'select-time': 'Uhrzeit Auswählen',
    'enter-details': 'Ihre Details',
    'address': 'Adresse',
    'postal-code': 'Postleitzahl',
    'city': 'Stadt',
    'special-instructions': 'Besondere Hinweise',
    'review-booking': 'Buchung Überprüfen',
    'confirm-booking': 'Buchung Bestätigen',
    'booking-success': 'Buchung Erfolgreich',
    'booking-confirmation': 'Ihre Buchung wurde bestätigt',

    // Contact Page
    'contact-us': 'Kontakt',
    'contact-page-subtitle': 'Nehmen Sie Kontakt mit unserem Team auf für Fragen oder Unterstützung',
    'get-in-touch': 'Kontaktieren Sie uns',
    'phone-support': 'Telefonische Unterstützung',
    'phone-support-desc': 'Rufen Sie uns an für direkte Hilfe',
    'contact-phone-info': 'Verfügbar Montag - Sonntag (8:00 - 18:00 Uhr)',
    'email-support': 'E-Mail Support',
    'email-support-desc': 'Senden Sie uns jederzeit eine E-Mail',
    'email-response-time': 'Wir antworten in der Regel innerhalb von 24 Stunden',
    'live-chat': 'Live Chat',
    'live-chat-desc': 'Chatten Sie mit unserem Support-Team',
    'contact-chat-info': 'Verfügbar während der Geschäftszeiten',
    'chat-instructions': 'Klicken Sie auf das Chat-Symbol unten rechts',
    'our-address': 'Unsere Adresse',
    'service-areas': 'Servicegebiete',
    'service-areas-desc': 'Wir bieten unsere Dienste in Berlin und Umgebung an',
    'view-all-areas': 'Alle Servicegebiete anzeigen',
    'business-hours': 'Öffnungszeiten',
    'customer-support-hours': 'Kundenservice: Mo-So 8:00 - 18:00 Uhr',
    'cleaning-service-hours': 'Reinigungsservice: Mo-So 7:00 - 20:00 Uhr',
    'emergency-service': 'Notfallservice auf Anfrage verfügbar',
    'contact-form-title': 'Nachricht senden',
    'message-sent': 'Ihre Nachricht wurde erfolgreich gesendet! Wir melden uns in Kürze bei Ihnen.',
    'first-name': 'Vorname',
    'last-name': 'Nachname',
    'email': 'E-Mail',
    'phone': 'Telefon',
    'inquiry-type': 'Art der Anfrage',
    'booking-inquiry': 'Buchungsanfrage',
    'general-question': 'Allgemeine Frage',
    'service-feedback': 'Service Feedback',
    'technical-support': 'Technischer Support',
    'partnership': 'Kooperationsanfrage',
    'message': 'Nachricht',
    'message-placeholder': 'Wie können wir Ihnen helfen?',
    'sending': 'Wird gesendet...',
    'send-message': 'Nachricht senden',

    // FAQ Section
    'frequently-asked-questions': 'Häufig gestellte Fragen',
    'faq-1-question': 'Wie buche ich einen Reinigungsservice?',
    'faq-1-answer': 'Sie können unsere Dienste ganz einfach online über unsere Website buchen. Wählen Sie einfach den gewünschten Service aus, wählen Sie Datum und Uhrzeit und geben Sie Ihre Kontaktdaten an. Wir bestätigen Ihre Buchung innerhalb weniger Minuten.',
    'faq-2-question': 'Wie weit im Voraus sollte ich buchen?',
    'faq-2-answer': 'Wir empfehlen, für reguläre Reinigungen 24-48 Stunden im Voraus zu buchen. Für einen Service am selben Tag oder am nächsten Tag rufen Sie uns bitte direkt unter +49 1577 2526898 an.',
    'faq-3-question': 'Was passiert, wenn ich stornieren oder umbuchen muss?',
    'faq-3-answer': 'Sie können Ihren Termin bis zu 24 Stunden vor der geplanten Zeit kostenlos stornieren oder umbuchen. Bei Stornierungen mit weniger als 24 Stunden Vorlaufzeit kann eine kleine Gebühr anfallen.',
    'faq-4-question': 'Muss ich Reinigungsmittel zur Verfügung stellen?',
    'faq-4-answer': 'Nein, unsere Reinigungskräfte bringen alle notwendigen Reinigungsmittel und Geräte mit. Wenn Sie bestimmte Produkte verwenden möchten, teilen Sie uns dies bitte bei der Buchung mit.',
    'faq-5-question': 'Sind Ihre Reinigungskräfte versichert und überprüft?',
    'faq-5-answer': 'Ja, alle unsere Reinigungskräfte werden gründlich überprüft und sind versichert. Wir legen höchsten Wert auf Ihre Sicherheit.',
    'faq-6-question': 'Welche Zahlungsmethoden akzeptieren Sie?',
    'faq-6-answer': 'Wir akzeptieren Kredit- und Debitkarten, Banküberweisung und digitale Zahlungsmethoden. Für die Bestätigung der Buchung ist eine Anzahlung für die erste Stunde erforderlich.',

    // Services
    'regular-cleaning': 'Reguläre Reinigung',
    'deep-cleaning': 'Grundreinigung',
    'move-in-out': 'Umzugsreinigung',
    'office-cleaning': 'Büroreinigung',
    'window-cleaning': 'Fensterreinigung',
    'carpet-cleaning': 'Teppichreinigung',
    'book-service': 'Service buchen',

    // Home Page Translations
    'postal-code-title': 'Geben Sie Ihre Postleitzahl ein',
    'postal-code-placeholder': 'Postleitzahl eingeben...',
    'book-now': 'Jetzt Buchen',
    'how-it-works': 'So Funktioniert\'s',
    'step-1-title': 'Online Buchen',
    'step-1-desc': 'Wählen Sie Ihren Service und Wunschtermin',
    'step-2-title': 'Buchung Bestätigen',
    'step-2-desc': 'Erhalten Sie sofortige Bestätigung',
    'step-3-title': 'Service Erhalten',
    'step-3-desc': 'Unsere Profis kommen pünktlich',
    'services-title': 'Unsere Dienstleistungen',
    'basic-cleaning': 'Grundreinigung',
    'basic-cleaning-price': 'Ab €20/Stunde',
    'basic-cleaning-desc': 'Regelmäßige Haushaltsreinigung',
    'basic-feature-1': 'Abstauben und Wischen',
    'basic-feature-2': 'Staubsaugen',
    'basic-feature-3': 'Badreinigung',
    'basic-feature-4': 'Küchenreinigung',
    'basic-feature-5': 'Bodenwischen',
    'deep-cleaning': 'Tiefenreinigung',
    'deep-cleaning-price': 'Ab €25/Stunde',
    'deep-cleaning-desc': 'Gründliche Tiefenreinigung',
    'deep-feature-1': 'Alle Grundreinigungsservices',
    'deep-feature-2': 'Fensterreinigung',
    'deep-feature-3': 'Schrankinnenreinigung',
    'deep-feature-4': 'Wandreinigung',
    'deep-feature-5': 'Tiefe Möbelreinigung',
    'office-cleaning': 'Büroreinigung',
    'office-cleaning-price': 'Ab €22/Stunde',
    'office-cleaning-desc': 'Professionelle Büroreinigung',
    'office-feature-1': 'Arbeitsplatzreinigung',
    'office-feature-2': 'Besprechungsraumservice',
    'office-feature-3': 'Küche und Pausenraum',
    'office-feature-4': 'Toilettenreinigung',
    'office-feature-5': 'Abfallentsorgung',
    'contact-section-title': 'Kontaktieren Sie Uns',
    'contact-section-subtitle': 'Wir sind für Sie da',
    'contact-phone-title': 'Telefonischer Support',
    'contact-phone-info': '+49 1577 2526898',
    'contact-email-title': 'E-Mail Support',
    'contact-email-info': 'support@sauberheld.de',
    'contact-chat-title': 'Live Chat',
    'contact-chat-info': 'Verfügbar 8-20 Uhr',
    'features-title': 'Warum Uns Wählen',
    'easy-booking-title': 'Einfache Online-Buchung',
    'easy-booking-desc': 'Buchen Sie Ihren Reinigungsservice in Minuten',
    'background-checked-title': 'Geprüfte Fachkräfte',
    'background-checked-desc': 'Alle Reinigungskräfte sind überprüft',
    'english-speaking-title': 'Englischsprachig',
    'english-speaking-desc': 'Kommunikation in Deutsch & Englisch',
    'testimonials-title': 'Was Unsere Kunden Sagen',
    'testimonials-subtitle': 'Vertraut von tausenden zufriedenen Kunden',
    'testimonial-1': 'Ausgezeichneter Service! Die Reinigungskräfte waren professionell und gründlich.',
    'testimonial-1-author': 'Sarah M.',
    'testimonial-2': 'Sehr zuverlässig und immer pünktlich. Sehr zu empfehlen!',
    'testimonial-2-author': 'Michael K.',
    'testimonial-3': 'Große Aufmerksamkeit für Details und freundlicher Service.',
    'testimonial-3-author': 'Lisa B.',
  }
};

export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState(() => {
    const savedLanguage = localStorage.getItem('language');
    return VALID_LANGUAGES.includes(savedLanguage) ? savedLanguage : DEFAULT_LANGUAGE;
  });

  const [isChanging, setIsChanging] = useState(false);

  useEffect(() => {
    localStorage.setItem('language', currentLanguage);
    document.documentElement.lang = currentLanguage;
  }, [currentLanguage]);

  const changeLanguage = (lang) => {
    if (!VALID_LANGUAGES.includes(lang)) {
      console.warn(`Invalid language code: ${lang}`);
      return;
    }
    setIsChanging(true);
    setCurrentLanguage(lang);
    setTimeout(() => setIsChanging(false), 300); // Add a small delay for UI transitions
  };

  const toggleLanguage = () => {
    const newLang = currentLanguage === 'en' ? 'de' : 'en';
    changeLanguage(newLang);
  };

  const t = (key, ...args) => {
    if (!translations[currentLanguage]) {
      console.warn(`Missing language: ${currentLanguage}`);
      return key;
    }

    const translation = translations[currentLanguage][key];
    if (!translation) {
      console.warn(`Missing translation key: ${key} for language: ${currentLanguage}`);
      // Fallback to English if translation is missing
      return translations['en'][key] || key;
    }

    // Handle parameterized translations
    if (args.length > 0) {
      return translation.replace(/\{(\d+)\}/g, (match, num) => args[num] || match);
    }

    return translation;
  };

  return (
    <LanguageContext.Provider 
      value={{ 
        currentLanguage, 
        isChanging,
        changeLanguage,
        toggleLanguage, 
        t,
        languages: VALID_LANGUAGES 
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export default LanguageContext;
