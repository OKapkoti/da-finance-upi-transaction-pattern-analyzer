PEAK_HOUR_QUERY = """
SELECT 
    hour_of_day as hour,
    COUNT(*) as transaction_count,
    ROUND(SUM("amount (INR)"), 2) as total_amount,
    ROUND(AVG("amount (INR)"), 2) as avg_amount
FROM upi_transactions
WHERE transaction_status = 'SUCCESS'
GROUP BY hour
ORDER BY transaction_count DESC
"""

FAILED_BY_BANK_QUERY = """
SELECT 
    sender_bank as bank_col,
    COUNT(*) as failed_count,
    ROUND(SUM("amount (INR)"), 2) as value_lost,
    ROUND(COUNT(*) * 100.0 / 
        (SELECT COUNT(*) FROM upi_transactions 
         WHERE transaction_status = 'FAILED'), 2) as percentage
FROM upi_transactions
WHERE transaction_status = 'FAILED'
GROUP BY sender_bank
ORDER BY failed_count DESC
"""

CATEGORY_QUERY = """
SELECT 
    merchant_category as category_col,
    COUNT(*) as transaction_count,
    ROUND(SUM("amount (INR)"), 2) as total_value,
    ROUND(AVG("amount (INR)"), 2) as avg_transaction
FROM upi_transactions
WHERE transaction_status = 'SUCCESS'
GROUP BY merchant_category
ORDER BY total_value DESC
"""

CITY_QUERY = """
SELECT
    sender_state as city_col,
    COUNT(*) as total_transactions,
    ROUND(SUM("amount (INR)"), 2) as total_value,
    ROUND(AVG("amount (INR)"), 2) as avg_amount,
    SUM(CASE WHEN transaction_status = 'FAILED' THEN 1 ELSE 0 END) as failed_count
FROM upi_transactions
GROUP BY sender_state
ORDER BY total_transactions DESC
"""

AGE_GROUP_QUERY = """
SELECT
    sender_age_group as age_col,
    COUNT(*) as transaction_count,
    ROUND(AVG("amount (INR)"), 2) as avg_amount,
    ROUND(SUM("amount (INR)"), 2) as total_spend
FROM upi_transactions
GROUP BY sender_age_group
ORDER BY total_spend DESC
"""

MONTHLY_TREND_QUERY = """
SELECT
    strftime('%Y-%m', timestamp) as month,
    COUNT(*) as transaction_count,
    ROUND(SUM("amount (INR)"), 2) as total_value
FROM upi_transactions
GROUP BY month
ORDER BY month ASC
"""
