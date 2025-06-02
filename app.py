import streamlit as st
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import openai  # Optional: only if using OpenAI API

# --- Set up OpenAI (Optional) ---
# openai.api_key = "your-api-key-here"

# --- Page UI ---
st.set_page_config(page_title="AI Math Tutor", layout="centered")
st.title("🧮 AI Tutor for Math Problems")
st.write("Enter a math problem below. The AI will solve and explain it step-by-step.")

# --- User Input ---
user_input = st.text_input("Enter a math equation or expression (e.g., solve x**2 - 4 = 0)")

# --- Core Logic ---
def solve_expression(expr_str):
    try:
        if "=" in expr_str:
            lhs, rhs = expr_str.split("=")
            lhs_expr = parse_expr(lhs.strip())
            rhs_expr = parse_expr(rhs.strip())
            eq = sp.Eq(lhs_expr, rhs_expr)
            symbol = list(eq.free_symbols)[0]
            solution = sp.solve(eq, symbol)
        else:
            expr = parse_expr(expr_str)
            solution = sp.simplify(expr)

        return solution
    except Exception as e:
        return f"❌ Error: {str(e)}"


from openai import OpenAI

# Initialize OpenRouter client with your API key and base URL
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["OPENROUTER_API_KEY"],
)

def get_explanation_with_openrouter(prompt):
    try:
        completion = client.chat.completions.create(
            model="mistralai/devstral-small:free",
            messages=[
                {"role": "system", "content": "You are a helpful math tutor who explains step-by-step solutions."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error while generating explanation: {str(e)}"

# --- Solve Button ---
if st.button("Solve"):
    if user_input.strip() == "":
        st.warning("Please enter a math problem.")
    else:
        st.subheader("🧮 SymPy Result:")
        result = solve_expression(user_input)
        st.code(result)

        st.subheader("📘 Explanation:")
        explanation = get_explanation_with_openrouter(user_input)
        st.markdown(explanation)
