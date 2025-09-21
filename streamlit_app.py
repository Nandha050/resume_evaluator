#!/usr/bin/env python3
"""
Streamlit Cloud deployment entry point for the Resume Evaluation System
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def check_spacy_model():
    """Check if spaCy model is available"""
    try:
        import spacy
        spacy.load("en_core_web_sm")
        print("✅ spaCy model available")
        return True
    except OSError:
        print("⚠️ spaCy model not found - app will work with limited NLP features")
        return False

def start_backend():
    """Start FastAPI backend in background"""
    try:
        print("🚀 Starting FastAPI backend...")
        # Use uvicorn to start the backend
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--log-level", "error"
        ], check=True)
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def main():
    """Main entry point for Streamlit Cloud"""
    print("🎯 Resume Evaluation System - Streamlit Cloud Deployment")
    print("=" * 60)
    
    # Check spaCy model
    check_spacy_model()
    
    # Create necessary directories
    os.makedirs("data/uploads", exist_ok=True)
    os.makedirs(".streamlit", exist_ok=True)
    
    # Start backend in background thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait for backend to start
    print("⏳ Waiting for backend to start...")
    time.sleep(5)
    
    # Import and run the dashboard
    try:
        import streamlit as st
        from dashboard import main as dashboard_main
        
        print("✅ Starting Streamlit dashboard...")
        dashboard_main()
        
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        # Fallback: run dashboard directly
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"], check=True)

if __name__ == "__main__":
    main()
