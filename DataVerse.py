import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import io
import json

# Page configuration
st.set_page_config(
    page_title="IT Infrastructure Alert Data Generator",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

class AlertDataGenerator:
    """Generate realistic IT infrastructure alert data for ML training"""
    
    def __init__(self):
        # Alert categories with realistic weights
        self.alert_categories = {
            'Performance': 25,
            'Availability': 20,
            'Exception': 20,
            'Database': 15,
            'Connectivity': 10,
            'Security': 5,
            'Network': 3,
            'Application': 2
        }
        
        # Priority distribution (realistic)
        self.priority_distribution = {
            'P1': 10,  # Critical
            'P2': 15,  # High
            'P3': 35,  # Medium
            'P4': 30,  # Low
            'P5': 10   # Informational
        }
        
        # System sources
        self.systems = [
            'SAP_ECC_PRD', 'SAP_S4HANA_PRD', 'HANA_DB_01', 'HANA_DB_02',
            'BTP_Tenant_01', 'BTP_Tenant_02', 'App_SRV_01', 'App_SRV_02',
            'Web_Gateway_01', 'Integration_Hub', 'API_Gateway', 'Auth_Service',
            'Payment_Gateway', 'Email_Service', 'File_Server', 'Backup_System'
        ]
        
        # Alert messages by category
        self.alert_messages = {
            'Performance': [
                'CPU utilization exceeded 90% threshold for 5 minutes',
                'Response time degradation detected - average 3.5s',
                'Memory usage critical - 95% utilized',
                'Disk I/O operations exceeding 1000 IOPS',
                'Thread pool exhaustion warning - 98% threads active',
                'Query execution time exceeded 10 seconds',
                'API response latency above 2000ms',
                'High garbage collection activity detected',
                'Connection pool near capacity - 90% used',
                'Slow transaction processing detected'
            ],
            'Availability': [
                'Service unavailable - HTTP 503 errors',
                'Health check failure detected',
                'Database connection lost',
                'Service restart required due to unresponsive state',
                'Scheduled maintenance window started',
                'Failover to secondary system initiated',
                'Service degradation - partial functionality available',
                'Load balancer health check failing',
                'Cluster node unreachable',
                'Service recovery in progress'
            ],
            'Exception': [
                'NullPointerException in payment processing module',
                'Unhandled exception in user authentication service',
                'OutOfMemoryError in report generation',
                'Database deadlock detected and resolved',
                'Connection timeout exception - external API',
                'JSON parsing error in data ingestion',
                'File not found exception in batch job',
                'Concurrent modification exception in cache layer',
                'Invalid state exception in workflow engine',
                'Stack overflow error in recursive function'
            ],
            'Database': [
                'Database connection pool exhausted',
                'Long-running query detected - 45 seconds',
                'Database backup failed - disk space',
                'Replication lag exceeds 10 minutes',
                'Table lock timeout occurred',
                'Index fragmentation above 30%',
                'Database checkpoint taking longer than expected',
                'Transaction log full - immediate action required',
                'Database mirroring suspended',
                'Slow query alert - full table scan detected'
            ],
            'Connectivity': [
                'Network latency spike detected - 500ms',
                'TCP connection reset by peer',
                'DNS resolution failure for external service',
                'VPN tunnel disconnected',
                'Firewall rule blocking legitimate traffic',
                'Network packet loss exceeds 5%',
                'SSL certificate validation failed',
                'Load balancer connection timeout',
                'Network interface card error detected',
                'Bandwidth utilization above 80%'
            ],
            'Security': [
                'Multiple failed login attempts detected',
                'Unauthorized access attempt blocked',
                'Security certificate expiring in 7 days',
                'Suspicious API access pattern detected',
                'Privilege escalation attempt logged',
                'Data encryption key rotation required',
                'Firewall rule violation detected',
                'Intrusion detection system alert triggered',
                'SQL injection attempt blocked',
                'Cross-site scripting attempt detected'
            ],
            'Network': [
                'Network switch port flapping detected',
                'Router CPU utilization high - 85%',
                'BGP peer session down',
                'Network packet corruption detected',
                'VLAN configuration mismatch',
                'Network device reboot detected',
                'Spanning tree topology change',
                'Network monitoring agent unreachable',
                'SNMP trap received - link down',
                'Network congestion detected on uplink'
            ],
            'Application': [
                'Application deployment failed - rollback initiated',
                'Configuration file syntax error detected',
                'Application license expiring in 30 days',
                'Session management error - memory leak suspected',
                'Application cache invalidation failed',
                'Microservice mesh communication failure',
                'Application startup sequence timeout',
                'Feature flag configuration error',
                'Application metrics collection failed',
                'Third-party integration service timeout'
            ]
        }
        
        # Team mapping by category
        self.team_mapping = {
            'Performance': ['Infrastructure Team', 'Platform Team'],
            'Availability': ['SRE Team', 'Operations Team'],
            'Exception': ['Development Team', 'Application Team'],
            'Database': ['Database Team', 'DBA Team'],
            'Connectivity': ['Network Team', 'Infrastructure Team'],
            'Security': ['Security Team', 'InfoSec Team'],
            'Network': ['Network Team', 'Infrastructure Team'],
            'Application': ['Application Team', 'Development Team']
        }
    
    def weighted_random_choice(self, choices_dict):
        """Select item based on weights"""
        items = list(choices_dict.keys())
        weights = list(choices_dict.values())
        return random.choices(items, weights=weights, k=1)[0]
    
    def generate_timestamp(self):
        """Generate random timestamp within last 30 days"""
        now = datetime.now()
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        seconds_ago = random.randint(0, 59)
        
        timestamp = now - timedelta(
            days=days_ago,
            hours=hours_ago,
            minutes=minutes_ago,
            seconds=seconds_ago
        )
        
        return timestamp
    
    def generate_alert(self, index):
        """Generate a single alert record"""
        # Select category and priority based on weights
        category = self.weighted_random_choice(self.alert_categories)
        priority = self.weighted_random_choice(self.priority_distribution)
        
        # Select random system and message
        system = random.choice(self.systems)
        message = random.choice(self.alert_messages[category])
        timestamp = self.generate_timestamp()
        
        # Status based on priority (P1/P2 more likely to be open)
        if priority in ['P1', 'P2']:
            status = random.choices(
                ['Open', 'Acknowledged', 'Resolved'],
                weights=[60, 25, 15],
                k=1
            )[0]
        else:
            status = random.choices(
                ['Open', 'Acknowledged', 'Resolved'],
                weights=[30, 30, 40],
                k=1
            )[0]
        
        # Resolution time (if resolved)
        resolution_time = random.randint(5, 245) if status == 'Resolved' else None
        
        # Assigned team
        teams = self.team_mapping[category]
        assigned_team = random.choice(teams)
        
        # Severity score based on priority
        if priority == 'P1':
            severity_score = round(random.uniform(90, 100), 2)
        elif priority == 'P2':
            severity_score = round(random.uniform(70, 89), 2)
        elif priority == 'P3':
            severity_score = round(random.uniform(40, 69), 2)
        elif priority == 'P4':
            severity_score = round(random.uniform(20, 39), 2)
        else:
            severity_score = round(random.uniform(0, 19), 2)
        
        # Impact level
        impact = 'High' if priority in ['P1', 'P2'] else 'Medium' if priority == 'P3' else 'Low'
        
        return {
            'alert_id': f"ALT-{str(index + 1).zfill(8)}",
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'category': category,
            'priority': priority,
            'system_source': system,
            'message': message,
            'status': status,
            'assigned_team': assigned_team,
            'resolution_time_minutes': resolution_time,
            'severity_score': severity_score,
            'impact': impact
        }
    
    def generate_dataset(self, num_records):
        """Generate complete dataset"""
        alerts = []
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(num_records):
            alerts.append(self.generate_alert(i))
            
            # Update progress every 100 records or at the end
            if (i + 1) % 100 == 0 or i == num_records - 1:
                progress = (i + 1) / num_records
                progress_bar.progress(progress)
                status_text.text(f"Generating alerts... {i + 1}/{num_records}")
        
        progress_bar.empty()
        status_text.empty()
        
        # Convert to DataFrame and sort by timestamp
        df = pd.DataFrame(alerts)
        df = df.sort_values('timestamp', ascending=False).reset_index(drop=True)
        
        return df


def main():
    # Header
    st.markdown('<h1 class="main-header">🚨 IT Infrastructure Alert Data Generator</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 2rem;">'
        'Generate realistic synthetic alert data for ML training and testing'
        '</p>',
        unsafe_allow_html=True
    )
    
    # Initialize generator
    if 'generator' not in st.session_state:
        st.session_state.generator = AlertDataGenerator()
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    num_records = st.sidebar.slider(
        "Number of Alert Records",
        min_value=10,
        max_value=100000,
        value=1000,
        step=10,
        help="Generate between 10 and 100,000 alert records"
    )
    
    st.sidebar.markdown("---")
    
    # Priority distribution info
    st.sidebar.markdown("### 📊 Priority Distribution")
    st.sidebar.markdown("""
    - **P1 (Critical)**: ~10%
    - **P2 (High)**: ~15%
    - **P3 (Medium)**: ~35%
    - **P4 (Low)**: ~30%
    - **P5 (Info)**: ~10%
    """)
    
    st.sidebar.markdown("---")
    
    # Category distribution info
    st.sidebar.markdown("### 🏷️ Category Distribution")
    st.sidebar.markdown("""
    - **Performance**: ~25%
    - **Availability**: ~20%
    - **Exception**: ~20%
    - **Database**: ~15%
    - **Connectivity**: ~10%
    - **Security**: ~5%
    - **Network**: ~3%
    - **Application**: ~2%
    """)
    
    # Generate button
    st.sidebar.markdown("---")
    generate_btn = st.sidebar.button(
        "🚀 Generate Data",
        type="primary",
        use_container_width=True
    )
    
    # Main content
    if generate_btn:
        with st.spinner("Generating synthetic data..."):
            start_time = datetime.now()
            
            # Generate data
            df = st.session_state.generator.generate_dataset(num_records)
            
            # Store in session state
            st.session_state.generated_data = df
            
            generation_time = (datetime.now() - start_time).total_seconds()
            
            st.success(f"✅ Generated {len(df):,} alert records in {generation_time:.2f} seconds!")
    
    # Display results if data exists
    if 'generated_data' in st.session_state:
        df = st.session_state.generated_data
        
        # Statistics row
        st.markdown("### 📈 Dataset Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                f'<div class="metric-card">'
                f'<h2 style="color: #ef4444; margin: 0;">{len(df):,}</h2>'
                f'<p style="color: #666; margin: 0.5rem 0 0 0;">Total Records</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f'<div class="metric-card">'
                f'<h2 style="color: #ef4444; margin: 0;">{len(df.columns)}</h2>'
                f'<p style="color: #666; margin: 0.5rem 0 0 0;">Columns</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with col3:
            memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
            st.markdown(
                f'<div class="metric-card">'
                f'<h2 style="color: #ef4444; margin: 0;">{memory_mb:.1f} MB</h2>'
                f'<p style="color: #666; margin: 0.5rem 0 0 0;">Memory Usage</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with col4:
            date_range = (pd.to_datetime(df['timestamp']).max() - pd.to_datetime(df['timestamp']).min()).days
            st.markdown(
                f'<div class="metric-card">'
                f'<h2 style="color: #ef4444; margin: 0;">{date_range}</h2>'
                f'<p style="color: #666; margin: 0.5rem 0 0 0;">Days Span</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        # Distribution Analysis
        st.markdown("### 📊 Distribution Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### By Category")
            category_dist = df['category'].value_counts().sort_values(ascending=False)
            for cat, count in category_dist.items():
                percentage = (count / len(df)) * 100
                st.markdown(f"**{cat}**: {count:,} ({percentage:.1f}%)")
        
        with col2:
            st.markdown("#### By Priority")
            priority_order = ['P1', 'P2', 'P3', 'P4', 'P5']
            for priority in priority_order:
                count = len(df[df['priority'] == priority])
                percentage = (count / len(df)) * 100
                st.markdown(f"**{priority}**: {count:,} ({percentage:.1f}%)")
        
        with col3:
            st.markdown("#### By Status")
            status_dist = df['status'].value_counts()
            for status, count in status_dist.items():
                percentage = (count / len(df)) * 100
                st.markdown(f"**{status}**: {count:,} ({percentage:.1f}%)")
        
        st.markdown("---")
        
        # Download section
        st.markdown("### 💾 Download Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV download
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name=f"alert_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # JSON download
            json_data = df.to_json(orient='records', indent=2, date_format='iso')
            
            st.download_button(
                label="📋 Download JSON",
                data=json_data,
                file_name=f"alert_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col3:
            # Excel download
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Alert Data', index=False)
            excel_data = excel_buffer.getvalue()
            
            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name=f"alert_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Data preview
        st.markdown("### 🔍 Data Preview (First 20 Records)")
        
        # Column information expander
        with st.expander("📋 Column Information"):
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.astype(str),
                'Non-Null': df.count().values,
                'Null Count': df.isnull().sum().values,
                'Unique': df.nunique().values
            })
            st.dataframe(col_info, use_container_width=True)
        
        # Display data
        st.dataframe(
            df.head(20),
            use_container_width=True,
            height=400
        )
        
        if len(df) > 20:
            st.info(f"📌 Showing first 20 rows out of {len(df):,} total records")
    
    else:
        # Show features when no data is generated
        st.markdown("### ✨ Key Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🏷️ 8 Alert Categories</h4>
                <p>Performance, Availability, Exception, Database, Connectivity, Security, Network, and Application alerts</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>🎯 Realistic Priority Mix</h4>
                <p>Balanced distribution across P1-P5 priorities matching real-world patterns</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>🖥️ Multiple Systems</h4>
                <p>16 different system sources including SAP, HANA, BTP, and custom services</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>⏰ Temporal Variety</h4>
                <p>Timestamps spread across 30 days with varied time patterns</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>💬 Rich Messages</h4>
                <p>80+ unique, realistic alert messages across all categories</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h4>🤖 ML-Ready</h4>
                <p>Includes severity scores, impact levels, resolution times, and team assignments</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #999; padding: 1rem;">'
        'Built with passion by <a href="https://www.linkedin.com/in/bikramsarkar/" target="_blank">Bikram</a> for Data Scientists and ML Engineers'
        
        '</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()