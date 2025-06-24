#!/usr/bin/env python3
"""
Real-Time Log Viewer Dashboard for Aufraumenbee
Monitor frontend and backend logs in real-time
"""

import streamlit as st
import pandas as pd
import sqlite3
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Try to import auto-refresh, fallback if not available
try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH_AVAILABLE = True
except ImportError:
    AUTO_REFRESH_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="🔍 Aufraumenbee - Real-Time Logs",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better log display
st.markdown("""
<style>
.log-container {
    background-color: #0E1117;
    color: #FAFAFA;
    padding: 10px;
    border-radius: 5px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid #262730;
}

.log-entry {
    margin-bottom: 5px;
    padding: 5px;
    border-left: 3px solid #FF6B6B;
}

.log-info { border-left-color: #4ECDC4; }
.log-warning { border-left-color: #FFE66D; }
.log-error { border-left-color: #FF6B6B; }
.log-debug { border-left-color: #95E1D3; }

.metric-card {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
}

.status-indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 10px;
}

.status-green { background-color: #4CAF50; }
.status-red { background-color: #F44336; }
.status-yellow { background-color: #FF9800; }
</style>
""", unsafe_allow_html=True)

def get_log_files():
    """Get list of available log files"""
    log_dir = Path("logs")
    if not log_dir.exists():
        return []
    return [f.name for f in log_dir.glob("*.log")]

def read_log_file(filename, max_lines=100):
    """Read last N lines from log file"""
    log_path = Path("logs") / filename
    if not log_path.exists():
        return []
    
    try:
        with open(log_path, 'r') as f:
            lines = f.readlines()
            return lines[-max_lines:] if len(lines) > max_lines else lines
    except Exception as e:
        return [f"Error reading log file: {e}"]

def get_database_logs(table_name, limit=50):
    """Get logs from database"""
    try:
        conn = sqlite3.connect('aufraumenbee.db')
        
        if table_name == 'activity_logs':
            query = """
                SELECT timestamp, component, action, user_info, details, caller
                FROM activity_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            """
        elif table_name == 'error_logs':
            query = """
                SELECT timestamp, component, error_type, error_message, traceback, context
                FROM error_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            """
        elif table_name == 'db_operation_logs':
            query = """
                SELECT timestamp, operation, table_name, details
                FROM db_operation_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            """
        elif table_name == 'api_logs':
            query = """
                SELECT timestamp, endpoint, method, user_info, request_data, response_status
                FROM api_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            """
        else:
            return pd.DataFrame()
        
        df = pd.read_sql_query(query, conn, params=[limit])
        conn.close()
        return df
    
    except Exception as e:
        st.error(f"Error reading database logs: {e}")
        return pd.DataFrame()

def display_log_metrics():
    """Display log metrics dashboard"""
    try:
        conn = sqlite3.connect('aufraumenbee.db')
        
        # Get activity counts
        activity_count = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM activity_logs WHERE timestamp > datetime('now', '-1 hour')",
            conn
        ).iloc[0]['count']
        
        # Get error counts
        error_count = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM error_logs WHERE timestamp > datetime('now', '-1 hour')",
            conn
        ).iloc[0]['count']
        
        # Get database operation counts
        db_ops_count = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM db_operation_logs WHERE timestamp > datetime('now', '-1 hour')",
            conn
        ).iloc[0]['count']
        
        # Get API request counts
        api_count = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM api_logs WHERE timestamp > datetime('now', '-1 hour')",
            conn
        ).iloc[0]['count']
        
        conn.close()
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔄 Activities</h3>
                <h2>{activity_count}</h2>
                <p>Last Hour</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            status_color = "status-red" if error_count > 0 else "status-green"
            st.markdown(f"""
            <div class="metric-card">
                <h3>❌ Errors</h3>
                <h2><span class="status-indicator {status_color}"></span>{error_count}</h2>
                <p>Last Hour</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🗄️ DB Operations</h3>
                <h2>{db_ops_count}</h2>
                <p>Last Hour</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🌐 API Requests</h3>
                <h2>{api_count}</h2>
                <p>Last Hour</p>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error displaying metrics: {e}")

def display_activity_timeline():
    """Display activity timeline chart"""
    try:
        conn = sqlite3.connect('aufraumenbee.db')
        
        # Get activity timeline data
        query = """
            SELECT 
                datetime(timestamp) as time,
                component,
                COUNT(*) as activity_count
            FROM activity_logs 
            WHERE timestamp > datetime('now', '-24 hours')
            GROUP BY datetime(timestamp, 'start of hour'), component
            ORDER BY time DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            fig = px.line(
                df, 
                x='time', 
                y='activity_count', 
                color='component',
                title="📈 Activity Timeline (Last 24 Hours)",
                labels={'time': 'Time', 'activity_count': 'Activity Count'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No activity data available for the last 24 hours")
    
    except Exception as e:
        st.error(f"Error displaying activity timeline: {e}")

def format_log_entry(entry, log_type="file"):
    """Format log entry for display"""
    if log_type == "file":
        # Parse log level from file log entry
        if "| ERROR |" in entry:
            return f'<div class="log-entry log-error">{entry.strip()}</div>'
        elif "| WARNING |" in entry:
            return f'<div class="log-entry log-warning">{entry.strip()}</div>'
        elif "| INFO |" in entry:
            return f'<div class="log-entry log-info">{entry.strip()}</div>'
        elif "| DEBUG |" in entry:
            return f'<div class="log-entry log-debug">{entry.strip()}</div>'
        else:
            return f'<div class="log-entry">{entry.strip()}</div>'
    else:
        # Database log entry formatting
        return f'<div class="log-entry log-info">{entry}</div>'

def main():
    """Main application"""
    st.title("🔍 Aufraumenbee - Real-Time Log Monitor")
    st.markdown("Monitor all frontend and backend activities in real-time")
    
    # Auto-refresh every 5 seconds
    if AUTO_REFRESH_AVAILABLE:
        st_autorefresh(interval=5000, key="log_refresh")
    else:
        st.info("Auto-refresh not available. Install streamlit-autorefresh for automatic updates.")
    
    # Display metrics
    st.markdown("### 📊 System Metrics")
    display_log_metrics()
    
    # Activity timeline
    st.markdown("### 📈 Activity Timeline")
    display_activity_timeline()
    
    # Main log viewer
    st.markdown("### 📋 Real-Time Logs")
    
    # Sidebar for log configuration
    with st.sidebar:
        st.header("🔧 Log Configuration")
        
        # Log source selection
        log_source = st.radio(
            "Select Log Source:",
            ["File Logs", "Database Logs"],
            key="log_source"
        )
        
        if log_source == "File Logs":
            # File log options
            log_files = get_log_files()
            if log_files:
                selected_file = st.selectbox("Select Log File:", log_files)
                max_lines = st.slider("Max Lines to Display:", 10, 500, 100)
            else:
                st.warning("No log files found. Start the application to generate logs.")
                selected_file = None
        else:
            # Database log options
            log_tables = ["activity_logs", "error_logs", "db_operation_logs", "api_logs"]
            selected_table = st.selectbox("Select Log Table:", log_tables)
            max_records = st.slider("Max Records to Display:", 10, 200, 50)
        
        # Filter options
        st.markdown("---")
        st.header("🔍 Filters")
        
        show_errors_only = st.checkbox("Show Errors Only")
        show_last_hour = st.checkbox("Last Hour Only")
        
        # Auto-refresh control
        st.markdown("---")
        st.header("🔄 Auto-Refresh")
        st.info("Page auto-refreshes every 5 seconds")
        
        if st.button("🔄 Manual Refresh"):
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if log_source == "File Logs" and selected_file:
            st.markdown(f"#### 📄 {selected_file}")
            
            # Read and display log file
            log_entries = read_log_file(selected_file, max_lines)
            
            if log_entries:
                # Apply filters
                if show_errors_only:
                    log_entries = [entry for entry in log_entries if "ERROR" in entry.upper()]
                
                if show_last_hour:
                    now = datetime.now()
                    hour_ago = now - timedelta(hours=1)
                    # Filter logic for last hour (simplified)
                    log_entries = log_entries[-50:]  # Show last 50 entries as approximation
                
                # Display logs
                log_html = '<div class="log-container">'
                for entry in reversed(log_entries[-50:]):  # Show last 50 entries
                    log_html += format_log_entry(entry)
                log_html += '</div>'
                
                st.markdown(log_html, unsafe_allow_html=True)
            else:
                st.info("No log entries found")
        
        elif log_source == "Database Logs":
            st.markdown(f"#### 🗄️ {selected_table.replace('_', ' ').title()}")
            
            # Read and display database logs
            df = get_database_logs(selected_table, max_records)
            
            if not df.empty:
                # Apply filters
                if show_last_hour:
                    hour_ago = datetime.now() - timedelta(hours=1)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df = df[df['timestamp'] > hour_ago]
                
                if show_errors_only and 'error_type' in df.columns:
                    df = df[df['error_type'].notna()]
                
                # Display as formatted table
                st.dataframe(
                    df,
                    use_container_width=True,
                    height=400
                )
                
                # Show JSON details for selected row
                if len(df) > 0:
                    selected_row = st.selectbox(
                        "Select row to view details:",
                        range(len(df)),
                        format_func=lambda x: f"Row {x+1}: {df.iloc[x]['timestamp']}"
                    )
                    
                    st.markdown("#### 📋 Row Details")
                    row_data = df.iloc[selected_row].to_dict()
                    
                    # Parse JSON fields
                    for key, value in row_data.items():
                        if isinstance(value, str) and (value.startswith('{') or value.startswith('[')):
                            try:
                                parsed = json.loads(value)
                                st.json(parsed)
                            except:
                                st.text(value)
                        else:
                            st.text(f"{key}: {value}")
            else:
                st.info("No database log entries found")
    
    with col2:
        st.markdown("#### 🎛️ Live Status")
        
        # System status indicators
        log_files = get_log_files()
        
        st.markdown("**Log Files Status:**")
        for log_file in log_files:
            log_path = Path("logs") / log_file
            size = log_path.stat().st_size if log_path.exists() else 0
            size_mb = size / (1024 * 1024)
            
            if size_mb > 0:
                status_color = "🟢"
            else:
                status_color = "🔴"
            
            st.markdown(f"{status_color} {log_file}: {size_mb:.2f} MB")
        
        # Database status
        st.markdown("---")
        st.markdown("**Database Status:**")
        try:
            conn = sqlite3.connect('aufraumenbee.db')
            cursor = conn.cursor()
            
            tables = ['activity_logs', 'error_logs', 'db_operation_logs', 'api_logs']
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    st.markdown(f"🟢 {table}: {count} records")
                except:
                    st.markdown(f"🔴 {table}: Not available")
            
            conn.close()
        except Exception as e:
            st.error(f"Database connection error: {e}")
        
        # Quick actions
        st.markdown("---")
        st.markdown("#### ⚡ Quick Actions")
        
        if st.button("🗑️ Clear Log Files"):
            try:
                for log_file in get_log_files():
                    log_path = Path("logs") / log_file
                    log_path.unlink()
                st.success("Log files cleared!")
                st.rerun()
            except Exception as e:
                st.error(f"Error clearing logs: {e}")
        
        if st.button("📊 Export Logs"):
            try:
                # Export database logs to CSV
                conn = sqlite3.connect('aufraumenbee.db')
                df = pd.read_sql_query("SELECT * FROM activity_logs ORDER BY timestamp DESC LIMIT 1000", conn)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Activity Logs CSV",
                    data=csv,
                    file_name=f"activity_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                conn.close()
            except Exception as e:
                st.error(f"Error exporting logs: {e}")

if __name__ == "__main__":
    main()
