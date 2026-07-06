import pandas as pd
import pytest
from pipeline.transform import transform
from pipeline.validate import validate_weather_data

# mock data 
MOCK_API_RESPONSE = {
    "hourly": {
        "time": ["2026-07-04T00:00", "2026-07-04T01:00"],
        "temperature_2m": [26.1, 25.7],
        "precipitation": [0.0, 0.1],
        "windspeed_10m": [5.2, 3.9]
    }
}

# --- TRANSFORMATION TESTS ---

def test_transform_returns_dataframe():
    """Does transform return a valid Pandas DataFrame?"""
    # Act
    result = transform(MOCK_API_RESPONSE, city="Lagos")
    
    # Assert
    assert isinstance(result, pd.DataFrame), "Expected a Pandas DataFrame output!"


def test_transform_adds_city_column():
    """Does the city column contain the correct value?"""
    target_city = "Abuja"
    
    # Act
    result = transform(MOCK_API_RESPONSE, city=target_city)
    
    # Assert
    assert 'city' in result.columns, "The 'city' column is missing entirely!"
    assert (result['city'] == target_city).all(), f"Not all rows matched the city: {target_city}"


# --- VALIDATION TESTS ---

def test_validate_catches_nulls():
    """Does validation return False when given null data in a critical column?"""
    # 1. Grab a clean DataFrame from our transform logic
    clean_df = transform(MOCK_API_RESPONSE, city="Kano")
    
    # 2. Intentionally corrupt the data by inserting a None/Null value into a critical column
    clean_df.loc[0, 'temperature_2m'] = None
    
    # Act: Run it through the pipeline gatekeeper
    validation_result = validate_weather_data(clean_df)
    
    # Assert: should explicitly catch the null and drop a False flag
    assert validation_result is False, "Validation should have failed due to null critical data!"