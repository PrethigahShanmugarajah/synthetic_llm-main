import json
from typing import Union
from synthetic_data.llm_client import GeminiClient
from synthetic_data.input_parser import Schema, Input
from synthetic_data.output_processor import parse_generated_data, validate_data, postprocess_data

class DataGenerator:
    def __init__(self, llm_client: GeminiClient):
        self.llm_client = llm_client

    def generate_synthetic_data(
        self,
        schema_type: str,
        schema_definition: Union[list, dict],
        hints: dict,
        output_format: str,
        num_rows: int,
        output_path: str,
        extra_hints: str = ""
    ):
        """Generates synthetic data based on the provided schema and hints."""

        # 1. Input Validation
        schema = Schema(schema_type, schema_definition, hints)
        input_data = Input(schema, output_format, num_rows, output_path)
        input_data.validate()

        # 2. Prompt Engineering
        prompt = self._build_prompt(input_data, extra_hints)

        # 3. LLM Interaction
        generated_data_str = self.llm_client.generate_data(prompt)

        if generated_data_str is None:
            print("Failed to generate data.")
            return

        # 4. Output Processing
        parsed_data = parse_generated_data(
            generated_data_str, schema_type, output_format
        )

        if parsed_data is None:
            print("Failed to parse generated data.")
            return

        validate_data(parsed_data, schema)
        processed_data = postprocess_data(parsed_data)

        return processed_data  # Return the data instead of writing to file

    def _build_prompt(self, input_data: Input, extra_hints: str) -> str:
        """Builds a prompt for the LLM based on the input schema and hints."""
        if input_data.schema.type == "tabular":
            return self._build_tabular_prompt(input_data, extra_hints)
        elif input_data.schema.type == "json":
            return self._build_json_prompt(input_data, extra_hints)
        else:
            raise ValueError("Invalid schema type.")

    def _build_tabular_prompt(self, input_data: Input, extra_hints: str) -> str:
        """Builds a prompt for tabular data generation."""
        schema_def = input_data.schema.definition
        hints = input_data.schema.hints
        num_rows = input_data.num_rows
        output_format = input_data.output_format

        prompt = f"Generate {num_rows} rows of synthetic data for a table with the following schema:\n\n"
        prompt += "| Column Name | Data Type | Constraints | Description |\n"
        prompt += "|---|---|---|---|\n"
        for col in schema_def:
            name = col["name"]
            data_type = col["data_type"]
            constraints = col.get("constraints", "")
            description = hints.get(name, "")
            prompt += f"| {name} | {data_type} | {constraints} | {description} |\n"

        if extra_hints:
            prompt += f"\nAdditional Hints:\n{extra_hints}\n"

        prompt += f"\nGenerate the data in {output_format.upper()} format. "
        prompt += "Ensure that all constraints and data types are respected. "

        if output_format.lower() == "json":
            prompt += "Provide each row as a JSON object within a JSON array."

        return prompt

    def _build_json_prompt(self, input_data: Input, extra_hints: str) -> str:
        """Builds a prompt for JSON data generation."""
        schema_def = input_data.schema.definition
        hints = input_data.schema.hints
        num_rows = input_data.num_rows
        output_format = input_data.output_format

        prompt = f"Generate {num_rows} sample JSON objects that conform to the following JSON schema:\n\n"
        prompt += f"`json\n{json.dumps(schema_def, indent=2)}\n`\n\n"

        if hints:
            prompt += "Schema Hints:\n"
            for key, value in hints.items():
                prompt += f"- {key}: {value}\n"

        if extra_hints:
            prompt += f"\nAdditional Hints:\n{extra_hints}\n"

        prompt += "\nProvide the output as a single JSON array where each element is a JSON object conforming to the schema."

        return prompt