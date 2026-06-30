SELECT
    'bronze_listings' AS model_name,
    COUNT(*) AS total_rows,
    MAX(CREATED_AT) AS latest_load_timestamp,
    DATEDIFF('hour', MAX(CREATED_AT), CURRENT_TIMESTAMP()) AS hours_since_last_load
FROM AIRBNB.bronze.bronze_listings

UNION ALL


SELECT
    'bronze_bookings' AS model_name,
    COUNT(*) AS total_rows,
    MAX(CREATED_AT) AS latest_load_timestamp,
    DATEDIFF('hour', MAX(CREATED_AT), CURRENT_TIMESTAMP()) AS hours_since_last_load
FROM AIRBNB.bronze.bronze_bookings

UNION ALL


SELECT
    'bronze_hosts' AS model_name,
    COUNT(*) AS total_rows,
    MAX(CREATED_AT) AS latest_load_timestamp,
    DATEDIFF('hour', MAX(CREATED_AT), CURRENT_TIMESTAMP()) AS hours_since_last_load
FROM AIRBNB.bronze.bronze_hosts


ORDER BY model_name