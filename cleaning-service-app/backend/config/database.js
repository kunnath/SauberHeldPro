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
  console.log('Initializing database...');
  
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
    }
  });

  // Cleaners table
  db.run(`
    CREATE TABLE IF NOT EXISTS cleaners (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      first_name TEXT NOT NULL,
      last_name TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      phone TEXT,
      specialties TEXT,
      rating DECIMAL(3,2) DEFAULT 5.0,
      experience_years INTEGER DEFAULT 0,
      is_available BOOLEAN DEFAULT TRUE,
      hourly_rate DECIMAL(8,2) DEFAULT 25.00,
      bio TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `, (err) => {
    if (err) {
      console.error('Error creating cleaners table:', err);
    }
  });

  // Bookings table
  db.run(`
    CREATE TABLE IF NOT EXISTS bookings (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL,
      service_type_id INTEGER NOT NULL,
      cleaner_id INTEGER,
      service_date DATE NOT NULL,
      service_time TIME NOT NULL,
      estimated_duration INTEGER NOT NULL,
      total_price DECIMAL(10,2) NOT NULL,
      status TEXT DEFAULT 'pending',
      special_instructions TEXT,
      address TEXT NOT NULL,
      cancellation_reason TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users (id),
      FOREIGN KEY (service_type_id) REFERENCES service_types (id),
      FOREIGN KEY (cleaner_id) REFERENCES cleaners (id)
    )
  `, (err) => {
    if (err) {
      console.error('Error creating bookings table:', err);
    }
  });

  // Contact messages table
  db.run(`
    CREATE TABLE IF NOT EXISTS contact_messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT NOT NULL,
      phone TEXT,
      subject TEXT,
      message TEXT NOT NULL,
      service_interest TEXT,
      status TEXT DEFAULT 'new',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `, (err) => {
    if (err) {
      console.error('Error creating contact_messages table:', err);
    }
  });

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
  `, (err) => {
    if (err) {
      console.error('Error creating reviews table:', err);
    }
  });

  // Insert default data after a delay to ensure tables are created
  setTimeout(() => {
    insertDefaultData();
  }, 1000);

  console.log('✅ Database initialization started');
};

const insertDefaultData = () => {
  // Insert default service types
  db.get("SELECT COUNT(*) as count FROM service_types", (err, row) => {
    if (err) {
      console.error('Error checking service types:', err);
      return;
    }
    
    if (row.count === 0) {
      console.log('Inserting default service types...');
      
      const services = [
        {
          name: 'Basic Cleaning',
          description: 'Essential cleaning service for maintaining a tidy home',
          base_price: 28.90,
          duration_minutes: 120,
          category: 'home',
          features: JSON.stringify([
            'Dusting all surfaces',
            'Vacuuming and mopping floors',
            'Bathroom cleaning',
            'Kitchen cleaning',
            'Trash removal'
          ])
        },
        {
          name: 'Deep Cleaning',
          description: 'Comprehensive cleaning service for a thorough clean',
          base_price: 45.90,
          duration_minutes: 180,
          category: 'home',
          features: JSON.stringify([
            'Everything in Basic Cleaning',
            'Inside appliances cleaning',
            'Baseboards and window sills',
            'Light fixtures cleaning',
            'Inside cabinets and drawers'
          ])
        },
        {
          name: 'Move-in/Move-out Cleaning',
          description: 'Complete cleaning for new or vacant properties',
          base_price: 65.90,
          duration_minutes: 240,
          category: 'moving',
          features: JSON.stringify([
            'Everything in Deep Cleaning',
            'Inside refrigerator and oven',
            'All windows (inside)',
            'Closets and storage areas',
            'Garage/basement cleaning'
          ])
        },
        {
          name: 'Office Cleaning',
          description: 'Professional cleaning for workplace environments',
          base_price: 35.90,
          duration_minutes: 90,
          category: 'office',
          features: JSON.stringify([
            'Desk and workspace cleaning',
            'Restroom sanitization',
            'Kitchen/break room cleaning',
            'Trash and recycling',
            'Floor care'
          ])
        },
        {
          name: 'Post-Construction Cleanup',
          description: 'Specialized cleaning after renovation or construction',
          base_price: 85.90,
          duration_minutes: 300,
          category: 'construction',
          features: JSON.stringify([
            'Dust and debris removal',
            'Window cleaning',
            'Paint and material cleanup',
            'Floor restoration',
            'Final polish and inspection'
          ])
        }
      ];

      const stmt = db.prepare(`
        INSERT INTO service_types (name, description, base_price, duration_minutes, category, features)
        VALUES (?, ?, ?, ?, ?, ?)
      `);

      services.forEach((service) => {
        stmt.run(
          service.name,
          service.description,
          service.base_price,
          service.duration_minutes,
          service.category,
          service.features
        );
      });

      stmt.finalize();
      console.log(`✅ Inserted ${services.length} default service types`);
    }
  });

  // Insert default cleaners
  db.get("SELECT COUNT(*) as count FROM cleaners", (err, row) => {
    if (err) {
      console.error('Error checking cleaners:', err);
      return;
    }
    
    if (row.count === 0) {
      console.log('Inserting default cleaners...');
      
      const cleaners = [
        {
          first_name: 'Maria',
          last_name: 'Garcia',
          email: 'maria.garcia@cleanpro.com',
          phone: '+49 30 1234 5678',
          specialties: 'Deep Cleaning, Move-in/Move-out',
          rating: 4.9,
          experience_years: 5,
          hourly_rate: 28.00,
          bio: 'Experienced cleaner specializing in deep cleaning services. Attention to detail is my priority.'
        },
        {
          first_name: 'Anna',
          last_name: 'Schmidt',
          email: 'anna.schmidt@cleanpro.com',
          phone: '+49 30 2345 6789',
          specialties: 'Basic Cleaning, Office Cleaning',
          rating: 4.8,
          experience_years: 3,
          hourly_rate: 25.00,
          bio: 'Reliable and efficient cleaner with expertise in residential and office cleaning.'
        },
        {
          first_name: 'Sophie',
          last_name: 'Mueller',
          email: 'sophie.mueller@cleanpro.com',
          phone: '+49 30 3456 7890',
          specialties: 'Post-Construction, Deep Cleaning',
          rating: 4.9,
          experience_years: 7,
          hourly_rate: 32.00,
          bio: 'Specialist in post-construction cleanup and challenging cleaning projects.'
        },
        {
          first_name: 'Elena',
          last_name: 'Popov',
          email: 'elena.popov@cleanpro.com',
          phone: '+49 30 4567 8901',
          specialties: 'Basic Cleaning, Move-in/Move-out',
          rating: 4.7,
          experience_years: 4,
          hourly_rate: 26.00,
          bio: 'Friendly and thorough cleaner with excellent customer service skills.'
        }
      ];

      const stmt = db.prepare(`
        INSERT INTO cleaners (first_name, last_name, email, phone, specialties, rating, experience_years, hourly_rate, bio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      `);

      cleaners.forEach((cleaner) => {
        stmt.run(
          cleaner.first_name,
          cleaner.last_name,
          cleaner.email,
          cleaner.phone,
          cleaner.specialties,
          cleaner.rating,
          cleaner.experience_years,
          cleaner.hourly_rate,
          cleaner.bio
        );
      });

      stmt.finalize();
      console.log(`✅ Inserted ${cleaners.length} default cleaners`);
    }
  });
};

module.exports = db;
module.exports.initializeDatabase = initializeDatabase;
