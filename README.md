<div align="center">
  <h1>💸 UPI Transaction Pattern Analyzer</h1>
  

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-red?style=for-the-badge)]([https://upi-transaction-pattern-analyzer-byom.streamlit.app/]
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/OKapkoti/da-finance-upi-transaction-pattern-analyzer)

  <p><strong>A comprehensive, full-stack data analytics dashboard for uncovering insights from Unified Payments Interface (UPI) transactions.</strong></p>
</div>

---

## 📌 Project Overview

Digital payments via UPI have grown exponentially, processing billions of transactions monthly. Analyzing these transaction patterns is critical for understanding consumer behavior, monitoring system health, and detecting systemic failures. 

This project provides a **production-grade analytics dashboard** designed for banks, fintech companies, and payment gateways. By ingesting raw transaction data, validating its integrity, and modeling it in an embedded SQLite database, the dashboard allows stakeholders to seamlessly discover:
- Overall payment system performance and volume trends
- High-failure regions, merchants, and banks
- Peak transaction hours to optimize server load balancing
- Demographic-based consumer spending behaviors

---

## ✨ Features

- **Interactive Streamlit Dashboard**: A sleek, multi-page application with intuitive sidebar navigation.
- **Data Quality Analysis**: Automated validation computing integrity scores, missing values, and duplicate rows.
- **Premium Dark-Themed UI**: Modern glassmorphism aesthetic with tailored CSS for a professional analytics experience.
- **Responsive Layout**: Fluid grids and dynamically resizing Plotly charts.
- **KPI Cards**: Stylized metric cards highlighting real-time summary statistics with visual indicators.
- **Transaction Analysis**: Deep-dives into top merchants, sender banks, and preferred payment apps.
- **Peak Hour Analysis**: Identification of the busiest hours and days via interactive heatmaps.
- **Failed Transaction Analysis**: Root-cause exploration of failed payments across dimensions to minimize value lost.
- **User Behavior Analysis**: Demographic profiling to understand which age groups spend the most.
- **Regional Analysis**: Geographic breakdown of transaction volumes and failure rates by state.
- **SQLite Integration**: Fast, structured data querying bypassing Pandas bottlenecks for heavy aggregations.
- **SQL-Based Analytics**: Embedded SQL queries dynamically expanding for transparency and data validation.
- **Plotly Interactive Visualizations**: Transparent, responsive charts (Bar, Pie, Treemap, Line, Heatmap) with hover tooltips.
- **Excel Report Export**: Multi-sheet `.xlsx` generation using XlsxWriter for sharing insights with management.
- **CSV Export**: Raw filtered data extraction for external processing.

---

## 🏗 Project Architecture

```text
       [ Raw CSV Dataset ]
               │
               ▼
      [ Data Validation ]
               │
               ▼
       [ Data Cleaning ]
               │
               ▼
      [ SQLite Database ]
               │
               ▼
        [ SQL Queries ]
               │
               ▼
      [ Pandas Analysis ]
               │
               ▼
   [ Plotly Visualizations ]
               │
               ▼
    [ Streamlit Dashboard ]
               │
               ▼
    [ Excel Report Export ]
```

---

## 📂 Project Structure

```text
da-finance-upi-transaction-pattern-analyzer/
│
├── app.py                   # Main Streamlit application entry point
├── requirements.txt         # Python dependency list
├── README.md                # Project documentation
├── .gitignore               # Ignored files and folders
├── assets/                  
│   └── style.css            # Custom CSS for dark theme and UI elements
├── data/
│   ├── raw/                 # Raw input datasets (CSV)
│   ├── processed/           # Cleaned and processed data
│   └── sample/              # Sample datasets for testing
├── database/
│   └── upi.db               # Embedded SQLite database
├── exports/                 # Generated Excel and CSV reports
└── src/
    ├── __init__.py          # Module initialization
    ├── data_loader.py       # Data ingestion, cleaning, and SQLite integration
    ├── analysis.py          # Business logic and KPI aggregation
    ├── visualizations.py    # Plotly charting functions and unified theme
    └── sql_queries.py       # Centralized SQL query definitions
```

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Pandas** | Data manipulation, cleaning, and preprocessing |
| **NumPy** | Numerical operations and array handling |
| **SQLite** | Embedded relational database for structured querying |
| **SQL** | Aggregation logic and analytical queries |
| **Streamlit** | Frontend dashboard framework and UI rendering |
| **Plotly** | Interactive and responsive data visualizations |
| **XlsxWriter** | Complex Excel report generation and formatting |
| **OpenPyXL** | Excel file reading and writing engine |
| **Git** | Version control |
| **GitHub** | Source code hosting and collaboration |

---

## 📊 Dashboard Pages

The application is modularized into 7 focused analytical pages:

### 1. Overview
The entry point of the dashboard. It calculates high-level KPIs (Total Value, Success Rate, Average Transaction) and provides a rigorous **Data Quality Report** ensuring the underlying dataset is clean, complete, and trustworthy.

### 2. Transaction Analysis
Focuses on where and how money is being spent. It breaks down transaction volumes by **Merchant Category**, reveals the most popular **Payment Apps**, and highlights the top **Sender Banks** driving volume.

### 3. Peak Hour Analysis
Crucial for engineering and infrastructure teams. This page features an hourly trend line and a robust **Weekday vs. Hour Heatmap** to visually identify exactly when the payment gateway is under the most stress.

### 4. Failed Transaction Analysis
A risk-management view that calculates the total **Value Lost** to failed transactions. It breaks down failure rates by bank, device, and region, helping product teams pinpoint where payment drop-offs occur.

### 5. User Behavior Analysis
A demographic deep-dive. It explores transaction patterns across different **Age Groups**, uncovering which demographics spend the most and which apps they prefer to use.

### 6. Regional Analysis
A geographic breakdown mapping transaction volume and failure rates across different **States and Cities**, allowing regional managers to tailor their expansion strategies.

### 7. Export Report
The reporting engine. It allows analysts to instantly download a comprehensive, multi-sheet **Excel Dashboard Report** or extract a raw **CSV file** of the current dataset.

---

## 📈 KPIs

The dashboard actively tracks and calculates the following Key Performance Indicators:
- **Total Transactions (Volume)**
- **Total Value Transacted (INR)**
- **Overall Success Rate (%)**
- **Average Transaction Amount**
- **Failed Transactions (Count)**
- **Pending Transactions (Count)**
- **Total Value Lost to Failures**
- **Dataset Integrity Score**
- **Unique Cities & Banks Connected**

---

## 🗃 Database Design

To ensure the application scales beyond what Pandas can handle efficiently in memory, the system uses an embedded **SQLite** database.

- **Data Flow**: Upon launch, raw CSV data is cleaned and actively loaded into a unified `upi_transactions` SQL table.
- **SQL Aggregations**: Complex analytical queries (e.g., peak hour matrices, regional grouping) are pushed down to the database engine via optimized `SELECT`, `GROUP BY`, and `ORDER BY` statements.
- **Why SQL?**: By leveraging SQL, the application separates data modeling from UI rendering, dramatically improving performance for large datasets and mirroring how enterprise data warehouses operate.

---

## 📉 Visualizations

The dashboard utilizes **Plotly Express** and **Plotly Graph Objects** for all visualizations, ensuring they are highly interactive, responsive, and beautifully styled.
- **Bar Charts**: Used for categorical comparisons (Top Banks, Regions).
- **Pie / Donut Charts**: Used to show market share (Payment Apps).
- **Line Charts**: Used for time-series and hourly trend analysis.
- **Heatmaps**: Used for multi-dimensional cross-tabulations (Hour vs. Day).
- **Treemaps**: Used to visualize hierarchical spending categories.

All charts share a unified, premium dark theme applied globally via a centralized `apply_theme()` function.

---

## 📥 Export Functionality

Data democratization is built directly into the application:
- **Excel Report Generation**: Uses `XlsxWriter` to dynamically generate a multi-sheet `.xlsx` workbook containing structured aggregations for KPIs, Regional Data, and Failed Transactions. 
- **CSV Export**: A one-click download of the cleaned, validated dataset for external integration.

---

## 🚀 Installation

Follow these steps to run the dashboard locally:

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/da-finance-upi-transaction-pattern-analyzer.git

# 2. Navigate to the project directory
cd da-finance-upi-transaction-pattern-analyzer

# 3. Create a virtual environment
python -m venv venv

# 4. Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run the Streamlit dashboard
streamlit run app.py
```

---

## 📸 Screenshots

> *Replace the placeholder URLs below with actual images of your dashboard.*

### Overview
![Overview Dashboard](assets/screenshots/overview.png)

### Transaction Analysis
![Transaction Analysis](assets/screenshots/transaction.png)

### Peak Hour Analysis
![Peak Hour Analysis](assets/screenshots/peak_hour.png)

### Failed Analysis
![Failed Analysis](assets/screenshots/failed.png)

### User Behavior
![User Behavior](assets/screenshots/user_behavior.png)

### Regional Analysis
![Regional Analysis](assets/screenshots/regional.png)

### Export
![Export Page](assets/screenshots/export.png)

---

## 🔮 Future Improvements

- **Real-time Streaming**: Integrate with Kafka/RabbitMQ to analyze live UPI transaction streams.
- **Authentication & Security**: Add robust login systems and role-based access control (RBAC).
- **Machine Learning Integration**: Implement predictive models for transaction failure forecasting and anomaly/fraud detection.
- **Cloud Deployment**: Containerize with Docker and deploy to AWS/GCP for high availability.
- **API Integration**: Create REST API endpoints (using FastAPI) to serve calculated KPIs to other internal microservices.

---

## 👨‍💻 Author

**Your Name**  
Data Analyst / Python Developer  
- 💼 **LinkedIn**: [linkedin.com/in/yourprofile](https://linkedin.com)
- 🐙 **GitHub**: [github.com/yourusername](https://github.com)
- 🌐 **Portfolio**: [yourportfolio.com](https://yourportfolio.com)

---

## ⭐ If you like this project

If you found this project helpful, interesting, or if it helped you learn something new, please consider giving it a **Star** ⭐️ on GitHub! It helps others find the repository and encourages further development.
