#!/usr/bin/env python3
"""
Database migration script to ensure all required columns exist for multilingual support
"""

import sqlite3
import os

def migrate_database():
    """Migrate the database to add missing columns for multilingual support"""
    db_path = 'aufraumenbee.db'
    
    if not os.path.exists(db_path):
        print("Database file doesn't exist yet. Will be created when needed.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Migrate employees table
        print("🔧 Migrating employees table...")
        cursor.execute("PRAGMA table_info(employees)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print("Current employees table columns:", column_names)
        
        # Required columns for the admin portal
        required_columns = {
            'status': 'TEXT DEFAULT "active"',
            'specialties': 'TEXT',
            'hourly_rate': 'REAL'
        }
        
        # Add missing columns
        for column, definition in required_columns.items():
            if column not in column_names:
                print(f"Adding {column} column to employees table...")
                cursor.execute(f'ALTER TABLE employees ADD COLUMN {column} {definition}')
                conn.commit()
                print(f"✅ {column} column added successfully")
        
        # Handle the specialties/skills column mapping
        if 'skills' in column_names and 'specialties' not in column_names:
            print("Migrating 'skills' column to 'specialties'...")
            cursor.execute('ALTER TABLE employees ADD COLUMN specialties TEXT')
            cursor.execute('UPDATE employees SET specialties = skills WHERE skills IS NOT NULL')
            conn.commit()
            print("✅ Skills data migrated to specialties column")
        elif 'specialties' in column_names and 'skills' in column_names:
            # Update specialties from skills if specialties is empty
            cursor.execute('''
                UPDATE employees 
                SET specialties = COALESCE(specialties, skills) 
                WHERE (specialties IS NULL OR specialties = '') AND skills IS NOT NULL
            ''')
            conn.commit()
            print("✅ Specialties updated from skills where needed")
        
        # Update status values
        cursor.execute('UPDATE employees SET status = "active" WHERE status IS NULL OR status = ""')
        conn.commit()
        
        # Migrate service_types table for multilingual support
        print("\n🔧 Migrating service_types table...")
        cursor.execute("PRAGMA table_info(service_types)")
        service_columns = cursor.fetchall()
        service_column_names = [col[1] for col in service_columns]
        
        print("Current service_types table columns:", service_column_names)
        
        # Add multilingual columns to service_types
        multilingual_service_columns = {
            'name_en': 'TEXT',
            'name_de': 'TEXT',
            'description_en': 'TEXT',
            'description_de': 'TEXT',
            'duration_hours': 'INTEGER DEFAULT 2'
        }
        
        for column, definition in multilingual_service_columns.items():
            if column not in service_column_names:
                print(f"Adding {column} column to service_types table...")
                cursor.execute(f'ALTER TABLE service_types ADD COLUMN {column} {definition}')
                conn.commit()
                print(f"✅ {column} column added successfully")
        
        # Migrate existing service data to multilingual columns
        if 'name' in service_column_names and 'name_en' in multilingual_service_columns:
            print("Migrating existing service data to multilingual columns...")
            
            # Map existing services to multilingual data
            service_translations = {
                'Regular Cleaning': {'en': 'Regular Cleaning', 'de': 'Grundreinigung'},
                'Deep Cleaning': {'en': 'Deep Cleaning', 'de': 'Tiefenreinigung'},
                'Move-in/Move-out Cleaning': {'en': 'Move-in/Move-out Cleaning', 'de': 'Ein-/Auszugsreinigung'},
                'Office Cleaning': {'en': 'Office Cleaning', 'de': 'Büroreinigung'},
                'Window Cleaning': {'en': 'Window Cleaning', 'de': 'Fensterreinigung'},
                'Carpet Cleaning': {'en': 'Carpet Cleaning', 'de': 'Teppichreinigung'}
            }
            
            description_translations = {
                'Standard house cleaning including dusting, vacuuming, mopping, and bathroom cleaning': {
                    'en': 'Standard house cleaning including dusting, vacuuming, mopping, and bathroom cleaning',
                    'de': 'Standard-Hausreinigung einschließlich Abstauben, Staubsaugen, Wischen und Badezimmerreinigung'
                },
                'Thorough cleaning including inside appliances, baseboards, and detailed cleaning': {
                    'en': 'Thorough cleaning including inside appliances, baseboards, and detailed cleaning',
                    'de': 'Gründliche Reinigung einschließlich Geräte, Sockelleisten und Detailreinigung'
                },
                'Complete cleaning for moving situations including inside cabinets and appliances': {
                    'en': 'Complete cleaning for moving situations including inside cabinets and appliances',
                    'de': 'Komplette Reinigung für Umzugssituationen einschließlich Schränke und Geräte'
                }
            }
            
            # Update English names and descriptions
            cursor.execute('''
                UPDATE service_types 
                SET name_en = name, description_en = description 
                WHERE name_en IS NULL OR name_en = ""
            ''')
            
            # Update German translations
            for orig_name, translations in service_translations.items():
                cursor.execute('''
                    UPDATE service_types 
                    SET name_de = ? 
                    WHERE name = ? AND (name_de IS NULL OR name_de = "")
                ''', (translations['de'], orig_name))
            
            for orig_desc, translations in description_translations.items():
                cursor.execute('''
                    UPDATE service_types 
                    SET description_de = ? 
                    WHERE description = ? AND (description_de IS NULL OR description_de = "")
                ''', (translations['de'], orig_desc))
            
            # Convert duration_minutes to duration_hours if needed
            if 'duration_minutes' in service_column_names:
                cursor.execute('''
                    UPDATE service_types 
                    SET duration_hours = CAST((duration_minutes + 30) / 60 AS INTEGER)
                    WHERE duration_hours IS NULL AND duration_minutes IS NOT NULL
                ''')
            
            conn.commit()
            print("✅ Service data migrated to multilingual columns")
        
        # Verify the migrations
        cursor.execute("SELECT COUNT(*) FROM employees")
        total_employees = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM employees WHERE status = 'active'")
        active_employees = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM service_types")
        total_services = cursor.fetchone()[0]
        
        print(f"\n📊 Final database statistics:")
        print(f"   Total employees: {total_employees}")
        print(f"   Active employees: {active_employees}")
        print(f"   Total services: {total_services}")
        
        # Check final table structures
        cursor.execute("PRAGMA table_info(employees)")
        final_emp_columns = cursor.fetchall()
        
        cursor.execute("PRAGMA table_info(service_types)")
        final_service_columns = cursor.fetchall()
        
        print(f"\n📋 Final employees table structure:")
        for col in final_emp_columns:
            print(f"   {col[1]} - {col[2]} (default: {col[4]})")
        
        print(f"\n📋 Final service_types table structure:")
        for col in final_service_columns:
            print(f"   {col[1]} - {col[2]} (default: {col[4]})")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 Starting comprehensive multilingual database migration...")
    migrate_database()
    print("✅ Migration completed")
