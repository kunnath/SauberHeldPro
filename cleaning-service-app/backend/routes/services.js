const express = require('express');
const db = require('../config/database');

const router = express.Router();

// Get all active service types
router.get('/', (req, res) => {
  db.all('SELECT * FROM service_types WHERE is_active = 1 ORDER BY name', (err, services) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    const formattedServices = services.map(service => ({
      id: service.id,
      name: service.name,
      description: service.description,
      basePrice: service.base_price,
      durationMinutes: service.duration_minutes,
      category: service.category,
      features: service.features ? JSON.parse(service.features) : [],
      isActive: service.is_active,
      createdAt: service.created_at
    }));

    res.json({
      services: formattedServices
    });
  });
});

// Get specific service type
router.get('/:id', (req, res) => {
  const serviceId = req.params.id;

  db.get('SELECT * FROM service_types WHERE id = ? AND active = 1', [serviceId], (err, service) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    if (!service) {
      return res.status(404).json({ error: 'Service not found' });
    }

    res.json({
      id: service.id,
      name: service.name,
      description: service.description,
      basePrice: service.base_price,
      durationMinutes: service.duration_minutes,
      category: service.category,
      features: service.features ? JSON.parse(service.features) : [],
      active: service.active,
      createdAt: service.created_at
    });
  });
});

// Get available cleaners for a postal code
router.get('/cleaners/:postalCode', (req, res) => {
  const postalCode = req.params.postalCode;
  const date = req.query.date;
  const time = req.query.time;

  db.all(`
    SELECT 
      id, first_name, last_name, rating, experience_years, 
      languages, hourly_rate, total_jobs
    FROM cleaners 
    WHERE postal_codes LIKE ? 
    AND available = 1 
    AND background_checked = 1
    ORDER BY rating DESC, total_jobs DESC
  `, [`%${postalCode.substring(0, 5)}%`], (err, cleaners) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    // If date and time are provided, filter out busy cleaners
    if (date && time) {
      // For demo purposes, assume all cleaners are available
      // In a real app, you'd check against existing bookings
    }

    const formattedCleaners = cleaners.map(cleaner => ({
      id: cleaner.id,
      name: `${cleaner.first_name} ${cleaner.last_name}`,
      rating: cleaner.rating,
      experienceYears: cleaner.experience_years,
      languages: cleaner.languages ? cleaner.languages.split(',') : ['German'],
      hourlyRate: cleaner.hourly_rate,
      totalJobs: cleaner.total_jobs
    }));

    res.json({
      cleaners: formattedCleaners,
      available: formattedCleaners.length > 0
    });
  });
});

// Get service availability for a specific date and postal code
router.get('/availability/:postalCode/:date', (req, res) => {
  const { postalCode, date } = req.params;
  
  // For demo purposes, generate available time slots
  const timeSlots = [
    '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00'
  ];

  // Check existing bookings for this date and postal code area
  db.all(`
    SELECT booking_time, COUNT(*) as bookings_count
    FROM bookings 
    WHERE booking_date = ? 
    AND postal_code LIKE ?
    AND status IN ('pending', 'confirmed')
    GROUP BY booking_time
  `, [date, `${postalCode.substring(0, 3)}%`], (err, existingBookings) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    // Create a map of busy time slots
    const busySlots = {};
    existingBookings.forEach(booking => {
      busySlots[booking.booking_time] = booking.bookings_count;
    });

    // For demo, assume max 3 cleaners can work at the same time
    const maxConcurrentBookings = 3;

    const availableSlots = timeSlots.map(time => ({
      time,
      available: (busySlots[time] || 0) < maxConcurrentBookings,
      availableCleaners: maxConcurrentBookings - (busySlots[time] || 0)
    }));

    res.json({
      date,
      postalCode,
      timeSlots: availableSlots
    });
  });
});

// Get service pricing for postal code
router.get('/pricing/:serviceId/:postalCode', (req, res) => {
  const { serviceId, postalCode } = req.params;
  const duration = parseInt(req.query.duration) || 2; // default 2 hours

  db.get('SELECT * FROM service_types WHERE id = ?', [serviceId], (err, service) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    if (!service) {
      return res.status(404).json({ error: 'Service not found' });
    }

    // Calculate pricing (could include postal code-based surcharges)
    const basePrice = service.base_price;
    const totalPrice = basePrice * duration;
    const depositAmount = totalPrice * 0.3; // 30% deposit

    // Potential surcharges based on postal code
    let surcharge = 0;
    const postalCodeNum = parseInt(postalCode);
    
    // Example: premium areas have a small surcharge
    if (postalCodeNum >= 10115 && postalCodeNum <= 10117) {
      surcharge = 5; // €5 premium area surcharge
    }

    const finalPrice = totalPrice + surcharge;

    res.json({
      service: {
        id: service.id,
        name: service.name,
        basePrice: service.base_price
      },
      pricing: {
        basePrice,
        duration,
        subtotal: totalPrice,
        surcharge,
        totalPrice: finalPrice,
        depositAmount: finalPrice * 0.3,
        remainingAmount: finalPrice * 0.7
      },
      postalCode
    });
  });
});

// Get all cleaners
router.get('/cleaners', (req, res) => {
  db.all('SELECT * FROM cleaners WHERE is_available = 1 ORDER BY rating DESC', (err, cleaners) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    const formattedCleaners = cleaners.map(cleaner => ({
      id: cleaner.id,
      firstName: cleaner.first_name,
      lastName: cleaner.last_name,
      email: cleaner.email,
      phone: cleaner.phone,
      specialties: cleaner.specialties,
      rating: cleaner.rating,
      experienceYears: cleaner.experience_years,
      hourlyRate: cleaner.hourly_rate,
      bio: cleaner.bio,
      isAvailable: cleaner.is_available,
      createdAt: cleaner.created_at
    }));

    res.json({
      cleaners: formattedCleaners
    });
  });
});

module.exports = router;
