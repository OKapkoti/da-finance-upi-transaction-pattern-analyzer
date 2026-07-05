import pandas as pd

def get_overview_kpis(df):
    total_transactions = len(df)
    total_value = df['amount (INR)'].sum()
    success_rate = (df['transaction_status'] == 'SUCCESS').mean() * 100
    avg_amount = df['amount (INR)'].mean()
    failed_count = (df['transaction_status'] == 'FAILED').sum()
    pending_count = len(df) - (df['transaction_status'] == 'SUCCESS').sum() - failed_count
    return {
        "total_transactions": total_transactions,
        "total_value": total_value,
        "success_rate": success_rate,
        "avg_amount": avg_amount,
        "failed_count": failed_count,
        "pending_count": pending_count,
        "city_count": df['sender_state'].nunique(),
        "bank_count": df['sender_bank'].nunique()
    }

def get_transaction_by_category(df):
    return df[df['transaction_status'] == 'SUCCESS'].groupby('merchant_category').agg(
        transaction_count=('transaction id', 'count'),
        total_value=('amount (INR)', 'sum')
    ).reset_index().sort_values('total_value', ascending=False)

def get_peak_hour_analysis(df):
    # Already have hour_of_day and day_of_week
    # Create pivot table hour vs day of week
    pivot_df = pd.pivot_table(
        df, values='transaction id', index='hour_of_day',
        columns='day_of_week', aggfunc='count', fill_value=0
    )
    # Order days correctly
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_df = pivot_df.reindex(columns=[d for d in days_order if d in pivot_df.columns])
    
    hour_df = df.groupby('hour_of_day')['transaction id'].count().reset_index()
    hour_df.columns = ['hour_of_day', 'transaction_count']
    
    return hour_df, pivot_df

def get_day_of_week_analysis(df):
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    res = df.groupby('day_of_week')['transaction id'].count().reset_index()
    res['day_of_week'] = pd.Categorical(res['day_of_week'], categories=days_order, ordered=True)
    res = res.sort_values('day_of_week')
    res.columns = ['day_of_week', 'transaction_count']
    return res

def get_monthly_trends(df):
    df['month'] = df['timestamp'].dt.to_period('M').astype(str)
    res = df.groupby('month').agg(
        transaction_count=('transaction id', 'count'),
        total_value=('amount (INR)', 'sum')
    ).reset_index().sort_values('month')
    return res

def get_failed_analysis(df):
    failed_df = df[df['transaction_status'] == 'FAILED']
    by_bank = failed_df.groupby('sender_bank')['transaction id'].count().reset_index().sort_values('transaction id', ascending=False)
    by_app = failed_df.groupby('device_type')['transaction id'].count().reset_index().sort_values('transaction id', ascending=False)
    by_category = failed_df.groupby('merchant_category')['transaction id'].count().reset_index().sort_values('transaction id', ascending=False)
    by_hour = failed_df.groupby('hour_of_day')['transaction id'].count().reset_index().sort_values('transaction id', ascending=False)
    by_city = failed_df.groupby('sender_state')['transaction id'].count().reset_index().sort_values('transaction id', ascending=False)
    return by_bank, by_app, by_category, by_hour, by_city

def get_user_behavior(df):
    by_age = df.groupby('sender_age_group').agg(
        transaction_count=('transaction id', 'count'),
        avg_amount=('amount (INR)', 'mean'),
        total_spend=('amount (INR)', 'sum')
    ).reset_index().sort_values('total_spend', ascending=False)
    
    pref_app = df.groupby(['sender_age_group', 'device_type'])['transaction id'].count().reset_index()
    pref_app = pref_app.sort_values(['sender_age_group', 'transaction id'], ascending=[True, False]).drop_duplicates('sender_age_group')
    
    pref_cat = df.groupby(['sender_age_group', 'merchant_category'])['transaction id'].count().reset_index()
    pref_cat = pref_cat.sort_values(['sender_age_group', 'transaction id'], ascending=[True, False]).drop_duplicates('sender_age_group')
    
    return by_age, pref_app, pref_cat

def get_city_analysis(df):
    res = df.groupby('sender_state').agg(
        total_transactions=('transaction id', 'count'),
        total_value=('amount (INR)', 'sum'),
        avg_amount=('amount (INR)', 'mean')
    )
    failed = df[df['transaction_status'] == 'FAILED'].groupby('sender_state')['transaction id'].count()
    res['failed_count'] = failed
    res['failed_count'] = res['failed_count'].fillna(0)
    res['failure_rate'] = (res['failed_count'] / res['total_transactions']) * 100
    return res.reset_index().sort_values('total_transactions', ascending=False)

def get_payment_app_analysis(df):
    res = df.groupby('device_type').agg(
        transaction_count=('transaction id', 'count'),
        total_value=('amount (INR)', 'sum')
    )
    failed = df[df['transaction_status'] == 'FAILED'].groupby('device_type')['transaction id'].count()
    res['failed_count'] = failed
    res['failed_count'] = res['failed_count'].fillna(0)
    res['failure_rate'] = (res['failed_count'] / res['transaction_count']) * 100
    return res.reset_index().sort_values('transaction_count', ascending=False)
