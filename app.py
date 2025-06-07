import streamlit as st
import pandas as pd
import json
import io
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import pyarrow as pa
import pyarrow.parquet as pq

# Import from synthetic_data modules
from synthetic_data.generator import DataGenerator
from synthetic_data.llm_client import GeminiClient
from synthetic_data.input_parser import (
    Schema,
    Input,
    parse_tabular_schema_from_csv,
    parse_json_schema_from_text,
)
from synthetic_data.output_processor import (
    parse_generated_data,
    validate_data,
    postprocess_data
)

def main():
    st.title("Synthetic Data Generator")

    # Input Section
    with st.expander("Schema Input", expanded=True):
        schema_type = st.selectbox("Schema Type", ["tabular", "json"])
        uploaded_file = st.file_uploader(
            "Upload Schema Definition (CSV for tabular, TXT for JSON)",
            type=["csv", "txt"]
        )
        extra_hints = st.text_area(
            "Additional Hints (Optional)",
            placeholder="Enter any additional hints or instructions for data generation, one per line."
        )

        schema_definition = None
        hints_dict = None

        if uploaded_file:
            if schema_type == "tabular":
                try:
                    schema_definition, hints_dict = parse_tabular_schema_from_csv(uploaded_file)
                    st.write("Schema Definition (from CSV):")
                    st.dataframe(pd.DataFrame(schema_definition))
                    if hints_dict:
                        st.write("Hints (from CSV):")
                        st.write(hints_dict)
                except ValueError as e:
                    st.error(str(e))
            else:  # schema_type == "json"
                schema_text = uploaded_file.read().decode("utf-8")
                try:
                    schema_definition = parse_json_schema_from_text(schema_text)
                    st.write("Schema Definition (from TXT):")
                    st.json(schema_definition)
                except ValueError as e:
                    st.error(str(e))

    # Other Parameters
    num_rows = st.number_input("Number of Rows/Objects", min_value=1, max_value=1000, value=10)
    output_format = st.selectbox("Output Format", ["csv", "parquet", "json"])
    # Remove output_path input

    # Generate Button
    if st.button("Generate Data"):
        if schema_definition:
            with st.spinner("Generating data..."):
                try:
                    # Initialize Gemini Client and Data Generator
                    gemini_client = GeminiClient()
                    data_generator = DataGenerator(gemini_client)

                    # Generate data
                    generated_data = data_generator.generate_synthetic_data(
                        schema_type,
                        schema_definition,
                        hints_dict,
                        output_format,
                        num_rows,
                        None,  # Pass None for output_path
                        extra_hints,
                    )

                    # Display data if generation was successful
                    if generated_data:
                        st.success("Data generation successful!")
                        st.write("Generated Data:")
                        if schema_type == "tabular":
                            st.dataframe(generated_data)
                        elif schema_type == "json":
                            st.json(generated_data)

                except Exception as e:  # Catch any error during the process
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please provide a valid schema.")

if __name__ == "__main__":
    main()