from synthetic_data.llm_client import GeminiClient

partial_data = [
    { "email": "alice@mail.com", "signup_date": "2023-06-01", "is_verified": True },
    { "email": "bob@domain.net", "signup_date": "2022-12-18", "is_verified": False }
]

client = GeminiClient()
result = client.generate_data(partial_data, "Add a 'user_id' and a realistic 'name' for each entry.")
print(result)