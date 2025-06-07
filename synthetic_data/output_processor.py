import pandas as pd
import json
import io
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def parse_generated_data(data_str, schema_type, output_format):
    """Parses the generated data string into a Pandas DataFrame or a list of JSON objects."""
    if schema_type == "tabular":
        if output_format == "csv":
            return pd.read_csv(io.StringIO(data_str))
        elif output_format == "parquet":
            # Convert CSV string to DataFrame, then to Parquet
            df = pd.read_csv(io.StringIO(data_str))
            return df
        elif output_format == "json":
            # Convert JSON string to DataFrame
            try:
                data = json.loads(data_str)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                else:
                    print("Warning: JSON data is not an array. Attempting to parse as single object.")
                    return pd.DataFrame([data])
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            raise ValueError("Invalid output format for tabular data.")
    elif schema_type == "json":
        try:
            data = json.loads(data_str)
            if isinstance(data, list):
                return data  # Return list of JSON objects
            else:
                print("Warning: JSON data is not an array. Returning as is.")
                return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        raise ValueError("Invalid schema type.")

def validate_data(data, schema):
    """Validates the generated data against the schema (if applicable)."""
    if schema.type == "tabular":
        # Basic type validation for tabular data
        for col_def in schema.definition:
            col_name = col_def["name"]
            expected_type = col_def["data_type"]

            if col_name not in data.columns:
                raise ValueError(f"Column {col_name} is missing in generated data.")

            # Basic type validation
            if expected_type.lower() == "int":
                if not pd.api.types.is_integer_dtype(data[col_name]):
                    raise ValueError(f"Column {col_name} is not of type int.")
            elif expected_type.lower() == "float" or expected_type.lower() == "decimal":
                if not pd.api.types.is_float_dtype(data[col_name]):
                    raise ValueError(f"Column {col_name} is not of type float.")
            elif expected_type.lower() == "string" or expected_type.lower() == "varchar":
                if not pd.api.types.is_string_dtype(data[col_name]):
                    raise ValueError(f"Column {col_name} is not of type string.")
            elif expected_type.lower() == "date":
                try:
                    pd.to_datetime(data[col_name])
                except ValueError:
                    raise ValueError(f"Column {col_name} is not of type date.")

    elif schema.type == "json":
        # Use jsonschema to validate JSON data
        try:
            validate(instance=data, schema=schema.definition)
        except ValidationError as e:
            raise ValueError(f"JSON data validation failed: {e}")

def postprocess_data(data):
    """Applies post-processing steps to the data (if needed)."""
    # Add your post-processing logic here
    return data