const express = require('express');
const { body, validationResult } = require('express-validator');
const jwt = require('jsonwebtoken');
const db = require('../config/database');

const router = express.Router();
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

// Middleware to verify JWT token
const authenticateToken = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'Access denied. No token provided.' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(403).json({ error: 'Invalid token.' });
  }
};

// Create a new booking
router.post('/', authenticateToken, [
  body('serviceTypeId').isInt(),
  body('postalCode').trim().isLength({ min: 5 }),
  body('address').trim().isLength({ min: 5 }),
  body('bookingDate').isISO8601(),
  body('bookingTime').matches(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/),
  body('duration').isInt({ min: 1 }),
  body('totalPrice').isFloat({ min: 0 })
], (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        error: 'Validation failed',
        details: errors.array()
      });
    }

    const {
      serviceTypeId,
      postalCode,
      address,
      bookingDate,
      bookingTime,
      duration,
      totalPrice,
      specialInstructions
    } = req.body;

    const userId = req.user.userId;
    const depositAmount = totalPrice * 0.3; // 30% deposit

    // Find available cleaner for the postal code and time
    db.all(`
      SELECT * FROM cleaners 
      WHERE postal_codes LIKE ? 
      AND available = 1 
      AND background_checked = 1
      ORDER BY rating DESC
    `, [`%${postalCode.substring(0, 5)}%`], (err, cleaners) => {
      if (err) {
        console.error('Database error:', err);
        return res.status(500).json({ error: 'Database error' });
      }

      // For demo purposes, assign the first available cleaner
      const cleanerId = cleaners.length > 0 ? cleaners[0].id : null;

      const stmt = db.prepare(`
        INSERT INTO bookings (
          user_id, service_type_id, cleaner_id, postal_code, address,
          booking_date, booking_time, duration, total_price, deposit_amount,
          special_instructions, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
      `);

      stmt.run([
        userId, serviceTypeId, cleanerId, postalCode, address,
        bookingDate, bookingTime, duration, totalPrice, depositAmount,
        specialInstructions
      ], function(err) {
        if (err) {
          console.error('Error creating booking:', err);
          return res.status(500).json({ error: 'Failed to create booking' });
        }

        const bookingId = this.lastID;

        // Get the complete booking with service and cleaner details
        db.get(`
          SELECT 
            b.*,
            st.name as service_name,
            st.description as service_description,
            c.first_name as cleaner_first_name,
            c.last_name as cleaner_last_name,
            c.phone as cleaner_phone,
            c.rating as cleaner_rating
          FROM bookings b
          LEFT JOIN service_types st ON b.service_type_id = st.id
          LEFT JOIN cleaners c ON b.cleaner_id = c.id
          WHERE b.id = ?
        `, [bookingId], (err, booking) => {
          if (err) {
            console.error('Error fetching booking:', err);
            return res.status(500).json({ error: 'Booking created but failed to fetch details' });
          }

          res.status(201).json({
            message: 'Booking created successfully',
            booking: {
              id: booking.id,
              serviceType: {
                id: booking.service_type_id,
                name: booking.service_name,
                description: booking.service_description
              },
              cleaner: booking.cleaner_id ? {
                id: booking.cleaner_id,
                name: `${booking.cleaner_first_name} ${booking.cleaner_last_name}`,
                phone: booking.cleaner_phone,
                rating: booking.cleaner_rating
              } : null,
              postalCode: booking.postal_code,
              address: booking.address,
              date: booking.booking_date,
              time: booking.booking_time,
              duration: booking.duration,
              totalPrice: booking.total_price,
              depositAmount: booking.deposit_amount,
              specialInstructions: booking.special_instructions,
              status: booking.status,
              createdAt: booking.created_at
            }
          });
        });
      });

      stmt.finalize();
    });
  } catch (error) {
    console.error('Booking creation error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Get user's bookings
router.get('/my-bookings', authenticateToken, (req, res) => {
  const userId = req.user.userId;
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const offset = (page - 1) * limit;

  db.all(`
    SELECT 
      b.*,
      st.name as service_name,
      st.description as service_description,
      st.base_price,
      c.first_name as cleaner_first_name,
      c.last_name as cleaner_last_name,
      c.phone as cleaner_phone,
      c.rating as cleaner_rating
    FROM bookings b
    LEFT JOIN service_types st ON b.service_type_id = st.id
    LEFT JOIN cleaners c ON b.cleaner_id = c.id
    WHERE b.user_id = ?
    ORDER BY b.created_at DESC
    LIMIT ? OFFSET ?
  `, [userId, limit, offset], (err, bookings) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    const formattedBookings = bookings.map(booking => ({
      id: booking.id,
      serviceType: {
        id: booking.service_type_id,
        name: booking.service_name,
        description: booking.service_description,
        basePrice: booking.base_price
      },
      cleaner: booking.cleaner_id ? {
        id: booking.cleaner_id,
        name: `${booking.cleaner_first_name} ${booking.cleaner_last_name}`,
        phone: booking.cleaner_phone,
        rating: booking.cleaner_rating
      } : null,
      postalCode: booking.postal_code,
      address: booking.address,
      date: booking.booking_date,
      time: booking.booking_time,
      duration: booking.duration,
      totalPrice: booking.total_price,
      depositAmount: booking.deposit_amount,
      specialInstructions: booking.special_instructions,
      status: booking.status,
      paymentStatus: booking.payment_status,
      createdAt: booking.created_at,
      updatedAt: booking.updated_at
    }));

    res.json({
      bookings: formattedBookings,
      pagination: {
        page,
        limit,
        total: bookings.length
      }
    });
  });
});

// Get specific booking
router.get('/:id', authenticateToken, (req, res) => {
  const bookingId = req.params.id;
  const userId = req.user.userId;

  db.get(`
    SELECT 
      b.*,
      st.name as service_name,
      st.description as service_description,
      st.base_price,
      c.first_name as cleaner_first_name,
      c.last_name as cleaner_last_name,
      c.phone as cleaner_phone,
      c.email as cleaner_email,
      c.rating as cleaner_rating,
      c.experience_years
    FROM bookings b
    LEFT JOIN service_types st ON b.service_type_id = st.id
    LEFT JOIN cleaners c ON b.cleaner_id = c.id
    WHERE b.id = ? AND b.user_id = ?
  `, [bookingId, userId], (err, booking) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    if (!booking) {
      return res.status(404).json({ error: 'Booking not found' });
    }

    res.json({
      id: booking.id,
      serviceType: {
        id: booking.service_type_id,
        name: booking.service_name,
        description: booking.service_description,
        basePrice: booking.base_price
      },
      cleaner: booking.cleaner_id ? {
        id: booking.cleaner_id,
        name: `${booking.cleaner_first_name} ${booking.cleaner_last_name}`,
        phone: booking.cleaner_phone,
        email: booking.cleaner_email,
        rating: booking.cleaner_rating,
        experienceYears: booking.experience_years
      } : null,
      postalCode: booking.postal_code,
      address: booking.address,
      date: booking.booking_date,
      time: booking.booking_time,
      duration: booking.duration,
      totalPrice: booking.total_price,
      depositAmount: booking.deposit_amount,
      specialInstructions: booking.special_instructions,
      status: booking.status,
      paymentStatus: booking.payment_status,
      createdAt: booking.created_at,
      updatedAt: booking.updated_at
    });
  });
});

// Update booking status (cancel, reschedule)
router.patch('/:id', authenticateToken, [
  body('status').optional().isIn(['pending', 'confirmed', 'completed', 'cancelled']),
  body('bookingDate').optional().isISO8601(),
  body('bookingTime').optional().matches(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
], (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      error: 'Validation failed',
      details: errors.array()
    });
  }

  const bookingId = req.params.id;
  const userId = req.user.userId;
  const updates = req.body;

  // First check if booking belongs to user
  db.get('SELECT * FROM bookings WHERE id = ? AND user_id = ?', [bookingId, userId], (err, booking) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    if (!booking) {
      return res.status(404).json({ error: 'Booking not found' });
    }

    // Build update query dynamically
    const updateFields = [];
    const updateValues = [];

    if (updates.status) {
      updateFields.push('status = ?');
      updateValues.push(updates.status);
    }

    if (updates.bookingDate) {
      updateFields.push('booking_date = ?');
      updateValues.push(updates.bookingDate);
    }

    if (updates.bookingTime) {
      updateFields.push('booking_time = ?');
      updateValues.push(updates.bookingTime);
    }

    if (updateFields.length === 0) {
      return res.status(400).json({ error: 'No valid fields to update' });
    }

    updateFields.push('updated_at = CURRENT_TIMESTAMP');
    updateValues.push(bookingId);

    const updateQuery = `UPDATE bookings SET ${updateFields.join(', ')} WHERE id = ?`;

    db.run(updateQuery, updateValues, function(err) {
      if (err) {
        console.error('Error updating booking:', err);
        return res.status(500).json({ error: 'Failed to update booking' });
      }

      res.json({
        message: 'Booking updated successfully',
        changes: this.changes
      });
    });
  });
});

// Delete booking (only if pending)
router.delete('/:id', authenticateToken, (req, res) => {
  const bookingId = req.params.id;
  const userId = req.user.userId;

  // Check if booking belongs to user and is pending
  db.get('SELECT * FROM bookings WHERE id = ? AND user_id = ? AND status = "pending"', [bookingId, userId], (err, booking) => {
    if (err) {
      console.error('Database error:', err);
      return res.status(500).json({ error: 'Database error' });
    }

    if (!booking) {
      return res.status(404).json({ error: 'Booking not found or cannot be deleted' });
    }

    db.run('DELETE FROM bookings WHERE id = ?', [bookingId], function(err) {
      if (err) {
        console.error('Error deleting booking:', err);
        return res.status(500).json({ error: 'Failed to delete booking' });
      }

      res.json({
        message: 'Booking deleted successfully'
      });
    });
  });
});

module.exports = router;
