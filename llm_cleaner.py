from groq import Groq
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Get API key from environment (SAFE)
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_data(df):
    sample = df.head(10).to_string()

    prompt = f"""
    You are a data cleaning expert.

    Analyze this dataset:
    {sample}

    Suggest:
    - data issues
    - cleaning steps
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def smart_clean(df):
    df = df.copy()

    df.drop_duplicates(inplace=True)

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col].fillna(df[col].median(), inplace=True)
        else:
            df[col].fillna(df[col].mode()[0], inplace=True)

    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()

    return df
