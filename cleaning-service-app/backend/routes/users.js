const express = require('express');
const bcrypt = require('bcryptjs');
const db = require('../config/database');
const auth = require('../middleware/auth');

const router = express.Router();

// Get user profile
router.get('/profile', auth, (req, res) => {
  try {
    const stmt = db.prepare(`
      SELECT id, email, first_name, last_name, phone, address, created_at 
      FROM users WHERE id = ?
    `);
    const user = stmt.get(req.userId);
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json(user);
  } catch (error) {
    console.error('Error fetching user profile:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Update user profile
router.put('/profile', auth, (req, res) => {
  try {
    const { first_name, last_name, phone, address } = req.body;
    
    // Validation
    if (!first_name || !last_name) {
      return res.status(400).json({ error: 'First name and last name are required' });
    }
    
    const stmt = db.prepare(`
      UPDATE users 
      SET first_name = ?, last_name = ?, phone = ?, address = ?, updated_at = ?
      WHERE id = ?
    `);
    
    const result = stmt.run(
      first_name,
      last_name,
      phone || null,
      address || null,
      new Date().toISOString(),
      req.userId
    );
    
    if (result.changes === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    // Return updated user data
    const userStmt = db.prepare(`
      SELECT id, email, first_name, last_name, phone, address, created_at 
      FROM users WHERE id = ?
    `);
    const updatedUser = userStmt.get(req.userId);
    
    res.json({ 
      message: 'Profile updated successfully',
      user: updatedUser
    });
  } catch (error) {
    console.error('Error updating user profile:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Change password
router.put('/change-password', auth, async (req, res) => {
  try {
    const { currentPassword, newPassword } = req.body;
    
    // Validation
    if (!currentPassword || !newPassword) {
      return res.status(400).json({ error: 'Current password and new password are required' });
    }
    
    if (newPassword.length < 6) {
      return res.status(400).json({ error: 'New password must be at least 6 characters long' });
    }
    
    // Get current user password
    const userStmt = db.prepare('SELECT password FROM users WHERE id = ?');
    const user = userStmt.get(req.userId);
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    // Verify current password
    const isCurrentPasswordValid = await bcrypt.compare(currentPassword, user.password);
    if (!isCurrentPasswordValid) {
      return res.status(400).json({ error: 'Current password is incorrect' });
    }
    
    // Hash new password
    const saltRounds = 12;
    const hashedNewPassword = await bcrypt.hash(newPassword, saltRounds);
    
    // Update password
    const updateStmt = db.prepare(`
      UPDATE users 
      SET password = ?, updated_at = ?
      WHERE id = ?
    `);
    
    const result = updateStmt.run(
      hashedNewPassword,
      new Date().toISOString(),
      req.userId
    );
    
    if (result.changes === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json({ message: 'Password changed successfully' });
  } catch (error) {
    console.error('Error changing password:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Get user's booking history
router.get('/bookings', auth, (req, res) => {
  try {
    const { page = 1, limit = 10, status } = req.query;
    const offset = (page - 1) * limit;
    
    let whereClause = 'WHERE b.user_id = ?';
    let params = [req.userId];
    
    if (status) {
      whereClause += ' AND b.status = ?';
      params.push(status);
    }
    
    const stmt = db.prepare(`
      SELECT 
        b.id,
        b.service_date,
        b.service_time,
        b.estimated_duration,
        b.total_price,
        b.status,
        b.special_instructions,
        b.created_at,
        st.name as service_name,
        st.description as service_description,
        c.first_name as cleaner_first_name,
        c.last_name as cleaner_last_name,
        c.phone as cleaner_phone
      FROM bookings b
      JOIN service_types st ON b.service_type_id = st.id
      LEFT JOIN cleaners c ON b.cleaner_id = c.id
      ${whereClause}
      ORDER BY b.service_date DESC, b.service_time DESC
      LIMIT ? OFFSET ?
    `);
    
    const bookings = stmt.all(...params, limit, offset);
    
    // Get total count for pagination
    const countStmt = db.prepare(`
      SELECT COUNT(*) as total FROM bookings b ${whereClause}
    `);
    const { total } = countStmt.get(...params);
    
    res.json({
      bookings,
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total,
        totalPages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    console.error('Error fetching user bookings:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

// Delete user account
router.delete('/account', auth, (req, res) => {
  try {
    const { password } = req.body;
    
    if (!password) {
      return res.status(400).json({ error: 'Password is required to delete account' });
    }
    
    // Get user password for verification
    const userStmt = db.prepare('SELECT password FROM users WHERE id = ?');
    const user = userStmt.get(req.userId);
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    // Verify password
    const isPasswordValid = bcrypt.compareSync(password, user.password);
    if (!isPasswordValid) {
      return res.status(400).json({ error: 'Incorrect password' });
    }
    
    // Check for active bookings
    const activeBookingsStmt = db.prepare(`
      SELECT COUNT(*) as count FROM bookings 
      WHERE user_id = ? AND status IN ('pending', 'confirmed') 
      AND service_date >= date('now')
    `);
    const { count } = activeBookingsStmt.get(req.userId);
    
    if (count > 0) {
      return res.status(400).json({ 
        error: 'Cannot delete account with active bookings. Please cancel or complete your bookings first.' 
      });
    }
    
    // Delete user (bookings will be kept for records)
    const deleteStmt = db.prepare('DELETE FROM users WHERE id = ?');
    const result = deleteStmt.run(req.userId);
    
    if (result.changes === 0) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json({ message: 'Account deleted successfully' });
  } catch (error) {
    console.error('Error deleting user account:', error);
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
