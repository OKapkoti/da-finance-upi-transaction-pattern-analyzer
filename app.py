import streamlit as st
import pandas as pd
import xlsxwriter
from io import BytesIO

from src.data_loader import load_data, validate_and_clean, run_data_quality_check, load_to_sqlite, query_sqlite
from src.analysis import (
    get_overview_kpis, get_transaction_by_category, get_peak_hour_analysis,
    get_day_of_week_analysis, get_monthly_trends, get_failed_analysis,
    get_user_behavior, get_city_analysis, get_payment_app_analysis
)
from src.visualizations import plot_bar, plot_pie, plot_heatmap, plot_line, plot_treemap
from src.sql_queries import (
    PEAK_HOUR_QUERY, FAILED_BY_BANK_QUERY, CATEGORY_QUERY, 
    CITY_QUERY, AGE_GROUP_QUERY, MONTHLY_TREND_QUERY
)

st.set_page_config(page_title="UPI Analyzer", page_icon="💸", layout="wide")

# Load Custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    load_css("assets/style.css")
except Exception as e:
    pass

def render_kpi_card(title, value):
    # Extract emoji if present
    icon = ""
    clean_title = title
    if len(title) > 0 and title[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789':
        parts = title.split(' ', 1)
        if len(parts) > 1:
            icon = parts[0]
            clean_title = parts[1]

    html = f"""<div class="kpi-card">
    <div class="kpi-card-title">{clean_title}</div>
    <div class="kpi-card-value">
        {f'<span class="kpi-icon">{icon}</span>' if icon else ''}
        {value}
    </div>
</div>"""
    return html

@st.cache_data
def prepare_data():
    df = load_data()
    df = validate_and_clean(df)
    quality = run_data_quality_check(df)
    load_to_sqlite(df)
    return df, quality

df, quality = prepare_data()
kpis = get_overview_kpis(df)

# Sidebar for navigation
st.sidebar.title("Navigation")
pages = [
    "🏠 Overview",
    "📊 Transaction Analysis",
    "⏰ Peak Hour Analysis",
    "❌ Failed Transaction Analysis",
    "👥 User Behavior Analysis",
    "🏙️ City & Regional Analysis",
    "📥 Export Report"
]
page = st.sidebar.radio("Go to", pages)

if page == "🏠 Overview":
    st.title("💸 UPI Transaction Pattern Analyzer")
    st.caption("Analyzing digital payment patterns across India")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi_card("📊 Total Transactions", f"{kpis['total_transactions']:,}"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("💰 Total Value", f"₹{kpis['total_value']:,.0f}"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("✅ Success Rate", f"{kpis['success_rate']:.1f}%"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi_card("📈 Avg Transaction", f"₹{kpis['avg_amount']:,.0f}"), unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi_card("❌ Failed Transactions", f"{kpis['failed_count']:,}"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("⏳ Pending Transactions", f"{kpis['pending_count']:,}"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("🏙️ Cities Covered", f"{kpis['city_count']}"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi_card("🏦 Banks Connected", f"{kpis['bank_count']}"), unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Data Quality Report")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi_card("Total Records", f"{quality['total_records']:,}"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("Duplicate Rows", str(quality['duplicate_rows'])), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("Missing Values", str(sum(quality['missing_values'].values()))), unsafe_allow_html=True)
    with col4:
        score = quality['quality_score']
        badge = "🟢" if score >= 90 else "🟡" if score >= 70 else "🔴"
        st.markdown(render_kpi_card("Dataset Integrity Score", f"{badge} {score}%"), unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("🛠️ View Data Pipeline & Missing Values"):
        st.info("""
        **Problem Statement:** Banks and fintech companies lack tools to 
        analyze UPI transaction patterns, peak usage times, failure rates, 
        and user behavior at scale. This dashboard provides instant insights 
        from raw transaction data.
        """)
        st.code("CSV File → Data Validation → SQLite Database → SQL Aggregations → Pandas Processing → Plotly Visualizations → Excel Export")
        missing_df = pd.DataFrame.from_dict(
            quality['missing_values'],
            orient='index',
            columns=['Missing Count']
        )
        st.dataframe(missing_df, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("Overview loaded successfully. Select a page from the sidebar to dive deeper into the analytics.")

elif page == "📊 Transaction Analysis":
    st.title("📊 Transaction Analysis")
    st.caption("Analyze transaction volumes across merchants, apps, and banks.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    cat_df = get_transaction_by_category(df)
    app_df = get_payment_app_analysis(df)
    bank_df = df.groupby('sender_bank')['transaction id'].count().reset_index()
    bank_df.columns = ['sender_bank', 'transaction_count']
    bank_df = bank_df.sort_values('transaction_count', ascending=False)
    
    top_merchant = cat_df.iloc[0]['merchant_category'] if not cat_df.empty else "N/A"
    top_app = app_df.iloc[0]['device_type'] if not app_df.empty else "N/A"
    top_bank = bank_df.iloc[0]['sender_bank'] if not bank_df.empty else "N/A"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(render_kpi_card("🏆 Top Merchant Category", top_merchant), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("📱 Most Used App", top_app), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("🏦 Top Sender Bank", top_bank), unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_bar(cat_df, 'merchant_category', 'transaction_count', 'Volume by Merchant Category'), use_container_width=True)
    with col2:
        status_df = df['transaction_status'].value_counts().reset_index()
        status_df.columns = ['status', 'count']
        st.plotly_chart(plot_pie(status_df, 'status', 'count', 'Transaction Status Breakdown'), use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        top10_merchants = cat_df.head(10)
        st.plotly_chart(plot_bar(top10_merchants, 'merchant_category', 'transaction_count', 'Top 10 Merchants by Volume', horizontal=False), use_container_width=True)
    with col2:
        st.plotly_chart(plot_bar(app_df, 'device_type', 'transaction_count', 'Transactions by Device Type (App)'), use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.plotly_chart(plot_bar(bank_df, 'sender_bank', 'transaction_count', 'Transactions by Bank'), use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"**Insight:** The majority of transactions are driven by **{top_merchant}** category and processed via **{top_app}** apps.")
    
    with st.expander("🔍 View Raw Data & SQL Query"):
        st.dataframe(df.head(100), use_container_width=True)
        st.code(CATEGORY_QUERY, language="sql")

elif page == "⏰ Peak Hour Analysis":
    st.title("⏰ Peak Hour Analysis")
    st.caption("Identify the busiest times and days for transactions.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    hour_df, pivot_df = get_peak_hour_analysis(df)
    day_df = get_day_of_week_analysis(df)
    month_df = get_monthly_trends(df)
    city_df = get_city_analysis(df)
    
    peak_hour = hour_df.loc[hour_df['transaction_count'].idxmax(), 'hour_of_day']
    peak_day = day_df.loc[day_df['transaction_count'].idxmax(), 'day_of_week']
    busiest_city = city_df.iloc[0]['sender_state']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(render_kpi_card("🔥 Peak Hour", f"{peak_hour}:00"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("📅 Peak Day", peak_day), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("🏙️ Busiest Region", busiest_city), unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.plotly_chart(plot_heatmap(pivot_df, "Hour of Day vs Day of Week"), use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_line(hour_df, 'hour_of_day', 'transaction_count', "Volume by Hour"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_bar(day_df, 'day_of_week', 'transaction_count', "Volume by Day of Week"), use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_line(month_df, 'month', 'transaction_count', "Monthly Trends"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_bar(city_df.head(10), 'sender_state', 'total_transactions', "Top 10 States/Cities by Volume"), use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"**Insight:** System load peaks at **{peak_hour}:00** heavily concentrated on **{peak_day}**s.")
        
    with st.expander("🔍 View SQL Query"):
        st.code(PEAK_HOUR_QUERY, language="sql")

elif page == "❌ Failed Transaction Analysis":
    st.title("❌ Failed Transaction Analysis")
    st.caption("Investigate patterns and root causes of failed transactions.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    failed_df = df[df['transaction_status'] == 'FAILED']
    total_failed = len(failed_df)
    value_lost = failed_df['amount (INR)'].sum()
    failure_rate = (total_failed / len(df)) * 100
    avg_failed_amount = failed_df['amount (INR)'].mean() if total_failed > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(render_kpi_card("Total Failed", f"{total_failed:,}"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("Value Lost (₹)", f"₹{value_lost:,.0f}"), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("Failure Rate (%)", f"{failure_rate:.2f}%"), unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi_card("Avg Failed Amount", f"₹{avg_failed_amount:,.0f}"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    by_bank, by_app, by_cat, by_hour, by_city = get_failed_analysis(df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_bar(by_bank, 'sender_bank', 'transaction id', "Failed by Bank"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_bar(by_app, 'device_type', 'transaction id', "Failed by Device (App)"), use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_bar(by_cat, 'merchant_category', 'transaction id', "Failed by Category"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_bar(by_hour, 'hour_of_day', 'transaction id', "Failed by Hour"), use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.plotly_chart(plot_bar(by_city.head(10), 'sender_state', 'transaction id', "Failed by State/City"), use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    worst_bank = by_bank.iloc[0]['sender_bank'] if not by_bank.empty else "N/A"
    st.error(f"**Insight:** The worst performing bank is **{worst_bank}**. High failure rates are observed during peak hours and on specific network conditions.")
    
    with st.expander("🔍 View SQL Query"):
        st.code(FAILED_BY_BANK_QUERY, language="sql")

elif page == "👥 User Behavior Analysis":
    st.title("👥 User Behavior Analysis")
    st.caption("Understand demographic spending patterns and preferences.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    by_age, pref_app, pref_cat = get_user_behavior(df)
    
    # Calculate KPIs
    top_age = by_age.loc[by_age['transaction_count'].idxmax(), 'sender_age_group'] if not by_age.empty else "N/A"
    top_spend = by_age.loc[by_age['total_spend'].idxmax(), 'sender_age_group'] if not by_age.empty else "N/A"
    top_pref_app = pref_app.loc[pref_app['transaction id'].idxmax(), 'device_type'] if not pref_app.empty else "N/A"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(render_kpi_card("🧑 Top Age Group (Vol)", top_age), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("💸 Highest Spend Group", top_spend), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("📱 Top Preferred App", top_pref_app), unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_bar(by_age, 'sender_age_group', 'transaction_count', "Volume by Age Group"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_bar(by_age, 'sender_age_group', 'avg_amount', "Avg Amount by Age Group"), use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_bar(by_age, 'sender_age_group', 'total_spend', "Total Spend by Age Group"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_bar(pref_app, 'sender_age_group', 'transaction id', "Preferred Device Type by Age Group", color='device_type'), use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.plotly_chart(plot_bar(pref_cat, 'sender_age_group', 'transaction id', "Top Spending Category by Age Group", color='merchant_category'), use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.success(f"**Insight:** The **{top_age}** age group represents the highest volume of transactions and spend.")
    
    with st.expander("🔍 View SQL Query"):
        st.code(AGE_GROUP_QUERY, language="sql")

elif page == "🏙️ City & Regional Analysis":
    st.title("🏙️ City & Regional Analysis")
    st.caption("Geographic distribution of transactions and failure rates.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    city_df = get_city_analysis(df)
    
    # KPIs
    top_region = city_df.iloc[0]['sender_state'] if not city_df.empty else "N/A"
    top_region_val = city_df.loc[city_df['total_value'].idxmax(), 'sender_state'] if not city_df.empty else "N/A"
    highest_failure = city_df.loc[city_df['failure_rate'].idxmax(), 'sender_state'] if not city_df.empty else "N/A"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(render_kpi_card("📍 Top Region (Vol)", top_region), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card("💰 Top Region (Value)", top_region_val), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card("⚠️ Highest Failure Region", highest_failure), unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_bar(city_df.head(10), 'sender_state', 'total_transactions', "Top Regions by Volume"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_bar(city_df.head(10), 'sender_state', 'total_value', "Top Regions by Value"), use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_bar(city_df.head(10), 'sender_state', 'failure_rate', "Failure Rate by Region"), use_container_width=True)
    with col2:
        st.plotly_chart(plot_bar(city_df.head(10), 'sender_state', 'avg_amount', "Avg Amount by Region"), use_container_width=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.plotly_chart(plot_treemap(city_df[city_df['total_transactions'] > 0], ['sender_state'], 'total_transactions', "Regional Transaction Distribution"), use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"**Insight:** **{top_region}** leads in overall transaction volume, while **{highest_failure}** requires infrastructure investigation due to high failure rates.")
    
    with st.expander("🔍 View SQL Query"):
        st.code(CITY_QUERY, language="sql")

elif page == "📥 Export Report":
    st.title("📥 Export Report")
    st.caption("Download your analysis results in standardized formats.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.info("""
    **Export Capabilities:**
    - **Excel Report:** A multi-sheet comprehensive report with Executive Summary, Transactions, Failed logs, Peak Hours, and City distributions.
    - **Cleaned CSV:** The raw, deduplicated, and formatted transaction dataset for custom analytics.
    """)
    st.markdown("<br>", unsafe_allow_html=True)
    
    def create_excel_report(df, kpis, failed_df, peak_df, city_df):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#6366f1',
            'font_color': 'white',
            'border': 1
        })
        
        ws1 = workbook.add_worksheet("Executive Summary")
        ws1.write(0, 0, "UPI Transaction Analysis Report", header_format)
        ws1.write(2, 0, "Total Transactions")
        ws1.write(2, 1, kpis['total_transactions'])
        ws1.write(3, 0, "Total Value (INR)")
        ws1.write(3, 1, kpis['total_value'])
        ws1.write(4, 0, "Success Rate")
        ws1.write(4, 1, kpis['success_rate'])
        
        ws2 = workbook.add_worksheet("Transaction Data")
        headers = df.columns.tolist()
        for col, header in enumerate(headers):
            ws2.write(0, col, header, header_format)
        for row, record in enumerate(df.head(10000).values.tolist()):
            for col, value in enumerate(record):
                ws2.write(row + 1, col, str(value))
        
        ws3 = workbook.add_worksheet("Failed Transactions")
        failed_headers = failed_df.columns.tolist()
        for col, header in enumerate(failed_headers):
            ws3.write(0, col, header, header_format)
        for row, record in enumerate(failed_df.values.tolist()):
            for col, value in enumerate(record):
                ws3.write(row + 1, col, str(value))
                
        ws4 = workbook.add_worksheet("Peak Hour Analysis")
        peak_headers = peak_df.columns.tolist()
        for col, header in enumerate(peak_headers):
            ws4.write(0, col, header, header_format)
        for row, record in enumerate(peak_df.values.tolist()):
            for col, value in enumerate(record):
                ws4.write(row + 1, col, str(value))
                
        ws5 = workbook.add_worksheet("City Analysis")
        city_headers = city_df.columns.tolist()
        for col, header in enumerate(city_headers):
            ws5.write(0, col, header, header_format)
        for row, record in enumerate(city_df.values.tolist()):
            for col, value in enumerate(record):
                ws5.write(row + 1, col, str(value))
        
        workbook.close()
        output.seek(0)
        return output

    failed_transactions = df[df['transaction_status'] == 'FAILED']
    peak_hour_df, _ = get_peak_hour_analysis(df)
    region_df = get_city_analysis(df)
    
    col_left, col1, col2, col_right = st.columns([1, 2, 2, 1])
    with col1:
        excel_data = create_excel_report(df, kpis, failed_transactions, peak_hour_df, region_df)
        st.download_button(
            label="📥 Download Excel Report",
            data=excel_data,
            file_name="upi_analysis_report.xlsx",
            mime="application/vnd.ms-excel"
        )
    with col2:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_data,
            file_name="upi_transactions_cleaned.csv",
            mime="text/csv"
        )
