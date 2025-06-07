import pandas as pd
import json

class Schema:
    def __init__(self, schema_type, definition, hints=None):
        self.type = schema_type
        self.definition = definition
        self.hints = hints or {}

    def validate(self):
        """Validates the schema definition."""
        if self.type == "tabular":
            if not isinstance(self.definition, list):
                raise ValueError("Tabular schema must be a list of column definitions.")
            for col in self.definition:
                if not all(k in col for k in ["name", "data_type"]):
                    raise ValueError("Each column must have 'name' and 'data_type'.")

        elif self.type == "json":
            try:
                json.loads(json.dumps(self.definition))  # Check for valid JSON structure
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON schema provided.")
        else:
            raise ValueError("Invalid schema type. Must be 'tabular' or 'json'.")

class Input:
    def __init__(self, schema, output_format, num_rows, output_path):
        self.schema = schema
        self.output_format = output_format
        self.num_rows = num_rows
        self.output_path = output_path

    def validate(self):
        """Validates the input parameters."""
        self.schema.validate()
        if self.output_format not in ["csv", "parquet", "json"]:
            raise ValueError("Invalid output format. Must be 'csv', 'parquet', or 'json'.")
        if self.num_rows <= 0:
            raise ValueError("Number of rows must be greater than 0.")

def parse_tabular_schema_from_csv(csv_file):
    """Parses tabular schema and hints from an uploaded CSV file."""
    try:
        df = pd.read_csv(csv_file)
        if not all(col in df.columns for col in ["name", "data_type"]):
            raise ValueError("CSV must contain 'name' and 'data_type' columns.")

        schema_definition = df[["name", "data_type", "constraints"]].fillna("").to_dict("records")
        hints = {}
        if "hint" in df.columns:
            for _, row in df.iterrows():
                if pd.notnull(row["hint"]):
                    hints[row["name"]] = row["hint"]
        return schema_definition, hints
    except Exception as e:
        raise ValueError(f"Error processing CSV file: {e}")

def parse_json_schema_from_text(schema_text):
    """Parses a JSON schema from a text input."""
    try:
        schema_definition = json.loads(schema_text)
        return schema_definition
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON schema.")