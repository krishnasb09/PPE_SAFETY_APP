import streamlit as st
import pandas as pd
import altair as alt
from database import get_connection

st.set_page_config(page_title="Admin Dashboard", layout="wide", page_icon="🛡️")

st.markdown("""
<style>
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #1e1e1e;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
    }
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #00d4ff;
    }
    /* Sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    /* Sidebar styling - broad approach for compatibility */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
    }

    /* Target all text elements in sidebar */
    section[data-testid="stSidebar"] * {
        color: #facc15 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }

    /* Specifically target links */
    section[data-testid="stSidebar"] a {
        color: #facc15 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        text-decoration: none !important;
        padding: 8px 12px !important;
        border-radius: 8px !important;
        margin: 2px 0 !important;
        display: block !important;
        transition: all 0.2s ease !important;
    }

    /* Hover effects */
    section[data-testid="stSidebar"] a:hover {
        color: #fde047 !important;
        background-color: rgba(250, 204, 21, 0.1) !important;
        transform: scale(1.02) !important;
    }

    /* Active/current page */
    section[data-testid="stSidebar"] a[aria-current="page"] {
        background-color: rgba(250, 204, 21, 0.15) !important;
        color: #fde047 !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

if "admin_logged_in" not in st.session_state or not st.session_state.admin_logged_in:
    st.error("🔒 Please Login.")
    st.stop()

c1, c2, c3 = st.columns([3, 1, 1])
with c1: st.title(" Safety Compliance Dashboard")
with c2:
    if st.button(" Refresh Data"):
        st.rerun()
with c3: 
    if st.button("Logout"): 
        st.session_state.admin_logged_in = False
        st.rerun()

conn = get_connection()
try:
    df = pd.read_sql("SELECT * FROM violations ORDER BY timestamp DESC", conn)
finally:
    conn.close()

if not df.empty:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    
    if 'date' in df.columns:
        df['date_dt'] = pd.to_datetime(df['date']).dt.date
    else:
        df['date_dt'] = df['timestamp'].dt.date


tab1, tab2, tab3 = st.tabs(["📅 Today's Logs", "📆 All Records", "📊 Statistics"])


with tab1:
    today = pd.Timestamp.now().date()
    if df.empty:
        st.info("No logs present.")
    else:
        df_today = df[df['date_dt'] == today]
        
        col_m1, col_m2, col_m3 = st.columns(3)
        total_violations = len(df_today)
        unique_persons = df_today['person_id'].nunique() if not df_today.empty else 0
        helmet_violations = len(df_today[df_today['missing_ppe'].str.contains("Helmet", case=False)]) if not df_today.empty else 0
        
        col_m1.metric("Total Log Entries", total_violations)
        col_m2.metric("⚠️ Unique Persons Violated", unique_persons, 
                     help="Number of different people who violated PPE rules (most important for compliance)")
        col_m3.metric("Critical (Helmet Missing)", helmet_violations)
        
        if total_violations > 0:
            st.info(f"ℹ️ **{unique_persons} unique person(s)** violated safety rules today. Click 'Refresh Data' to see latest detections.")
        
        st.markdown("### 📋 Live Feed Logs")
        
       
        view_mode = st.radio(
            "View Mode",
            ["Grouped (by person)", "Detailed (all entries)"],
            horizontal=True,
            help="Grouped view shows one row per person. Detailed shows all log entries."
        )
        
        if not df_today.empty:
            if view_mode == "Grouped (by person)":
                
                grouped = df_today.groupby(['person_id', 'source']).agg({
                    'missing_ppe': lambda x: ', '.join(sorted(set(', '.join(x).split(', ')))),
                    'video_time': 'first',
                    'status': 'first'
                }).reset_index()
                
                st.dataframe(
                    grouped,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "person_id": "Person ID",
                        "missing_ppe": "Missing Gear",
                        "video_time": "First Detected",
                        "source": "Source",
                        "status": "Status"
                    }
                )
                st.caption(f"Showing {len(grouped)} unique person-video combinations (grouped from {total_violations} total entries)")
            else:
                st.dataframe(
                df_today[['id', 'person_id', 'missing_ppe', 'video_time', 'source', 'status']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "id": "Log ID",
                    "person_id": "Person ID",
                    "missing_ppe": "Missing Gear",
                    "video_time": "Time (Ref)",
                    "source": "Source",
                    "status": "Status"
                }
            )
        else:
            st.success("✅ No violations recorded today!")


with tab2:
    st.markdown("### 🔍 Historical Data")
    
    # Filters
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        sources = ["All"] + list(df['source'].unique()) if not df.empty else []
        sel_source = st.selectbox("Filter Source", sources)
    with c_f2:
        gear_types = ["All", "Helmet", "Shoes", "Goggles", "Vest"]
        sel_gear = st.selectbox("Filter Missing Gear", gear_types)
        
    df_filt = df.copy()
    if sel_source != "All":
        df_filt = df_filt[df_filt['source'] == sel_source]
    if sel_gear != "All":
        df_filt = df_filt[df_filt['missing_ppe'].str.contains(sel_gear, case=False, na=False)]
        
    st.dataframe(
        df_filt,
        use_container_width=True,
        hide_index=True
    )


with tab3:
    if df.empty:
        st.write("Not enough data.")
    else:
        st.markdown("### 📈 Trends & Insights")
        
        c_stats1, c_stats2 = st.columns(2)
        
        with c_stats1:
            st.caption("Common Violations")
            s = df['missing_ppe'].str.split(', ').explode()
            pie_data = s.value_counts().reset_index()
            pie_data.columns = ['Type', 'Count']
            
            pie = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Count", type="quantitative"),
                color=alt.Color(field="Type", type="nominal", scale=alt.Scale(scheme='category10')),
                tooltip=['Type', 'Count']
            )
            st.altair_chart(pie, use_container_width=True)

        with c_stats2:
            st.caption("Violations per Day")
            daily_counts = df.groupby('date_dt').size().reset_index(name='Count')
            bar = alt.Chart(daily_counts).mark_bar().encode(
                x='date_dt:T',
                y='Count:Q',
                tooltip=['date_dt', 'Count']
            )
            st.altair_chart(bar, use_container_width=True)
