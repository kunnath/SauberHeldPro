const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.join(__dirname, '../data/cleaning_service.db');

// Create data directory if it doesn't exist
const fs = require('fs');
const dataDir = path.dirname(dbPath);
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database:', err.message);
  } else {
    console.log('📦 Connected to SQLite database');
  }
});

const initializeDatabase = () => {
  return new Promise((resolve, reject) => {
    // Enable foreign keys
    db.run('PRAGMA foreign_keys = ON');

    // Users table
    db.run(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        role TEXT DEFAULT 'customer',
        email_verified BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `, (err) => {
      if (err) {
        console.error('Error creating users table:', err);
        reject(err);
        return;
      }
    });

    // Service types table
    db.run(`
      CREATE TABLE IF NOT EXISTS service_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        base_price DECIMAL(10,2) NOT NULL,
        duration_minutes INTEGER NOT NULL,
        category TEXT DEFAULT 'home',
        features TEXT,
        is_active BOOLEAN DEFAULT TRUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `, (err) => {
      if (err) {
        console.error('Error creating service_types table:', err);
        reject(err);
        return;
      }
    });
      category TEXT DEFAULT 'home',
      features TEXT,
      active BOOLEAN DEFAULT TRUE,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Cleaners table
  db.run(`
    CREATE TABLE IF NOT EXISTS cleaners (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      phone TEXT,
      languages TEXT DEFAULT 'German',
      experience_years INTEGER DEFAULT 0,
      hourly_rate DECIMAL(10,2),
      rating DECIMAL(3,2) DEFAULT 0.0,
      total_jobs INTEGER DEFAULT 0,
      background_checked BOOLEAN DEFAULT FALSE,
      available BOOLEAN DEFAULT TRUE,
      postal_codes TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Bookings table
  db.run(`
    CREATE TABLE IF NOT EXISTS bookings (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      service_type_id INTEGER NOT NULL,
      cleaner_id INTEGER,
      postal_code TEXT NOT NULL,
      address TEXT NOT NULL,
      booking_date DATE NOT NULL,
      booking_time TEXT NOT NULL,
      duration INTEGER NOT NULL,
      total_price DECIMAL(10,2) NOT NULL,
      deposit_amount DECIMAL(10,2),
      special_instructions TEXT,
      status TEXT DEFAULT 'pending',
      payment_status TEXT DEFAULT 'pending',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users (id),
      FOREIGN KEY (service_type_id) REFERENCES service_types (id),
      FOREIGN KEY (cleaner_id) REFERENCES cleaners (id)
    )
  `);

  // Contact messages table
  db.run(`
    CREATE TABLE IF NOT EXISTS contact_messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      email TEXT NOT NULL,
      phone TEXT,
      subject TEXT NOT NULL,
      message TEXT NOT NULL,
      status TEXT DEFAULT 'new',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Reviews table
  db.run(`
    CREATE TABLE IF NOT EXISTS reviews (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      booking_id INTEGER NOT NULL,
      user_id INTEGER NOT NULL,
      cleaner_id INTEGER NOT NULL,
      rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
      comment TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (booking_id) REFERENCES bookings (id),
      FOREIGN KEY (user_id) REFERENCES users (id),
      FOREIGN KEY (cleaner_id) REFERENCES cleaners (id)
    )
  `);

  // Insert default service types
  db.get("SELECT COUNT(*) as count FROM service_types", (err, row) => {
    if (err) {
      console.error('Error checking service types:', err);
      return;
    }
    
    if (row.count === 0) {
      const services = [
        {
          name: 'Basic Cleaning',
          description: 'Reliable home cleaning service. Good choice if you want to maintain a clean home.',
          base_price: 28.90,
          duration_minutes: 120,
          category: 'home',
          features: JSON.stringify([
            'Regular maintenance cleaning',
            'Dusting and vacuuming',
            'Kitchen and bathroom cleaning',
            'Trash removal',
            'Making beds'
          ])
        },
        {
          name: 'Deep Cleaning',
          description: 'Extensive cleaning for move-in/move-out or after renovation.',
          base_price: 45.00,
          duration_minutes: 240,
          category: 'home',
          features: JSON.stringify([
            'Everything in Basic Cleaning',
            'Deep scrubbing of bathrooms',
            'Inside oven and refrigerator cleaning',
            'Baseboards and window sills',
            'Interior window cleaning'
          ])
        },
        {
          name: 'Office Cleaning',
          description: 'Customized cleaning solutions for your workplace.',
          base_price: 35.00,
          duration_minutes: 180,
          category: 'office',
          features: JSON.stringify([
            'Desk and workspace sanitizing',
            'Conference room cleaning',
            'Kitchen/break room maintenance',
            'Restroom deep cleaning',
            'Common area maintenance'
          ])
        }
      ];

      const stmt = db.prepare(`
        INSERT INTO service_types (name, description, base_price, duration_minutes, category, features)
        VALUES (?, ?, ?, ?, ?, ?)
      `);

      services.forEach(service => {
        stmt.run([
          service.name,
          service.description,
          service.base_price,
          service.duration_minutes,
          service.category,
          service.features
        ]);
      });

      stmt.finalize();
      console.log('✅ Default service types inserted');
    }
  });

  // Insert sample cleaners
  db.get("SELECT COUNT(*) as count FROM cleaners", (err, row) => {
    if (err) {
      console.error('Error checking cleaners:', err);
      return;
    }
    
    if (row.count === 0) {
      const cleaners = [
        {
          first_name: 'Maria',
          last_name: 'Schmidt',
          email: 'maria.schmidt@cleanpro.de',
          phone: '+49 30 123 456 789',
          languages: 'German,English',
          experience_years: 5,
          hourly_rate: 32.00,
          rating: 4.8,
          total_jobs: 127,
          background_checked: true,
          postal_codes: '10115,10117,10119,10178'
        },
        {
          first_name: 'Anna',
          last_name: 'Mueller',
          email: 'anna.mueller@cleanpro.de',
          phone: '+49 30 234 567 890',
          languages: 'German,English,Spanish',
          experience_years: 3,
          hourly_rate: 30.00,
          rating: 4.9,
          total_jobs: 89,
          background_checked: true,
          postal_codes: '10115,10117,10119,10178,10179'
        },
        {
          first_name: 'Thomas',
          last_name: 'Weber',
          email: 'thomas.weber@cleanpro.de',
          phone: '+49 30 345 678 901',
          languages: 'German,English',
          experience_years: 7,
          hourly_rate: 35.00,
          rating: 4.7,
          total_jobs: 203,
          background_checked: true,
          postal_codes: '10115,10117,10119,10178,10179,10243'
        }
      ];

      const stmt = db.prepare(`
        INSERT INTO cleaners (first_name, last_name, email, phone, languages, experience_years, hourly_rate, rating, total_jobs, background_checked, postal_codes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `);

      cleaners.forEach(cleaner => {
        stmt.run([
          cleaner.first_name,
          cleaner.last_name,
          cleaner.email,
          cleaner.phone,
          cleaner.languages,
          cleaner.experience_years,
          cleaner.hourly_rate,
          cleaner.rating,
          cleaner.total_jobs,
          cleaner.background_checked,
          cleaner.postal_codes
        ]);
      });

      stmt.finalize();
      console.log('✅ Sample cleaners inserted');
    }
  });

  console.log('✅ Database initialized successfully');
};

module.exports = initializeDatabase;
module.exports.db = db;
