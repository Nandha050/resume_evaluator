import streamlit as st
import os

# Set up environment
os.makedirs("data/uploads", exist_ok=True)
os.environ.setdefault("API_BASE_URL", "http://localhost:8000")

# Import and run the dashboard
from dashboard import main as dashboard_main

if __name__ == "__main__":
    dashboard_main()
