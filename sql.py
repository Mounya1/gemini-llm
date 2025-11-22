import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini client
client = genai.Client(api_key=API_KEY)


def generate_sql(question, prompt):
    combined_prompt = prompt + "\nQuestion: " + question
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=combined_prompt
    )
    return response.text.strip()  # Remove extra whitespace


def read_sql_query(sql, db):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            conn.commit()  # commits any changes (needed for INSERT/UPDATE/DELETE)
        return rows
    except Exception as e:
        return f"Error executing SQL: {e}"



st.set_page_config(page_title="Natural Language to SQL Query (Gemini 2.0)", layout="wide")
st.header("Gemini 2.0 App: Natural Language → SQL Query")

prompt = """
You are an expert in converting natural language questions into SQL queries.
The database has the following table: STUDENT(NAME, CLASS, SECTION).

Examples:
- "How many entries of records are present?" → SELECT COUNT(*) FROM STUDENT;
- "What are the names of students in class TENTH?" → SELECT NAME FROM STUDENT WHERE CLASS='TENTH';

Rules:
- Do NOT include triple quotes in the SQL.
- Output only the SQL query, no extra text.
"""

# User input
question = st.text_input("Enter your question related to the Student database:")
submit = st.button("Generate SQL Query")

if submit:
    
    sql_query = generate_sql(question, prompt)
    st.subheader("Generated SQL Query:")
    st.code(sql_query, language='sql')

    
    result = read_sql_query(sql_query, 'student.db')

    st.subheader("Query Result:")
    if isinstance(result, str):  # Error case
        st.error(result)
    elif result:
        st.table(result)
    else:
        st.write("No results found.")
