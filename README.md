# 🧠 synthetic_llm-main

A Python-based tool that uses Large Language Models (LLMs) like LLaMA2-Chat or GPT to generate structured, realistic synthetic test data from user-defined JSON schemas.

## 🔍 Description

This project automates the generation of diverse test datasets using LLMs. It accepts a JSON schema, creates a prompt, sends it to the LLM, and processes the response into clean, schema-compliant JSON files. Ideal for QA testing, benchmarking, and educational use.

## 🚀 Features

- ✅ Schema-driven test data generation
- 🤖 LLM prompt automation (OpenAI / LLaMA2 compatible)
- 🧾 Structured JSON output
- 🧹 Output validation and formatting
- 🔁 Easy-to-customize modular codebase

## 📦 Technologies Used

| Tool/Library         | Purpose                                |
|----------------------|----------------------------------------|
| Python 3.12          | Core programming language              |
| Transformers         | Hugging Face model integration         |
| JSON                 | Input schema and output format         |
| python-dotenv        | Secure API key handling                |
| argparse / PyYAML    | Command-line and config parsing        |

## 🛠️ How to Use

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
