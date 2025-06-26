import React, { createContext, useContext, useState, useEffect } from 'react';

const LanguageContext = createContext();

// Translation dictionary
const translations = {
  en: {
    // Header
    'english-german-support': 'English-German speaking support 7 days/week',
    'home': 'Home',
    'services': 'Services',
    'booking': 'Booking',
    'contact': 'Contact',
    'login': 'Login',
    'dashboard': 'Dashboard',
    'logout': 'Logout',
    
    // Home Page
    'hero-title': 'Book a reliable cleaning professional for your apartment or office',
    'hero-subtitle': 'Professional cleaning services with English-German speaking support 7 days a week',
    'book-now': 'Book Now',
    'learn-more': 'Learn More',
    'get-quote': 'Get Free Quote',
    'postal-code-title': 'Enter your postal code to get started:',
    'postal-code-placeholder': 'e.g., 10115',
    
    // How it works section
    'how-it-works': 'How does it work?',
    'step-1-title': 'Fill out the booking form',
    'step-1-desc': 'Select the type of cleaning, specify the date & time, and give us the address of your property. You can also select from a range of special requests.',
    'step-2-title': 'Pay for the first hour',
    'step-2-desc': 'To confirm your booking a deposit for the first hour is required. The amount paid is deducted from the final bill.',
    'step-3-title': 'Have your place cleaned',
    'step-3-desc': 'We\'ll match you with a verified cleaning person, who\'ll clean your apartment. After the cleaning, you\'ll receive a cleaning summary.',
    
    // Services section
    'services-title': 'Cleaning services for homes & offices',
    'basic-cleaning': 'Basic Cleaning',
    'basic-cleaning-price': '€28.90/h',
    'basic-cleaning-desc': 'Reliable home cleaning service. Good choice if you want to maintain a clean home.',
    // Individual service features
    'basic-feature-1': 'Regular maintenance cleaning',
    'basic-feature-2': 'Dusting and vacuuming',
    'basic-feature-3': 'Kitchen and bathroom cleaning',
    'basic-feature-4': 'Trash removal',
    'basic-feature-5': 'Reduced price for subscribers',
    
    'deep-cleaning': 'Deep Cleaning',
    'deep-cleaning-price': '€45.00/h',
    'deep-cleaning-desc': 'Extensive cleaning for move-in/move-out or after renovation.',
    // Individual service features
    'deep-feature-1': 'Everything in Basic Cleaning',
    'deep-feature-2': 'Deep scrubbing of bathrooms',
    'deep-feature-3': 'Inside oven and refrigerator cleaning',
    'deep-feature-4': 'Baseboards and window sills',
    'deep-feature-5': 'Light fixtures and ceiling fans',
    
    'office-cleaning': 'Office Cleaning',
    'office-cleaning-price': '€35.00/h',
    'office-cleaning-desc': 'Customized cleaning solutions for your workplace.',
    // Individual service features
    'office-feature-1': 'Desk and workspace sanitizing',
    'office-feature-2': 'Conference room cleaning',
    'office-feature-3': 'Kitchen/break room maintenance',
    'office-feature-4': 'Restroom deep cleaning',
    'office-feature-5': 'Common area maintenance',
    
    // Contact section
    'contact-section-title': 'German/English-speaking customer support 7 days/week',
    'contact-section-subtitle': 'Always ready to help',
    'contact-phone-title': 'VIA PHONE',
    'contact-phone-info': '+49 1577 2526898\n8 am - 6 pm (Monday - Sunday)',
    'contact-email-title': 'VIA EMAIL',
    'contact-email-info': 'info@cleaningservice.de\n24/7 (every day)',
    'contact-chat-title': 'VIA CHAT',
    'contact-chat-info': 'Chat on our website\n8 am - 6 pm (Monday - Sunday)',
    
    // Features Section
    'features-title': 'Find your dedicated home cleaner',
    'easy-booking-title': 'Easy Online Booking',
    'easy-booking-desc': 'You can book a home cleaning service in just 60 seconds using our simple booking form.',
    'background-checked-title': 'Background-Checked',
    'background-checked-desc': 'All cleaning service providers offering their services on our website are background-checked, legally-registered businesses.',
    'english-speaking-title': 'English Speaking',
    'english-speaking-desc': 'You can choose an English-speaking cleaner at no extra cost.',
    
    // Testimonials
    'testimonials-title': 'Over 20,000 happy customers since 2016',
    'testimonials-subtitle': 'What our customers say about our service?',
    'testimonial-1': 'I booked the last minute option a day before the cleaning. Everything was perfect. 10/10',
    'testimonial-1-author': 'Sorel Mihai Arghire',
    'testimonial-2': 'Very good service. We use their cleaners every week and we are very happy with the result. They are very professional and fast. I can only recommend.',
    'testimonial-2-author': 'Jerneja Vrcek',
    'testimonial-3': 'Excellent cleaning service, highest quality service and efficiency. Furthermore the customer support is fantastic. I will be recommending them to everyone! 5 stars!!',
    'testimonial-3-author': 'Abigail Horn',
    
    // Features Section
    'why-choose-us': 'Why Choose Us?',
    'trusted-professionals': 'Trusted Professionals',
    'trusted-professionals-desc': 'Our experienced and vetted cleaning professionals deliver exceptional results every time.',
    'eco-friendly': 'Eco-Friendly Products',
    'eco-friendly-desc': 'We use only environmentally safe cleaning products that are safe for your family and pets.',
    'flexible-scheduling': 'Flexible Scheduling',
    'flexible-scheduling-desc': 'Book cleaning services at your convenience with our easy online booking system.',
    'satisfaction-guarantee': '100% Satisfaction Guarantee',
    'satisfaction-guarantee-desc': 'Not happy with our service? We\'ll make it right or your money back.',
    
    // Contact Section
    'get-in-touch': 'Get in Touch',
    'contact-subtitle': 'Ready to experience the cleanest space of your life? Contact us today!',
    'call-now': 'Call Now',
    'email-us': 'Email Us',
    'live-chat': 'Live Chat',
    
    // Services
    'our-services': 'Our Services',
    'residential-cleaning': 'Residential Cleaning',
    'commercial-cleaning': 'Commercial Cleaning',
    'deep-cleaning': 'Deep Cleaning',
    'move-in-out': 'Move-in/Move-out Cleaning',
    
    // Booking
    'book-service': 'Book a Service',
    'select-service': 'Select Service',
    'choose-date': 'Choose Date',
    'choose-time': 'Choose Time',
    'contact-details': 'Contact Details',
    'booking-summary': 'Booking Summary',
    'confirm-booking': 'Confirm Booking',
    'first-name': 'First Name',
    'last-name': 'Last Name',
    'email': 'Email',
    'phone': 'Phone',
    'address': 'Address',
    'postal-code': 'Postal Code',
    'special-requests': 'Special Requests',
    
    // Success Page
    'booking-confirmed': 'Booking Confirmed!',
    'booking-success-message': 'Your cleaning service has been successfully booked!',
    'booking-details': 'Your Booking Details',
    'booking-id': 'Booking ID',
    'service': 'Service',
    'date': 'Date',
    'time': 'Time',
    'location': 'Location',
    'exclusive-bonus': 'Exclusive First-Time Bonus!',
    'welcome-offer': 'Thank you for choosing our service! As a welcome gift, enjoy 20% OFF your next booking!',
    'promo-code': 'Use Code: WELCOME20',
    'what-happens-next': 'What Happens Next?',
    'view-dashboard': 'View Dashboard',
    'book-another': 'Book Another Service',
    'contact-support': 'Contact Support',
    'call-us': 'Call Us',
    
    // Dashboard
    'welcome-back': 'Welcome back',
    'your-dashboard': 'Your Dashboard',
    'upcoming-bookings': 'Upcoming Bookings',
    'booking-history': 'Booking History',
    'account-settings': 'Account Settings',
    'view-details': 'View Details',
    'cancel-booking': 'Cancel Booking',
    'no-upcoming-bookings': 'No upcoming bookings',
    'no-booking-history': 'No booking history yet',
    
    // Detailed Services Page
    'our-cleaning-services': 'Our Cleaning Services',
    'professional-solutions-subtitle': 'Professional cleaning solutions tailored to your needs. All services include background-checked cleaners and satisfaction guarantee.',
    'service-comparison': 'Service Comparison',
    'features': 'Features',
    'why-choose-services': 'Why Choose Our Services?',
    'quick-efficient': 'Quick & Efficient',
    'quick-efficient-desc': 'Our trained professionals work efficiently to get your space clean without disrupting your schedule.',
    'fully-insured': 'Fully Insured',
    'fully-insured-desc': 'All our cleaners are background-checked, insured, and bonded for your peace of mind.',
    'flexible-scheduling': 'Flexible Scheduling',
    'flexible-scheduling-detailed': 'Book one-time cleanings or set up regular service. We work around your schedule.',
    
    // Service Details
    'basic-cleaning-detailed': 'Perfect for regular maintenance and keeping your home consistently clean. Our basic cleaning service covers all essential areas.',
    'basic-duration': '2-3 hours',
    'basic-ideal': 'Regular maintenance',
    'basic-features': [
      'Dusting and wiping surfaces',
      'Vacuuming all floors',
      'Kitchen cleaning (counters, sink, appliances)',
      'Bathroom cleaning and sanitizing',
      'Trash removal',
      'Making beds',
      'General tidying up'
    ],
    
    'deep-cleaning-detailed': 'Comprehensive cleaning for move-ins, move-outs, or when you need a thorough refresh. Includes everything in basic cleaning plus detailed work.',
    'deep-duration': '4-6 hours',
    'deep-ideal': 'Move-in/out, spring cleaning',
    'deep-features': [
      'Everything in Basic Cleaning',
      'Deep scrubbing of bathrooms',
      'Inside oven and refrigerator cleaning',
      'Baseboards and window sills',
      'Light fixtures and ceiling fans',
      'Interior window cleaning',
      'Cabinet fronts and drawers'
    ],
    
    'office-cleaning-detailed': 'Professional cleaning solutions tailored for your workplace. Create a healthy and productive environment for your team.',
    'office-duration': '2-4 hours',
    'office-ideal': 'Small to medium offices',
    'office-features': [
      'Desk and workspace sanitizing',
      'Conference room cleaning',
      'Kitchen/break room maintenance',
      'Restroom deep cleaning',
      'Floor vacuuming and mopping',
      'Trash and recycling removal',
      'Common area maintenance'
    ],
    
    // Comparison Table
    'dusting-surface-cleaning': 'Dusting & Surface Cleaning',
    'vacuuming': 'Vacuuming',
    'kitchen-cleaning': 'Kitchen Cleaning',
    'bathroom-sanitizing': 'Bathroom Sanitizing',
    'trash-removal': 'Trash Removal',
    'inside-appliances': 'Inside Appliances',
    'baseboards-details': 'Baseboards & Details',
    'window-cleaning-interior': 'Window Cleaning (Interior)',
    'workspace-sanitizing': 'Workspace Sanitizing',
    'conference-room-setup': 'Conference Room Setup',
    
    'book-service-type': 'Book {service}',
    'duration': 'Duration',
    'ideal-for': 'Ideal for',
    
    // Common
    'loading': 'Loading...',
    'submit': 'Submit',
    'cancel': 'Cancel',
    'edit': 'Edit',
    'save': 'Save',
    'delete': 'Delete',
    'yes': 'Yes',
    'no': 'No',
    'back': 'Back',
    'next': 'Next',
    'previous': 'Previous',
    'close': 'Close',
    
    // Booking Page Detailed
    'book-cleaning-service': 'Einen Reinigungsservice Buchen',
    'quick-easy-booking': 'Schnelle und einfache Buchung in nur wenigen Schritten',
    'step-1': 'Schritt 1',
    'step-2': 'Schritt 2',
    'step-3': 'Schritt 3', 
    'step-4': 'Schritt 4',
    'select-service-step': 'Service Auswählen',
    'choose-date-time': 'Datum & Zeit',
    'contact-details-step': 'Kontaktdaten',
    'confirm-book': 'Bestätigen & Buchen',
    
    // Service Selection
    'choose-service-type': 'Wählen Sie Ihren Service-Typ',
    'basic-cleaning-booking': 'Grundreinigung',
    'basic-cleaning-booking-desc': 'Regelmäßige Unterhaltsreinigung, Abstauben, Staubsaugen, Küchen- und Badezimmerreinigung',
    'deep-cleaning-booking': 'Tiefenreinigung',
    'deep-cleaning-booking-desc': 'Umfassende Reinigung, Baustellenreinigung, tiefe Küchen- und Badezimmerreinigung',
    'office-cleaning-booking': 'Büroreinigung',
    'office-cleaning-booking-desc': 'Maßgeschneiderte Reinigungslösungen für Ihren Arbeitsplatz',
    'per-hour': '/Stunde',
    'estimated-duration': 'Geschätzte Dauer',
    'hours': 'Stunden',
    
    // Date & Time Selection
    'select-date-time': 'Wählen Sie Ihr bevorzugtes Datum und Ihre Zeit',
    'available-times': 'Verfügbare Zeiten',
    'no-available-slots': 'Keine verfügbaren Zeitfenster für dieses Datum',
    'select-different-date': 'Bitte wählen Sie ein anderes Datum',
    
    // Contact Form
    'your-contact-information': 'Ihre Kontaktinformationen',
    'full-name': 'Vollständiger Name',
    'email-address': 'E-Mail-Adresse',
    'phone-number': 'Telefonnummer',
    'full-address': 'Vollständige Adresse',
    'additional-notes': 'Zusätzliche Notizen',
    'special-instructions': 'Besondere Anweisungen oder Wünsche',
    
    // Booking Summary
    'booking-summary-title': 'Buchungsübersicht',
    'selected-service': 'Ausgewählter Service',
    'scheduled-date': 'Geplantes Datum',
    'scheduled-time': 'Geplante Zeit',
    'customer-info': 'Kundeninformationen',
    'total-estimated-cost': 'Geschätzte Gesamtkosten',
    'deposit-required': 'Erforderliche Anzahlung (Erste Stunde)',
    'remaining-balance': 'Verbleibendes Guthaben',
    'paid-after-service': 'Nach Abschluss des Services zu zahlen',
    
    // Buttons & Actions
    'continue': 'Weiter',
    'go-back': 'Zurück',
    'book-service-now': 'Service Jetzt Buchen',
    'processing': 'Wird verarbeitet...',
    
    // Validation Messages
    'required-field': 'Dieses Feld ist erforderlich',
    'invalid-email': 'Bitte geben Sie eine gültige E-Mail-Adresse ein',
    'invalid-phone': 'Bitte geben Sie eine gültige Telefonnummer ein',
    'select-service-first': 'Bitte wählen Sie zuerst einen Service',
    'select-date-first': 'Bitte wählen Sie zuerst ein Datum',
    'select-time-first': 'Bitte wählen Sie zuerst eine Zeit',
    
    // Contact Page
    'contact-us': 'Kontakt',
    'contact-page-subtitle': 'Nehmen Sie Kontakt mit unserem freundlichen Team auf. Wir helfen Ihnen gerne bei allen Fragen zu unseren Reinigungsdienstleistungen.',
    'get-in-touch': 'Kontakt aufnehmen',
    'phone-support': 'Telefon-Support',
    'phone-support-desc': 'Sprechen Sie direkt mit unserem Kundenservice-Team',
    'email-support': 'E-Mail-Support',
    'email-support-desc': 'Senden Sie uns jederzeit eine Nachricht',
    'email-response-time': 'Wir antworten innerhalb von 24 Stunden',
    'live-chat': 'Live-Chat',
    'live-chat-desc': 'Chatten Sie direkt mit uns auf unserer Website',
    'chat-instructions': 'Klicken Sie auf das Chat-Symbol unten rechts',
    'our-address': 'Unsere Adresse',
    'service-areas': 'Servicegebiete',
    'service-areas-desc': 'Berlin, München, Frankfurt, Hamburg und umliegende Metropolregionen',
    'view-all-areas': 'Alle Servicegebiete anzeigen',
    'business-hours': 'Geschäftszeiten',
    'customer-support-hours': 'Kundensupport: 8:00 - 18:00 Uhr',
    'cleaning-service-hours': 'Reinigungsdienstleistungen: 7:00 - 20:00 Uhr',
    'emergency-service': 'Notdienst: 24/7 verfügbar',
    
    // Contact Form
    'contact-form-title': 'Senden Sie uns eine Nachricht',
    'contact-form-subtitle': 'Füllen Sie das untenstehende Formular aus und wir melden uns so schnell wie möglich bei Ihnen.',
    'inquiry-type': 'Art der Anfrage',
    'general-question': 'Allgemeine Frage',
    'booking-inquiry': 'Buchungsanfrage',
    'service-feedback': 'Service-Feedback',
    'technical-support': 'Technischer Support',
    'partnership': 'Partnerschaft',
    'subject': 'Betreff',
    'message': 'Nachricht',
    'message-placeholder': 'Teilen Sie uns mit, wie wir Ihnen helfen können...',
    'send-message': 'Nachricht Senden',
    'sending': 'Wird gesendet...',
    'message-sent': 'Vielen Dank! Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns innerhalb von 24 Stunden bei Ihnen.',
    
    // FAQ Section
    'frequently-asked-questions': 'Häufig gestellte Fragen',
    'faq-1-question': 'Welche Gebiete bedienen Sie?',
    'faq-1-answer': 'Wir bedienen derzeit Berlin, München, Frankfurt, Hamburg und umliegende Gebiete. Geben Sie Ihre Postleitzahl in unser Buchungsformular ein, um zu prüfen, ob wir Ihren Standort bedienen.',
    'faq-2-question': 'Wie weit im Voraus sollte ich buchen?',
    'faq-2-answer': 'Wir empfehlen, mindestens 24-48 Stunden im Voraus für die reguläre Reinigung zu buchen. Für Same-Day- oder Next-Day-Service rufen Sie uns bitte direkt an unter +49 1577 2526898.',
    'faq-3-question': 'Was ist, wenn ich stornieren oder umbuchen muss?',
    'faq-3-answer': 'Sie können Ihren Termin bis zu 24 Stunden vor der geplanten Zeit ohne Gebühren stornieren oder umbuchen. Bei Stornierungen mit weniger als 24 Stunden Vorlaufzeit kann eine kleine Gebühr anfallen.',
    'faq-4-question': 'Muss ich Reinigungsmittel bereitstellen?',
    'faq-4-answer': 'Nein, unsere Reinigungsfachkräfte bringen alle notwendigen Materialien und Ausrüstung mit. Wenn Sie spezielle Produkte bevorzugen, die wir verwenden sollen, lassen Sie es uns bei der Buchung wissen.',
    'faq-5-question': 'Sind Ihre Reinigungskräfte versichert und hintergrundgeprüft?',
    'faq-5-answer': 'Ja, alle unsere Reinigungsfachkräfte sind gründlich hintergrundgeprüft, versichert und kautioniert. Wir priorisieren Ihre Sicherheit und Geborgenheit.',
    'faq-6-question': 'Welche Zahlungsmethoden akzeptieren Sie?',
    'faq-6-answer': 'Wir akzeptieren Kreditkarten, Debitkarten, Banküberweisungen und digitale Geldbörsen. Eine Anzahlung für die erste Stunde ist erforderlich, um Ihre Buchung zu bestätigen.',
  },
  de: {
    // Header
    'english-german-support': 'Englisch-Deutscher Support 7 Tage/Woche',
    'home': 'Startseite',
    'services': 'Dienstleistungen',
    'booking': 'Buchung',
    'contact': 'Kontakt',
    'login': 'Anmelden',
    'dashboard': 'Dashboard',
    'logout': 'Abmelden',
    
    // Home Page
    'hero-title': 'Buchen Sie eine zuverlässige Reinigungsfachkraft für Ihre Wohnung oder Ihr Büro',
    'hero-subtitle': 'Professionelle Reinigungsdienstleistungen mit englisch-deutschsprachigem Support 7 Tage die Woche',
    'book-now': 'Jetzt Buchen',
    'learn-more': 'Mehr Erfahren',
    'postal-code-title': 'Geben Sie Ihre Postleitzahl ein, um zu beginnen:',
    'postal-code-placeholder': 'z.B. 10115',
    
    // How it works section
    'how-it-works': 'Wie funktioniert es?',
    'step-1-title': 'Füllen Sie das Buchungsformular aus',
    'step-1-desc': 'Wählen Sie die Art der Reinigung, geben Sie Datum & Uhrzeit an und teilen Sie uns die Adresse Ihrer Immobilie mit. Sie können auch aus einer Reihe von Sonderwünschen wählen.',
    'step-2-title': 'Bezahlen Sie für die erste Stunde',
    'step-2-desc': 'Zur Bestätigung Ihrer Buchung ist eine Anzahlung für die erste Stunde erforderlich. Der gezahlte Betrag wird von der Endrechnung abgezogen.',
    'step-3-title': 'Lassen Sie Ihren Ort reinigen',
    'step-3-desc': 'Wir vermitteln Sie mit einer verifizierten Reinigungskraft, die Ihre Wohnung reinigt. Nach der Reinigung erhalten Sie eine Reinigungsübersicht.',
    
    // Services section
    'services-title': 'Reinigungsdienstleistungen für Zuhause & Büros',
    'basic-cleaning': 'Grundreinigung',
    'basic-cleaning-price': '€28,90/h',
    'basic-cleaning-desc': 'Zuverlässiger Haushaltsreinigungsservice. Gute Wahl, wenn Sie ein sauberes Zuhause erhalten möchten.',
    // Individual service features
    'basic-feature-1': 'Regelmäßige Unterhaltsreinigung',
    'basic-feature-2': 'Abstauben und Staubsaugen',
    'basic-feature-3': 'Küchen- und Badezimmerreinigung',
    'basic-feature-4': 'Müllentsorgung',
    'basic-feature-5': 'Reduzierter Preis für Abonnenten',
    
    'deep-cleaning': 'Tiefenreinigung',
    'deep-cleaning-price': '€45,00/h',
    'deep-cleaning-desc': 'Umfassende Reinigung für Ein-/Auszug oder nach Renovierung.',
    // Individual service features
    'deep-feature-1': 'Alles aus der Grundreinigung',
    'deep-feature-2': 'Tiefenreinigung der Badezimmer',
    'deep-feature-3': 'Ofen- und Kühlschrankreinigung innen',
    'deep-feature-4': 'Fußleisten und Fensterbänke',
    'deep-feature-5': 'Leuchten und Deckenventilatoren',
    
    'office-cleaning': 'Büroreinigung',
    'office-cleaning-price': '€35,00/h',
    'office-cleaning-desc': 'Maßgeschneiderte Reinigungslösungen für Ihren Arbeitsplatz.',
    // Individual service features
    'office-feature-1': 'Schreibtisch- und Arbeitsplatzdesinfektion',
    'office-feature-2': 'Konferenzraumreinigung',
    'office-feature-3': 'Küchen-/Pausenraumpflege',
    'office-feature-4': 'Toiletten-Tiefenreinigung',
    'office-feature-5': 'Gemeinschaftsbereichspflege',
    
    // Contact section
    'contact-section-title': 'Deutsch/Englischsprachiger Kundensupport 7 Tage/Woche',
    'contact-section-subtitle': 'Immer bereit zu helfen',
    'contact-phone-title': 'PER TELEFON',
    'contact-phone-info': '+49 1577 2526898\n8-18 Uhr (Montag - Sonntag)',
    'contact-email-title': 'PER E-MAIL',
    'contact-email-info': 'info@cleaningservice.de\n24/7 (jeden Tag)',
    'contact-chat-title': 'PER CHAT',
    'contact-chat-info': 'Chat auf unserer Website\n8-18 Uhr (Montag - Sonntag)',
    
    // Features Section
    'features-title': 'Finden Sie Ihre persönliche Hausreinigungskraft',
    'easy-booking-title': 'Einfache Online-Buchung',
    'easy-booking-desc': 'Sie können einen Hausreinigungsservice in nur 60 Sekunden mit unserem einfachen Buchungsformular buchen.',
    'background-checked-title': 'Überprüfter Hintergrund',
    'background-checked-desc': 'Alle Reinigungsdienstleister, die ihre Dienste auf unserer Website anbieten, sind hintergrundgeprüft und rechtlich registrierte Unternehmen.',
    'english-speaking-title': 'Englischsprachig',
    'english-speaking-desc': 'Sie können ohne Aufpreis eine englischsprachige Reinigungskraft wählen.',
    
    // Testimonials
    'testimonials-title': 'Über 20.000 zufriedene Kunden seit 2016',
    'testimonials-subtitle': 'Was unsere Kunden über unseren Service sagen?',
    'testimonial-1': 'Ich habe die Last-Minute-Option einen Tag vor der Reinigung gebucht. Alles war perfekt. 10/10',
    'testimonial-1-author': 'Sorel Mihai Arghire',
    'testimonial-2': 'Sehr guter Service. Wir nutzen ihre Reinigungskräfte jede Woche und sind sehr zufrieden mit dem Ergebnis. Sie sind sehr professionell und schnell. Ich kann sie nur empfehlen.',
    'testimonial-2-author': 'Jerneja Vrcek',
    'testimonial-3': 'Exzellenter Reinigungsservice, höchste Servicequalität und Effizienz. Außerdem ist der Kundensupport fantastisch. Ich werde sie allen empfehlen! 5 Sterne!!',
    'testimonial-3-author': 'Abigail Horn',
    
    // Services
    'our-services': 'Unsere Dienstleistungen',
    'residential-cleaning': 'Haushaltsreinigung',
    'commercial-cleaning': 'Gewerbereinigung',
    'deep-cleaning': 'Tiefenreinigung',
    'move-in-out': 'Ein-/Auszugsreinigung',
    
    // Booking
    'book-service': 'Service Buchen',
    'select-service': 'Service Auswählen',
    'choose-date': 'Datum Wählen',
    'choose-time': 'Zeit Wählen',
    'contact-details': 'Kontaktdaten',
    'booking-summary': 'Buchungsübersicht',
    'confirm-booking': 'Buchung Bestätigen',
    'first-name': 'Vorname',
    'last-name': 'Nachname',
    'email': 'E-Mail',
    'phone': 'Telefon',
    'address': 'Adresse',
    'postal-code': 'Postleitzahl',
    'special-requests': 'Besondere Wünsche',
    
    // Success Page
    'booking-confirmed': 'Buchung Bestätigt!',
    'booking-success-message': 'Ihr Reinigungsservice wurde erfolgreich gebucht!',
    'booking-details': 'Ihre Buchungsdetails',
    'booking-id': 'Buchungs-ID',
    'service': 'Service',
    'date': 'Datum',
    'time': 'Zeit',
    'location': 'Standort',
    'exclusive-bonus': 'Exklusiver Erstkundenbonus!',
    'welcome-offer': 'Vielen Dank, dass Sie unseren Service gewählt haben! Als Willkommensgeschenk erhalten Sie 20% Rabatt auf Ihre nächste Buchung!',
    'promo-code': 'Code verwenden: WELCOME20',
    'what-happens-next': 'Was passiert als Nächstes?',
    'view-dashboard': 'Dashboard Anzeigen',
    'book-another': 'Weiteren Service Buchen',
    'contact-support': 'Support Kontaktieren',
    'call-us': 'Uns Anrufen',
    
    // Dashboard
    'welcome-back': 'Willkommen zurück',
    'your-dashboard': 'Ihr Dashboard',
    'upcoming-bookings': 'Bevorstehende Buchungen',
    'booking-history': 'Buchungsverlauf',
    'account-settings': 'Kontoeinstellungen',
    'view-details': 'Details Anzeigen',
    'cancel-booking': 'Buchung Stornieren',
    'no-upcoming-bookings': 'Keine bevorstehenden Buchungen',
    'no-booking-history': 'Noch kein Buchungsverlauf',
    
    // Detailed Services Page
    'our-cleaning-services': 'Unsere Reinigungsdienstleistungen',
    'professional-solutions-subtitle': 'Professionelle Reinigungslösungen, die auf Ihre Bedürfnisse zugeschnitten sind. Alle Dienstleistungen umfassen hintergrundgeprüfte Reinigungskräfte und Zufriedenheitsgarantie.',
    'service-comparison': 'Service-Vergleich',
    'features': 'Funktionen',
    'why-choose-services': 'Warum unsere Dienstleistungen wählen?',
    'quick-efficient': 'Schnell & Effizient',
    'quick-efficient-desc': 'Unsere geschulten Fachkräfte arbeiten effizient, um Ihren Raum zu reinigen, ohne Ihren Zeitplan zu unterbrechen.',
    'fully-insured': 'Vollversichert',
    'fully-insured-desc': 'Alle unsere Reinigungskräfte sind hintergrundgeprüft, versichert und kautioniert für Ihre Sicherheit.',
    'flexible-scheduling': 'Flexible Terminplanung',
    'flexible-scheduling-detailed': 'Buchen Sie einmalige Reinigungen oder richten Sie regelmäßigen Service ein. Wir arbeiten nach Ihrem Zeitplan.',
    
    // Service Details
    'basic-cleaning-detailed': 'Perfekt für regelmäßige Wartung und um Ihr Zuhause durchgehend sauber zu halten. Unser Grundreinigungsservice deckt alle wesentlichen Bereiche ab.',
    'basic-duration': '2-3 Stunden',
    'basic-ideal': 'Regelmäßige Wartung',
    'basic-features': [
      'Abstauben und Oberflächen wischen',
      'Alle Böden staubsaugen',
      'Küchenreinigung (Arbeitsplatten, Spülbecken, Geräte)',
      'Badezimmerreinigung und Desinfektion',
      'Müllentsorgung',
      'Betten machen',
      'Allgemeines Aufräumen'
    ],
    
    'deep-cleaning-detailed': 'Umfassende Reinigung für Ein-/Auszug oder wenn Sie eine gründliche Auffrischung benötigen. Umfasst alles aus der Grundreinigung plus Detailarbeit.',
    'deep-duration': '4-6 Stunden',
    'deep-ideal': 'Ein-/Auszug, Frühjahrsputz',
    'deep-features': [
      'Alles aus der Grundreinigung',
      'Tiefenreinigung der Badezimmer',
      'Ofen- und Kühlschrankreinigung innen',
      'Fußleisten und Fensterbänke',
      'Leuchten und Deckenventilatoren',
      'Fensterreinigung innen',
      'Schrankfronten und Schubladen'
    ],
    
    'office-cleaning-detailed': 'Professionelle Reinigungslösungen, die auf Ihren Arbeitsplatz zugeschnitten sind. Schaffen Sie eine gesunde und produktive Umgebung für Ihr Team.',
    'office-duration': '2-4 Stunden',
    'office-ideal': 'Kleine bis mittlere Büros',
    'office-features': [
      'Schreibtisch- und Arbeitsplatzdesinfektion',
      'Konferenzraumreinigung',
      'Küchen-/Pausenraumpflege',
      'Toiletten-Tiefenreinigung',
      'Bodenstaubsaugen und wischen',
      'Müll- und Recyclingentsorgung',
      'Gemeinschaftsbereichspflege'
    ],
    
    // Comparison Table
    'dusting-surface-cleaning': 'Abstauben & Oberflächenreinigung',
    'vacuuming': 'Staubsaugen',
    'kitchen-cleaning': 'Küchenreinigung',
    'bathroom-sanitizing': 'Badezimmerdesinfektion',
    'trash-removal': 'Müllentsorgung',
    'inside-appliances': 'Geräte innen',
    'baseboards-details': 'Fußleisten & Details',
    'window-cleaning-interior': 'Fensterreinigung (innen)',
    'workspace-sanitizing': 'Arbeitsplatzdesinfektion',
    'conference-room-setup': 'Konferenzraumeinrichtung',
    
    'book-service-type': '{service} Buchen',
    'duration': 'Dauer',
    'ideal-for': 'Ideal für',
    
    // Common
    'loading': 'Laden...',
    'submit': 'Senden',
    'cancel': 'Abbrechen',
    'edit': 'Bearbeiten',
    'save': 'Speichern',
    'delete': 'Löschen',
    'yes': 'Ja',
    'no': 'Nein',
    'back': 'Zurück',
    'next': 'Weiter',
    'previous': 'Zurück',
    'close': 'Schließen',
    
    // Booking Page Detailed
    'book-cleaning-service': 'Einen Reinigungsservice Buchen',
    'quick-easy-booking': 'Schnelle und einfache Buchung in nur wenigen Schritten',
    'step-1': 'Schritt 1',
    'step-2': 'Schritt 2',
    'step-3': 'Schritt 3', 
    'step-4': 'Schritt 4',
    'select-service-step': 'Service Auswählen',
    'choose-date-time': 'Datum & Zeit',
    'contact-details-step': 'Kontaktdaten',
    'confirm-book': 'Bestätigen & Buchen',
    
    // Service Selection
    'choose-service-type': 'Wählen Sie Ihren Service-Typ',
    'basic-cleaning-booking': 'Grundreinigung',
    'basic-cleaning-booking-desc': 'Regelmäßige Unterhaltsreinigung, Abstauben, Staubsaugen, Küchen- und Badezimmerreinigung',
    'deep-cleaning-booking': 'Tiefenreinigung',
    'deep-cleaning-booking-desc': 'Umfassende Reinigung, Baustellenreinigung, tiefe Küchen- und Badezimmerreinigung',
    'office-cleaning-booking': 'Büroreinigung',
    'office-cleaning-booking-desc': 'Maßgeschneiderte Reinigungslösungen für Ihren Arbeitsplatz',
    'per-hour': '/Stunde',
    'estimated-duration': 'Geschätzte Dauer',
    'hours': 'Stunden',
    
    // Date & Time Selection
    'select-date-time': 'Wählen Sie Ihr bevorzugtes Datum und Ihre Zeit',
    'available-times': 'Verfügbare Zeiten',
    'no-available-slots': 'Keine verfügbaren Zeitfenster für dieses Datum',
    'select-different-date': 'Bitte wählen Sie ein anderes Datum',
    
    // Contact Form
    'your-contact-information': 'Ihre Kontaktinformationen',
    'full-name': 'Vollständiger Name',
    'email-address': 'E-Mail-Adresse',
    'phone-number': 'Telefonnummer',
    'full-address': 'Vollständige Adresse',
    'additional-notes': 'Zusätzliche Notizen',
    'special-instructions': 'Besondere Anweisungen oder Wünsche',
    
    // Booking Summary
    'booking-summary-title': 'Buchungsübersicht',
    'selected-service': 'Ausgewählter Service',
    'scheduled-date': 'Geplantes Datum',
    'scheduled-time': 'Geplante Zeit',
    'customer-info': 'Kundeninformationen',
    'total-estimated-cost': 'Geschätzte Gesamtkosten',
    'deposit-required': 'Erforderliche Anzahlung (Erste Stunde)',
    'remaining-balance': 'Verbleibendes Guthaben',
    'paid-after-service': 'Nach Abschluss des Services zu zahlen',
    
    // Buttons & Actions
    'continue': 'Weiter',
    'go-back': 'Zurück',
    'book-service-now': 'Service Jetzt Buchen',
    'processing': 'Wird verarbeitet...',
    
    // Validation Messages
    'required-field': 'Dieses Feld ist erforderlich',
    'invalid-email': 'Bitte geben Sie eine gültige E-Mail-Adresse ein',
    'invalid-phone': 'Bitte geben Sie eine gültige Telefonnummer ein',
    'select-service-first': 'Bitte wählen Sie zuerst einen Service',
    'select-date-first': 'Bitte wählen Sie zuerst ein Datum',
    'select-time-first': 'Bitte wählen Sie zuerst eine Zeit',
    
    // Contact Page
    'contact-us': 'Kontakt',
    'contact-page-subtitle': 'Nehmen Sie Kontakt mit unserem freundlichen Team auf. Wir helfen Ihnen gerne bei allen Fragen zu unseren Reinigungsdienstleistungen.',
    'get-in-touch': 'Kontakt aufnehmen',
    'phone-support': 'Telefon-Support',
    'phone-support-desc': 'Sprechen Sie direkt mit unserem Kundenservice-Team',
    'email-support': 'E-Mail-Support',
    'email-support-desc': 'Senden Sie uns jederzeit eine Nachricht',
    'email-response-time': 'Wir antworten innerhalb von 24 Stunden',
    'live-chat': 'Live-Chat',
    'live-chat-desc': 'Chatten Sie direkt mit uns auf unserer Website',
    'chat-instructions': 'Klicken Sie auf das Chat-Symbol unten rechts',
    'our-address': 'Unsere Adresse',
    'service-areas': 'Servicegebiete',
    'service-areas-desc': 'Berlin, München, Frankfurt, Hamburg und umliegende Metropolregionen',
    'view-all-areas': 'Alle Servicegebiete anzeigen',
    'business-hours': 'Geschäftszeiten',
    'customer-support-hours': 'Kundensupport: 8:00 - 18:00 Uhr',
    'cleaning-service-hours': 'Reinigungsdienstleistungen: 7:00 - 20:00 Uhr',
    'emergency-service': 'Notdienst: 24/7 verfügbar',
    
    // Contact Form
    'contact-form-title': 'Senden Sie uns eine Nachricht',
    'contact-form-subtitle': 'Füllen Sie das untenstehende Formular aus und wir melden uns so schnell wie möglich bei Ihnen.',
    'inquiry-type': 'Art der Anfrage',
    'general-question': 'Allgemeine Frage',
    'booking-inquiry': 'Buchungsanfrage',
    'service-feedback': 'Service-Feedback',
    'technical-support': 'Technischer Support',
    'partnership': 'Partnerschaft',
    'subject': 'Betreff',
    'message': 'Nachricht',
    'message-placeholder': 'Teilen Sie uns mit, wie wir Ihnen helfen können...',
    'send-message': 'Nachricht Senden',
    'sending': 'Wird gesendet...',
    'message-sent': 'Vielen Dank! Ihre Nachricht wurde erfolgreich gesendet. Wir melden uns innerhalb von 24 Stunden bei Ihnen.',
    
    // FAQ Section
    'frequently-asked-questions': 'Häufig gestellte Fragen',
    'faq-1-question': 'Welche Gebiete bedienen Sie?',
    'faq-1-answer': 'Wir bedienen derzeit Berlin, München, Frankfurt, Hamburg und umliegende Gebiete. Geben Sie Ihre Postleitzahl in unser Buchungsformular ein, um zu prüfen, ob wir Ihren Standort bedienen.',
    'faq-2-question': 'Wie weit im Voraus sollte ich buchen?',
    'faq-2-answer': 'Wir empfehlen, mindestens 24-48 Stunden im Voraus für die reguläre Reinigung zu buchen. Für Same-Day- oder Next-Day-Service rufen Sie uns bitte direkt an unter +49 1577 2526898.',
    'faq-3-question': 'Was ist, wenn ich stornieren oder umbuchen muss?',
    'faq-3-answer': 'Sie können Ihren Termin bis zu 24 Stunden vor der geplanten Zeit ohne Gebühren stornieren oder umbuchen. Bei Stornierungen mit weniger als 24 Stunden Vorlaufzeit kann eine kleine Gebühr anfallen.',
    'faq-4-question': 'Muss ich Reinigungsmittel bereitstellen?',
    'faq-4-answer': 'Nein, unsere Reinigungsfachkräfte bringen alle notwendigen Materialien und Ausrüstung mit. Wenn Sie spezielle Produkte bevorzugen, die wir verwenden sollen, lassen Sie es uns bei der Buchung wissen.',
    'faq-5-question': 'Sind Ihre Reinigungskräfte versichert und hintergrundgeprüft?',
    'faq-5-answer': 'Ja, alle unsere Reinigungsfachkräfte sind gründlich hintergrundgeprüft, versichert und kautioniert. Wir priorisieren Ihre Sicherheit und Geborgenheit.',
    'faq-6-question': 'Welche Zahlungsmethoden akzeptieren Sie?',
    'faq-6-answer': 'Wir akzeptieren Kreditkarten, Debitkarten, Banküberweisungen und digitale Geldbörsen. Eine Anzahlung für die erste Stunde ist erforderlich, um Ihre Buchung zu bestätigen.',
  }
};

export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');

  // Load saved language from localStorage
  useEffect(() => {
    const savedLanguage = localStorage.getItem('preferredLanguage');
    if (savedLanguage && (savedLanguage === 'en' || savedLanguage === 'de')) {
      setCurrentLanguage(savedLanguage);
    }
  }, []);

  // Save language to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('preferredLanguage', currentLanguage);
  }, [currentLanguage]);

  const changeLanguage = (language) => {
    if (language === 'en' || language === 'de') {
      setCurrentLanguage(language);
    }
  };

  const t = (key) => {
    return translations[currentLanguage][key] || key;
  };

  const value = {
    currentLanguage,
    changeLanguage,
    t,
    translations: translations[currentLanguage]
  };

  return (
    <LanguageContext.Provider value={value}>
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
