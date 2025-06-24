#!/usr/bin/env python3
"""
Real-Time Logging System for Aufraumenbee
Provides real-time log monitoring for frontend and backend activities
"""

import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import threading
import queue
import json
from typing import Dict, Any, Optional
import sqlite3
import inspect
import traceback

class RealtimeLogger:
    """Enhanced logging system with real-time monitoring capabilities"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create separate loggers for different components
        self.loggers = {}
        self.log_queue = queue.Queue()
        self.setup_loggers()
        
        # Start background thread for real-time processing
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_logs, daemon=True)
        self.monitor_thread.start()
    
    def setup_loggers(self):
        """Setup separate loggers for different components"""
        components = [
            'frontend', 'backend', 'database', 'auth', 
            'customer_portal', 'admin_portal', 'api', 'errors'
        ]
        
        for component in components:
            logger = logging.getLogger(f'aufraumenbee.{component}')
            logger.setLevel(logging.DEBUG)
            
            # Clear existing handlers
            logger.handlers.clear()
            
            # Create file handler
            log_file = self.log_dir / f"{component}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            
            # Create console handler for real-time output
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
            self.loggers[component] = logger
    
    def get_logger(self, component: str) -> logging.Logger:
        """Get logger for specific component"""
        return self.loggers.get(component, self.loggers['backend'])
    
    def log_user_action(self, component: str, action: str, user_info: Dict[str, Any], 
                       details: Optional[Dict[str, Any]] = None):
        """Log user actions with context"""
        logger = self.get_logger(component)
        
        caller_frame = inspect.currentframe().f_back
        caller_info = f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno}"
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'component': component,
            'action': action,
            'user_info': user_info,
            'details': details or {},
            'caller': caller_info
        }
        
        logger.info(f"USER_ACTION: {json.dumps(log_entry, indent=2)}")
        
        # Store in database for analytics
        self._store_to_database(log_entry)
    
    def log_error(self, component: str, error: Exception, context: Dict[str, Any] = None):
        """Log errors with full context and traceback"""
        logger = self.get_logger('errors')
        
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'component': component,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {}
        }
        
        logger.error(f"ERROR: {json.dumps(error_info, indent=2)}")
        self._store_to_database(error_info, table='error_logs')
    
    def log_database_operation(self, operation: str, table: str, details: Dict[str, Any]):
        """Log database operations"""
        logger = self.get_logger('database')
        
        db_log = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'table': table,
            'details': details
        }
        
        logger.info(f"DB_OPERATION: {json.dumps(db_log, indent=2)}")
        self._store_to_database(db_log, table='db_operation_logs')
    
    def log_api_request(self, endpoint: str, method: str, user_info: Dict[str, Any], 
                       request_data: Dict[str, Any], response_status: int):
        """Log API requests and responses"""
        logger = self.get_logger('api')
        
        api_log = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'method': method,
            'user_info': user_info,
            'request_data': request_data,
            'response_status': response_status
        }
        
        logger.info(f"API_REQUEST: {json.dumps(api_log, indent=2)}")
        self._store_to_database(api_log, table='api_logs')
    
    def _store_to_database(self, log_data: Dict[str, Any], table: str = 'activity_logs'):
        """Store log data to database for analytics"""
        try:
            conn = sqlite3.connect('aufraumenbee.db')
            cursor = conn.cursor()
            
            # Create table if not exists
            if table == 'activity_logs':
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS activity_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        component TEXT,
                        action TEXT,
                        user_info TEXT,
                        details TEXT,
                        caller TEXT
                    )
                ''')
                
                cursor.execute('''
                    INSERT INTO activity_logs (component, action, user_info, details, caller)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    log_data.get('component'),
                    log_data.get('action'),
                    json.dumps(log_data.get('user_info', {})),
                    json.dumps(log_data.get('details', {})),
                    log_data.get('caller')
                ))
            
            elif table == 'error_logs':
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS error_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        component TEXT,
                        error_type TEXT,
                        error_message TEXT,
                        traceback TEXT,
                        context TEXT
                    )
                ''')
                
                cursor.execute('''
                    INSERT INTO error_logs (component, error_type, error_message, traceback, context)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    log_data.get('component'),
                    log_data.get('error_type'),
                    log_data.get('error_message'),
                    log_data.get('traceback'),
                    json.dumps(log_data.get('context', {}))
                ))
            
            elif table == 'db_operation_logs':
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS db_operation_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        operation TEXT,
                        table_name TEXT,
                        details TEXT
                    )
                ''')
                
                cursor.execute('''
                    INSERT INTO db_operation_logs (operation, table_name, details)
                    VALUES (?, ?, ?)
                ''', (
                    log_data.get('operation'),
                    log_data.get('table'),
                    json.dumps(log_data.get('details', {}))
                ))
            
            elif table == 'api_logs':
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS api_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        endpoint TEXT,
                        method TEXT,
                        user_info TEXT,
                        request_data TEXT,
                        response_status INTEGER
                    )
                ''')
                
                cursor.execute('''
                    INSERT INTO api_logs (endpoint, method, user_info, request_data, response_status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    log_data.get('endpoint'),
                    log_data.get('method'),
                    json.dumps(log_data.get('user_info', {})),
                    json.dumps(log_data.get('request_data', {})),
                    log_data.get('response_status')
                ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            # Fallback to console logging if database fails
            print(f"Failed to store log to database: {e}")
    
    def _monitor_logs(self):
        """Background thread to monitor logs in real-time"""
        while self.running:
            try:
                time.sleep(1)  # Check every second
                # This could be expanded to do real-time log processing
            except Exception as e:
                print(f"Log monitoring error: {e}")
    
    def stop(self):
        """Stop the logging system"""
        self.running = False

# Global logger instance
_global_logger = None

def get_realtime_logger() -> RealtimeLogger:
    """Get the global realtime logger instance"""
    global _global_logger
    if _global_logger is None:
        _global_logger = RealtimeLogger()
    return _global_logger

# Convenience functions
def log_user_action(component: str, action: str, user_info: Dict[str, Any], details: Dict[str, Any] = None):
    """Log user action"""
    get_realtime_logger().log_user_action(component, action, user_info, details)

def log_error(component: str, error: Exception, context: Dict[str, Any] = None):
    """Log error"""
    get_realtime_logger().log_error(component, error, context)

def log_database_operation(operation: str, table: str, details: Dict[str, Any]):
    """Log database operation"""
    get_realtime_logger().log_database_operation(operation, table, details)

def log_api_request(endpoint: str, method: str, user_info: Dict[str, Any], 
                   request_data: Dict[str, Any], response_status: int):
    """Log API request"""
    get_realtime_logger().log_api_request(endpoint, method, user_info, request_data, response_status)

if __name__ == "__main__":
    # Test the logging system
    logger = get_realtime_logger()
    
    # Test user action logging
    log_user_action(
        'customer_portal',
        'user_registration',
        {'username': 'test_user', 'email': 'test@example.com'},
        {'registration_method': 'email', 'source': 'direct'}
    )
    
    # Test error logging
    try:
        raise ValueError("Test error for logging")
    except Exception as e:
        log_error('customer_portal', e, {'test_context': 'testing error logging'})
    
    # Test database operation logging
    log_database_operation(
        'INSERT',
        'users',
        {'action': 'create_user', 'user_id': '12345'}
    )
    
    print("✅ Real-time logging system test completed!")
    print("📁 Check the logs/ directory for log files")
    print("🗄️ Check the aufraumenbee.db for stored log data")
