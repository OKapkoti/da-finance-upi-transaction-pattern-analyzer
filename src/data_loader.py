import pandas as pd
import sqlite3
import os

def load_data():
    raw_folder = "data/raw/"
    files = os.listdir(raw_folder)
    csv_files = [f for f in files if f.endswith('.csv')]
    df = pd.read_csv(raw_folder + csv_files[0])
    return df

def validate_and_clean(df):
    df = df.drop_duplicates()
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col])
            except:
                pass
    return df

def run_data_quality_check(df):
    total_fields = len(df) * len(df.columns)
    missing_fields = df.isnull().sum().sum()
    quality_score = round(
        ((total_fields - missing_fields) / total_fields) * 100, 2
    )
    return {
        "total_records": len(df),
        "total_columns": len(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "quality_score": quality_score,
        "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
    }

def load_to_sqlite(df, table_name="upi_transactions",
                   db_path="database/upi.db"):
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(db_path)
    # Make a copy to avoid modifying the original dataframe
    df_sql = df.copy()
    if 'timestamp' in df_sql.columns:
        df_sql['timestamp'] = df_sql['timestamp'].astype(str)
    df_sql.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def query_sqlite(query, db_path="database/upi.db"):
    conn = sqlite3.connect(db_path)
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result
