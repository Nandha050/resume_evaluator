#!/usr/bin/env python3
"""
Streamlit Cloud deployment entry point for the Resume Evaluation System
"""

import os
import subprocess
import sys

# Set up environment
os.makedirs("data/uploads", exist_ok=True)
os.environ.setdefault("API_BASE_URL", "http://localhost:8000")

# Install spaCy model if needed
try:
    import spacy
    spacy.load("en_core_web_sm")
except OSError:
    print("Installing spaCy model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

# Import and run the dashboard
import streamlit as st
from dashboard import main as dashboard_main

if __name__ == "__main__":
    dashboard_main()