const express = require('express');
const db = require('../config/database');
const rateLimit = require('express-rate-limit');

const router = express.Router();

// Rate limiting for contact form
const contactLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 3, // limit each IP to 3 contact form submissions per windowMs
  message: { error: 'Too many contact form submissions, please try again later.' }
});

// Submit contact form
router.post('/submit', contactLimiter, (req, res) => {
  try {
    const { name, email, phone, subject, message, service_interest } = req.body;
    
    // Validation
    if (!name || !email || !message) {
      return res.status(400).json({ 
        error: 'Name, email, and message are required' 
      });
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ error: 'Please provide a valid email address' });
    }
    
    // Message length validation
    if (message.length < 10) {
      return res.status(400).json({ 
        error: 'Message must be at least 10 characters long' 
      });
    }
    
    if (message.length > 1000) {
      return res.status(400).json({ 
        error: 'Message must be less than 1000 characters' 
      });
    }
    
    // Insert contact message
    const stmt = db.prepare(`
      INSERT INTO contact_messages (
        name, email, phone, subject, message, service_interest, 
        status, created_at
      ) VALUES (?, ?, ?, ?, ?, ?, 'new', ?)
    `);
    
    const result = stmt.run(
      name.trim(),
      email.trim().toLowerCase(),
      phone ? phone.trim() : null,
      subject ? subject.trim() : null,
      message.trim(),
      service_interest || null,
      new Date().toISOString()
    );
    
    res.status(201).json({ 
      message: 'Thank you for your message! We will get back to you soon.',
      id: result.lastInsertRowid
    });
  } catch (error) {
    console.error('Error submitting contact form:', error);
    res.status(500).json({ error: 'Server error. Please try again later.' });
  }
});

// Get contact messages (admin only - you might want to add admin auth middleware)
router.get('/messages', (req, res) => {
  try {
    const { page = 1, limit = 20, status } = req.query;
    const offset = (page - 1) * limit;
    
    let whereClause = '';
    let params = [];
    
    if (status) {
      whereClause = 'WHERE status = ?';
      params.push(status);
    }
    
    const stmt = db.prepare(`
      SELECT 
        id, name, email, phone, subject, message, service_interest,
        status, created_at
      FROM contact_messages
      ${whereClause}
      ORDER BY created_at DESC
      LIMIT ? OFFSET ?
    `);
    
    const messages = stmt.all(...params, limit, offset);
    
    // Get total count for pagination
    const countStmt = db.prepare(`
      SELECT COUNT(*) as total FROM contact_messages ${whereClause}
    `);
    const { total } = countStmt.get(...params);
    
    res.json({
      messages,
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total,
        totalPages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    console.error('Error fetching contact messages:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Update message status (admin only)
router.put('/messages/:id/status', (req, res) => {
  try {
    const { id } = req.params;
    const { status } = req.body;
    
    // Validation
    const validStatuses = ['new', 'in_progress', 'resolved', 'closed'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({ 
        error: 'Invalid status. Must be one of: ' + validStatuses.join(', ')
      });
    }
    
    const stmt = db.prepare(`
      UPDATE contact_messages 
      SET status = ?, updated_at = ?
      WHERE id = ?
    `);
    
    const result = stmt.run(status, new Date().toISOString(), id);
    
    if (result.changes === 0) {
      return res.status(404).json({ error: 'Message not found' });
    }
    
    res.json({ message: 'Message status updated successfully' });
  } catch (error) {
    console.error('Error updating message status:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Get message by ID (admin only)
router.get('/messages/:id', (req, res) => {
  try {
    const { id } = req.params;
    
    const stmt = db.prepare(`
      SELECT 
        id, name, email, phone, subject, message, service_interest,
        status, created_at, updated_at
      FROM contact_messages
      WHERE id = ?
    `);
    
    const message = stmt.get(id);
    
    if (!message) {
      return res.status(404).json({ error: 'Message not found' });
    }
    
    res.json(message);
  } catch (error) {
    console.error('Error fetching message:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Delete message (admin only)
router.delete('/messages/:id', (req, res) => {
  try {
    const { id } = req.params;
    
    const stmt = db.prepare('DELETE FROM contact_messages WHERE id = ?');
    const result = stmt.run(id);
    
    if (result.changes === 0) {
      return res.status(404).json({ error: 'Message not found' });
    }
    
    res.json({ message: 'Message deleted successfully' });
  } catch (error) {
    console.error('Error deleting message:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Get contact statistics (admin only)
router.get('/stats', (req, res) => {
  try {
    const statsStmt = db.prepare(`
      SELECT 
        COUNT(*) as total_messages,
        COUNT(CASE WHEN status = 'new' THEN 1 END) as new_messages,
        COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_messages,
        COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved_messages,
        COUNT(CASE WHEN status = 'closed' THEN 1 END) as closed_messages,
        COUNT(CASE WHEN created_at >= date('now', '-7 days') THEN 1 END) as messages_this_week,
        COUNT(CASE WHEN created_at >= date('now', '-30 days') THEN 1 END) as messages_this_month
      FROM contact_messages
    `);
    
    const stats = statsStmt.get();
    
    // Get service interest breakdown
    const serviceInterestStmt = db.prepare(`
      SELECT 
        service_interest,
        COUNT(*) as count
      FROM contact_messages
      WHERE service_interest IS NOT NULL
      GROUP BY service_interest
      ORDER BY count DESC
    `);
    
    const serviceInterests = serviceInterestStmt.all();
    
    res.json({
      ...stats,
      service_interests: serviceInterests
    });
  } catch (error) {
    console.error('Error fetching contact statistics:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
