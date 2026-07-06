import logging

logger = logging.getLogger(__name__)

def validate_weather_data(df, city=None):
    """
    Validates transformed weather data against business rules.
    Returns True if valid, False otherwise.
    """
    logger.info("Starting data validation checks...")
    is_valid = True

    # Check 1: No null values in critical columns, returns error
    critical_columns = ['temperature_2m', 'time', 'city']
    for col in critical_columns:
        null_count = df[col].isnull().sum()
        if null_count > 0:
            logger.error(f"Validation Failed: Column '{col}' contains {null_count} null values!")
            is_valid = False
        else:
            logger.info(f"Check Passed: Column '{col}' has zero null values.")

    # Check 2: Row count check (Exactly 72 rows per city), warning if otherwise
    expected_rows = 72
    city_counts = df['city'].value_counts()
    for city, count in city_counts.items():
        if count != expected_rows:
            logger.warning(f"Validation Warning: {city} has {count} rows, expected exactly {expected_rows}!")
            
        else:
            logger.info(f"Check Passed: {city} has exactly {expected_rows}.")


    # Check 3: Temperature range check, warning if otherwise
    for city in df['city'].unique():
        city_df = df[df['city'] == city]
        out_of_range = (~city_df['temperature_2m'].between(10,50)).sum()

        if out_of_range > 0:
            logger.warning(f"Validation Warning: {city} has {out_of_range} temperature values outside the allowed range (10°C to 50°C)!")
        else:
            logger.info(f"Check Passed: All temperatures for {city} are within range.")

    if is_valid:
        logger.info("All critical validation checks passed.")
    
    return is_valid  # always returns, whether True or False