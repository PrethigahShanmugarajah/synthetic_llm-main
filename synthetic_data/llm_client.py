import google.generativeai as genai
import os
import json

class GeminiClient:
    def __init__(self, api_key=None, model_name="models/gemini-1.5-pro"):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key not found. Set the GOOGLE_API_KEY environment variable.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_data_from_prompt(self, prompt):
        """Generates synthetic data using a raw prompt (used for schema-based generation)."""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating data with Gemini: {e}")
            return None

    def generate_data_from_partial(self, existing_data, missing_fields_description):
        """Fills missing fields for predefined JSON records (used in demo mode)."""
        try:
            prompt = (
                f"The following is a list of JSON records:\n\n"
                f"{json.dumps(existing_data, indent=2)}\n\n"
                f"{missing_fields_description}\n"
                "Return the result as a complete JSON array with all fields filled in. No markdown."
            )
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                return response_text
        except Exception as e:
            print(f"Error generating augmented data: {e}")
            return None





































































































# import google.generativeai as genai
# import os

# class GeminiClient:
#     def __init__(self, api_key=None, model_name="models/gemini-pro"):
#         self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
#         if not self.api_key:
#             raise ValueError("Google API key not found. Set the GOOGLE_API_KEY environment variable.")
#         genai.configure(api_key=self.api_key)
#         self.model = genai.GenerativeModel(model_name)

#     def generate_data(self, prompt):
#         """Generates synthetic data using the Gemini model."""
#         try:
#             response = self.model.generate_content(prompt)
#             return response.text
#         except Exception as e:
#             print(f"Error generating data with Gemini: {e}")
#             return None