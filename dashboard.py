import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Configure Streamlit page
st.set_page_config(
    page_title="Resume Evaluation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-card {
        border-left-color: #28a745;
    }
    .warning-card {
        border-left-color: #ffc107;
    }
    .danger-card {
        border-left-color: #dc3545;
    }
</style>
""", unsafe_allow_html=True)

def make_api_request(endpoint, method="GET", data=None, files=None):
    """Make API request with error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, data=data, files=files)
            else:
                # For form data (like evaluation endpoint), use data parameter
                response = requests.post(url, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to API. Please ensure the backend server is running.")
        return None
    except Exception as e:
        st.error(f"Error making API request: {str(e)}")
        return None

def main():
    # Check if user has selected a role
    if 'user_role' not in st.session_state:
        show_landing_page()
    else:
        # Show role-specific interface
        if st.session_state.user_role == 'placement_officer':
            show_placement_officer_interface()
        elif st.session_state.user_role == 'student':
            show_student_interface()

def show_landing_page():
    """Show landing page with role selection"""
    st.markdown('<h1 class="main-header">🎯 Automated Resume Evaluation System</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 3rem;">
        <p style="font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
            AI-powered resume evaluation system for Innomatics Research Labs
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two main cards
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
        ">
            <h2 style="margin-top: 0; font-size: 1.8rem;">👔 Placement Officer</h2>
            <p style="font-size: 1.1rem; margin-bottom: 2rem;">
                Upload job descriptions and evaluate resumes at scale
            </p>
            <ul style="text-align: left; margin-bottom: 2rem;">
                <li>📄 Upload job descriptions</li>
                <li>🔍 Search & filter resumes by job role, score, location</li>
                <li>📊 View evaluation results and rankings</li>
                <li>📈 Access analytics and insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Access Dashboard", key="placement_btn", type="primary", use_container_width=True):
            st.session_state.user_role = 'placement_officer'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 2rem;
        ">
            <h2 style="margin-top: 0; font-size: 1.8rem;">🎓 Student</h2>
            <p style="font-size: 1.1rem; margin-bottom: 2rem;">
                Upload your resume and get instant evaluation feedback
            </p>
            <ul style="text-align: left; margin-bottom: 2rem;">
                <li>📋 Upload your resume</li>
                <li>🎯 Get relevance score (0-100)</li>
                <li>📊 Receive verdict (High/Medium/Low)</li>
                <li>💡 Get improvement suggestions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📝 Start Application", key="student_btn", type="primary", use_container_width=True):
            st.session_state.user_role = 'student'
            st.rerun()
    
    # Add footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; background-color: #f8f9fa; border-radius: 10px;">
        <h3 style="color: #333;">🤖 Powered by AI</h3>
        <p style="color: #666;">
            Combines rule-based checks with LLM-powered semantic understanding for accurate resume evaluation
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_placement_officer_interface():
    """Show placement officer interface"""
    # Header with role indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">👔 Placement Officer Dashboard</h1>', unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📄 Upload Job Description", "🔍 Search & Filter Resumes"])
    
    with tab1:
        show_placement_overview()
    
    with tab2:
        show_placement_upload_jd()
    
    with tab3:
        show_placement_search_resumes()

def show_student_interface():
    """Show student interface"""
    # Header with role indicator
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">🎓 Student Application Portal</h1>', unsafe_allow_html=True)
    
    # Student workflow
    show_student_workflow()

def show_placement_overview():
    """Show placement officer overview dashboard"""
    st.header("📊 System Overview")
    st.info("🎯 **Placement Officer Dashboard** - Upload job descriptions and evaluate resumes at scale with AI-powered analysis.")
    
    # Get dashboard statistics
    stats = make_api_request("/dashboard/stats")
    
    if stats:
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Resumes",
                value=stats["total_resumes"],
                delta=None
            )
        
        with col2:
            st.metric(
                label="Job Descriptions",
                value=stats["total_job_descriptions"],
                delta=None
            )
        
        with col3:
            st.metric(
                label="Total Evaluations",
                value=stats["total_evaluations"],
                delta=None
            )
        
        with col4:
            avg_score = stats["average_scores"]["relevance_score"]
            st.metric(
                label="Avg Relevance Score",
                value=f"{avg_score:.1f}%",
                delta=None
            )
        
        # Verdict distribution chart
        st.subheader("📊 Evaluation Verdict Distribution")
        verdict_data = stats["verdict_distribution"]
        
        if verdict_data:
            # Create pie chart
            fig = px.pie(
                values=list(verdict_data.values()),
                names=list(verdict_data.keys()),
                title="Distribution of Evaluation Verdicts",
                color_discrete_map={
                    "High": "#28a745",
                    "Medium": "#ffc107", 
                    "Low": "#dc3545"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No evaluation data available yet.")
    
    else:
        st.error("Could not load dashboard statistics.")

def show_placement_upload_jd():
    """Show placement officer job description upload"""
    st.header("📄 Upload Job Description")
    st.info("💡 **Fully Automated**: Just upload the job description file - all requirements will be extracted automatically!")
    
    with st.form("placement_upload_jd_form"):
        # File upload
        jd_file = st.file_uploader(
            "Choose a job description file (PDF/DOCX/TXT)",
            type=['pdf', 'docx', 'doc', 'txt'],
            key="placement_jd_file",
            help="The system will automatically extract job title, company, skills, and requirements"
        )
        
        # Submit button
        submitted = st.form_submit_button("🚀 Upload & Auto-Parse Job Description", type="primary")
        
        if submitted and jd_file:
            # Prepare form data - no manual input needed
            form_data = {
                "title": "",  # Will be extracted automatically
                "company": "",  # Will be extracted automatically
                "location": ""  # Will be extracted automatically
            }
            
            files = {"file": (jd_file.name, jd_file.getvalue(), jd_file.type)}
            
            # Make API request
            with st.spinner("🤖 Automatically extracting job requirements..."):
                result = make_api_request("/upload/job-description", "POST", form_data, files)
            
            if result:
                st.success("✅ Job description uploaded and parsed successfully!")
                
                # Show extracted information in a clean format
                if "parsed_data" in result:
                    parsed = result["parsed_data"]
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Job Title", parsed.get("job_title", "Not detected"))
                        st.metric("Company", parsed.get("company_info", {}).get("name", "Not detected"))
                    with col2:
                        st.metric("Location", parsed.get("company_info", {}).get("location", "Not detected"))
                        st.metric("Required Skills", len(parsed.get("required_skills", [])))
                    
                    # Show extracted skills
                    if parsed.get("required_skills"):
                        st.subheader("🎯 Extracted Required Skills")
                        skills_text = ", ".join(parsed["required_skills"][:10])  # Show first 10
                        if len(parsed["required_skills"]) > 10:
                            skills_text += f" ... and {len(parsed['required_skills']) - 10} more"
                        st.write(skills_text)

def show_placement_search_resumes():
    """Show placement officer resume search and filter"""
    st.header("🔍 Search & Filter Resumes")
    st.info("🔍 **Search and Filter**: Find matching resumes by job role, score, and location.")
    
    # Get job descriptions for filtering
    jds_response = make_api_request("/job-descriptions")
    jds = jds_response.get("job_descriptions", []) if jds_response else []
    
    if not jds:
        st.warning("⚠️ No job descriptions found. Please upload a job description first.")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        jd_filter = st.selectbox(
            "Filter by Job Description",
            ["All"] + [f"{jd['title']} - {jd['company']}" for jd in jds],
            key="placement_jd_filter"
        )
    
    with col2:
        verdict_filter = st.selectbox(
            "Filter by Verdict",
            ["All", "High", "Medium", "Low"],
            key="placement_verdict_filter"
        )
    
    with col3:
        min_score = st.slider(
            "Minimum Score",
            min_value=0,
            max_value=100,
            value=0,
            key="placement_min_score"
        )
    
    # Get results
    params = {}
    if jd_filter != "All":
        jd_id = jds[jd_filter.split(" - ")[0] == [jd['title'] for jd in jds].index(jd_filter.split(" - ")[0])]["id"]
        params["job_description_id"] = jd_id
    
    if verdict_filter != "All":
        params["verdict"] = verdict_filter
    
    if min_score > 0:
        params["min_score"] = min_score
    
    # Build query string
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    endpoint = f"/results?{query_string}" if query_string else "/results"
    
    results_response = make_api_request(endpoint)
    
    if results_response and results_response.get("results"):
        results = results_response["results"]
        
        # Display results in a table
        st.subheader(f"📋 Matching Resumes ({len(results)} found)")
        
        # Create DataFrame
        df = pd.DataFrame(results)
        
        # Format the DataFrame for display
        display_df = df[["student_name", "job_title", "company", "relevance_score", "verdict", "evaluation_date"]].copy()
        display_df.columns = ["Student", "Job Title", "Company", "Score", "Verdict", "Date"]
        display_df["Score"] = display_df["Score"].astype(str) + "%"
        
        # Color code verdicts
        def color_verdict(val):
            if val == "High":
                return "background-color: #d4edda; color: #155724"
            elif val == "Medium":
                return "background-color: #fff3cd; color: #856404"
            elif val == "Low":
                return "background-color: #f8d7da; color: #721c24"
            return ""
        
        styled_df = display_df.style.applymap(color_verdict, subset=["Verdict"])
        st.dataframe(styled_df, use_container_width=True)
        
        # Download results
        if st.button("📥 Download Results as CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV",
                data=csv,
                file_name="placement_resume_results.csv",
                mime="text/csv"
            )
    
    else:
        st.info("No matching resumes found. Try adjusting your filters.")

def show_student_workflow():
    """Show student workflow - Apply for jobs using resume"""
    st.header("📝 Apply for Jobs")
    st.info("🎓 **Apply for Jobs**: Upload your resume and apply for available job positions. Get instant evaluation feedback!")
    
    # Step 1: Upload Resume (if not already uploaded)
    if 'student_resume_id' not in st.session_state:
        st.subheader("📋 Step 1: Upload Your Resume")
        
        with st.form("student_upload_form"):
            # File upload
            resume_file = st.file_uploader(
                "Choose your resume file (PDF/DOCX)",
                type=['pdf', 'docx', 'doc'],
                key="student_resume_file",
                help="The system will automatically extract your name, contact info, skills, and experience"
            )
            
            # Submit button
            submitted = st.form_submit_button("🚀 Upload Resume", type="primary")
            
            if submitted and resume_file:
                # Prepare form data - no manual input needed
                form_data = {
                    "student_name": "",  # Will be extracted automatically
                    "student_email": ""  # Will be extracted automatically
                }
                
                files = {"file": (resume_file.name, resume_file.getvalue(), resume_file.type)}
                
                # Make API request
                with st.spinner("🤖 Automatically extracting resume information..."):
                    result = make_api_request("/upload/resume", "POST", form_data, files)
                
                if result:
                    st.success("✅ Resume uploaded successfully!")
                    
                    # Show extracted information briefly
                    if "parsed_data" in result:
                        parsed = result["parsed_data"]
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Student Name", parsed.get("contact_info", {}).get("name", "Not detected"))
                            st.metric("Email", parsed.get("contact_info", {}).get("email", "Not detected"))
                        with col2:
                            st.metric("Skills Found", len(parsed.get("skills", [])))
                            st.metric("Experience Entries", len(parsed.get("experience", [])))
                    
                    # Store resume ID for job applications
                    st.session_state.student_resume_id = result.get("resume_id")
                    st.rerun()
    else:
        st.success("✅ Resume uploaded! Ready to apply for jobs.")
    
    # Step 2: Browse and Apply for Jobs
    if 'student_resume_id' in st.session_state:
        st.subheader("🎯 Step 2: Browse Available Jobs")
        
        # Debug info (can be removed later)
        with st.expander("🔧 Debug Info", expanded=False):
            st.write(f"Resume ID: {st.session_state.student_resume_id}")
            st.write(f"Session state keys: {list(st.session_state.keys())}")
        
        # Get job descriptions
        jds_response = make_api_request("/job-descriptions")
        jds = jds_response.get("job_descriptions", []) if jds_response else []
        
        if jds:
            st.write(f"**Found {len(jds)} available job positions:**")
            
            # Display jobs in cards
            for i, jd in enumerate(jds):
                with st.expander(f"📋 {jd['title']} - {jd['company']}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Company:** {jd['company']}")
                        st.write(f"**Location:** {jd.get('location', 'Not specified')}")
                        st.write(f"**Posted:** {jd.get('created_at', 'Recently')}")
                        
                        # Show job description preview
                        if jd.get('description'):
                            description_preview = jd['description'][:200] + "..." if len(jd['description']) > 200 else jd['description']
                            st.write(f"**Description:** {description_preview}")
                    
                    with col2:
                        # Apply button for this job
                        if st.button(f"🎯 Apply for this Job", key=f"apply_{jd['id']}", type="primary"):
                            # Check if resume is uploaded
                            if 'student_resume_id' not in st.session_state:
                                st.error("❌ Please upload your resume first before applying for jobs.")
                                return
                            
                            # Make evaluation request
                            form_data = {
                                "resume_id": st.session_state.student_resume_id,
                                "job_description_id": jd['id']
                            }
                            
                            # Debug info
                            st.write(f"🔧 Debug: Sending resume_id={form_data['resume_id']}, job_description_id={form_data['job_description_id']}")
                            
                            with st.spinner("🤖 Evaluating your application..."):
                                result = make_api_request("/evaluate", "POST", form_data)
                            
                            if result and "analysis" in result:
                                analysis = result["analysis"]
                                
                                # Show application results
                                st.success("🎉 Application submitted successfully!")
                                
                                # Score and verdict
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Relevance Score", f"{analysis['relevance_score']}/100")
                                with col2:
                                    verdict_color = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}
                                    st.metric("Verdict", f"{verdict_color.get(analysis['verdict'], '⚪')} {analysis['verdict']}")
                                with col3:
                                    st.metric("Match Quality", f"{analysis['score_breakdown']['hard_match_score']:.1f}/10")
                                
                                # Missing elements
                                st.subheader("🎯 Gap Analysis")
                                missing = analysis.get("missing_elements", {})
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if missing.get("skills"):
                                        st.write("**Missing Skills:**")
                                        for skill in missing["skills"][:5]:  # Show top 5
                                            st.write(f"• {skill}")
                                    else:
                                        st.write("✅ **No missing skills identified**")
                                
                                with col2:
                                    if missing.get("certifications"):
                                        st.write("**Missing Certifications:**")
                                        for cert in missing["certifications"][:3]:  # Show top 3
                                            st.write(f"• {cert}")
                                    else:
                                        st.write("✅ **No missing certifications identified**")
                                
                                # Improvement suggestions
                                st.subheader("💡 Personalized Improvement Suggestions")
                                suggestions = analysis.get("improvement_suggestions", [])
                                if suggestions:
                                    for suggestion in suggestions:
                                        st.write(f"• {suggestion}")
                                else:
                                    st.write("No specific suggestions available.")
                                
                                # Strengths
                                strengths = analysis.get("strengths", [])
                                if strengths:
                                    st.subheader("💪 Your Key Strengths")
                                    for strength in strengths[:3]:  # Show top 3
                                        st.write(f"• {strength}")
                                
                                # Download results
                                st.subheader("📥 Download Application Report")
                                if st.button("📊 Download Report", key=f"download_{jd['id']}"):
                                    # Create report data
                                    report_data = {
                                        "Job Title": jd['title'],
                                        "Company": jd['company'],
                                        "Student Name": analysis.get("student_name", "Unknown"),
                                        "Relevance Score": analysis["relevance_score"],
                                        "Verdict": analysis["verdict"],
                                        "Missing Skills": "; ".join(missing.get("skills", [])[:5]),
                                        "Missing Certifications": "; ".join(missing.get("certifications", [])[:3]),
                                        "Improvement Suggestions": "; ".join(suggestions[:3])
                                    }
                                    
                                    import pandas as pd
                                    df = pd.DataFrame([report_data])
                                    csv = df.to_csv(index=False)
                                    
                                    st.download_button(
                                        label="📥 Download Report",
                                        data=csv,
                                        file_name=f"application_report_{jd['title'].replace(' ', '_')}.csv",
                                        mime="text/csv"
                                    )
                            else:
                                st.error("❌ Failed to evaluate application. Please try again.")
        else:
            st.warning("⚠️ No job positions available at the moment. Please check back later.")

def show_dashboard():
    """Show main dashboard with statistics and charts"""
    st.header("📈 System Overview")
    st.info("🎯 **Automated Resume Evaluation System** - Automatically evaluates resumes against job requirements, generates relevance scores (0-100), identifies gaps, and provides personalized feedback.")
    
    # Get dashboard statistics
    stats = make_api_request("/dashboard/stats")
    
    if stats:
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Resumes",
                value=stats["total_resumes"],
                delta=None
            )
        
        with col2:
            st.metric(
                label="Job Descriptions",
                value=stats["total_job_descriptions"],
                delta=None
            )
        
        with col3:
            st.metric(
                label="Total Evaluations",
                value=stats["total_evaluations"],
                delta=None
            )
        
        with col4:
            avg_score = stats["average_scores"]["relevance_score"]
            st.metric(
                label="Avg Relevance Score",
                value=f"{avg_score:.1f}%",
                delta=None
            )
        
        # Verdict distribution chart
        st.subheader("📊 Evaluation Verdict Distribution")
        verdict_data = stats["verdict_distribution"]
        
        if verdict_data:
            # Create pie chart
            fig = px.pie(
                values=list(verdict_data.values()),
                names=list(verdict_data.keys()),
                title="Distribution of Evaluation Verdicts",
                color_discrete_map={
                    "High": "#28a745",
                    "Medium": "#ffc107", 
                    "Low": "#dc3545"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No evaluation data available yet.")
        
        # Score distribution
        st.subheader("📈 Score Distribution")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Avg Hard Match Score",
                value=f"{stats['average_scores']['hard_match_score']:.2f}",
                delta=None
            )
        
        with col2:
            st.metric(
                label="Avg Semantic Match Score",
                value=f"{stats['average_scores']['semantic_match_score']:.2f}",
                delta=None
            )
    
    else:
        st.error("Could not load dashboard statistics.")

def show_upload_page():
    """Show file upload page - Fully automated"""
    st.header("📤 Upload Files")
    st.info("💡 **Fully Automated**: Just upload files - all information will be extracted automatically!")
    
    # Create tabs for different upload types
    tab1, tab2 = st.tabs(["📄 Upload Job Description", "📋 Upload Resume"])
    
    with tab1:
        st.subheader("Upload Job Description")
        st.write("**For Placement Team**: Upload job description and the system will automatically extract all requirements.")
        
        with st.form("upload_jd_form"):
            # File upload
            jd_file = st.file_uploader(
                "Choose a job description file (PDF/DOCX/TXT)",
                type=['pdf', 'docx', 'doc', 'txt'],
                key="jd_file",
                help="The system will automatically extract job title, company, skills, and requirements"
            )
            
            # Submit button
            submitted = st.form_submit_button("🚀 Upload & Auto-Parse Job Description")
            
            if submitted and jd_file:
                # Prepare form data - no manual input needed
                form_data = {
                    "title": "",  # Will be extracted automatically
                    "company": "",  # Will be extracted automatically
                    "location": ""  # Will be extracted automatically
                }
                
                files = {"file": (jd_file.name, jd_file.getvalue(), jd_file.type)}
                
                # Make API request
                with st.spinner("🤖 Automatically extracting job requirements..."):
                    result = make_api_request("/upload/job-description", "POST", form_data, files)
                
                if result:
                    st.success("✅ Job description uploaded and parsed successfully!")
                    
                    # Show extracted information in a clean format
                    if "parsed_data" in result:
                        parsed = result["parsed_data"]
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Job Title", parsed.get("job_title", "Not detected"))
                            st.metric("Company", parsed.get("company_info", {}).get("name", "Not detected"))
                        with col2:
                            st.metric("Location", parsed.get("company_info", {}).get("location", "Not detected"))
                            st.metric("Required Skills", len(parsed.get("required_skills", [])))
                        
                        # Show extracted skills
                        if parsed.get("required_skills"):
                            st.subheader("🎯 Extracted Required Skills")
                            skills_text = ", ".join(parsed["required_skills"][:10])  # Show first 10
                            if len(parsed["required_skills"]) > 10:
                                skills_text += f" ... and {len(parsed['required_skills']) - 10} more"
                            st.write(skills_text)
    
    with tab2:
        st.subheader("Upload Resume")
        st.write("**For Students**: Upload your resume and the system will automatically extract all information.")
        
        with st.form("upload_resume_form"):
            # File upload
            resume_file = st.file_uploader(
                "Choose a resume file (PDF/DOCX)",
                type=['pdf', 'docx', 'doc'],
                key="resume_file",
                help="The system will automatically extract your name, contact info, skills, and experience"
            )
            
            # Submit button
            submitted = st.form_submit_button("🚀 Upload & Auto-Parse Resume")
            
            if submitted and resume_file:
                # Prepare form data - no manual input needed
                form_data = {
                    "student_name": "",  # Will be extracted automatically
                    "student_email": ""  # Will be extracted automatically
                }
                
                files = {"file": (resume_file.name, resume_file.getvalue(), resume_file.type)}
                
                # Make API request
                with st.spinner("🤖 Automatically extracting resume information..."):
                    result = make_api_request("/upload/resume", "POST", form_data, files)
                
                if result:
                    st.success("✅ Resume uploaded and parsed successfully!")
                    
                    # Show extracted information in a clean format
                    if "parsed_data" in result:
                        parsed = result["parsed_data"]
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Student Name", parsed.get("contact_info", {}).get("name", "Not detected"))
                            st.metric("Email", parsed.get("contact_info", {}).get("email", "Not detected"))
                        with col2:
                            st.metric("Skills Found", len(parsed.get("skills", [])))
                            st.metric("Experience Entries", len(parsed.get("experience", [])))
                        
                        # Show extracted skills
                        if parsed.get("skills"):
                            st.subheader("🛠️ Extracted Skills")
                            skills_text = ", ".join(parsed["skills"][:10])  # Show first 10
                            if len(parsed["skills"]) > 10:
                                skills_text += f" ... and {len(parsed['skills']) - 10} more"
                            st.write(skills_text)

def show_evaluation_page():
    """Show evaluation page - matches exact workflow"""
    st.header("🎯 Evaluate Resumes")
    st.info("**Automated Evaluation**: Select a job description and resumes to evaluate. The system will automatically generate relevance scores, verdicts, and improvement suggestions.")
    
    # Get job descriptions and resumes
    jds_response = make_api_request("/job-descriptions")
    resumes_response = make_api_request("/resumes")
    
    if not jds_response or not resumes_response:
        st.error("Could not load data. Please upload job descriptions and resumes first.")
        return
    
    jds = jds_response.get("job_descriptions", [])
    resumes = resumes_response.get("resumes", [])
    
    if not jds:
        st.warning("⚠️ No job descriptions found. Please upload a job description first.")
        return
    
    if not resumes:
        st.warning("⚠️ No resumes found. Please upload resumes first.")
        return
    
    # Step 1: Select Job Description
    st.subheader("📄 Step 1: Select Job Description")
    jd_options = [f"{jd['title']} - {jd['company']} (ID: {jd['id']})" for jd in jds]
    selected_jd = st.selectbox("Choose a job description to evaluate against:", jd_options)
    
    if selected_jd:
        jd_id = int(selected_jd.split("ID: ")[1].split(")")[0])
        selected_jd_data = next(jd for jd in jds if jd['id'] == jd_id)
        
        # Show job description details
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Job Title", selected_jd_data['title'])
        with col2:
            st.metric("Company", selected_jd_data['company'])
        with col3:
            st.metric("Location", selected_jd_data['location'])
        
        # Step 2: Select Resumes to Evaluate
        st.subheader("📋 Step 2: Select Resumes to Evaluate")
        
        # Multi-select for resumes
        resume_options = [f"{resume['student_name']} - {resume['filename']} (ID: {resume['id']})" for resume in resumes]
        selected_resumes = st.multiselect(
            "Choose resumes to evaluate (you can select multiple):",
            resume_options,
            help="Select one or more resumes to evaluate against the job description"
        )
        
        if selected_resumes:
            # Step 3: Run Evaluation
            st.subheader("🚀 Step 3: Run Automated Evaluation")
            
            if st.button("🎯 Start Evaluation", type="primary"):
                evaluation_results = []
                
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, selected_resume in enumerate(selected_resumes):
                    resume_id = int(selected_resume.split("ID: ")[1].split(")")[0])
                    resume_name = selected_resume.split(" - ")[0]
                    
                    status_text.text(f"Evaluating {resume_name}...")
                    
                    # Make evaluation request
                    form_data = {
                        "resume_id": resume_id,
                        "job_description_id": jd_id
                    }
                    
                    result = make_api_request("/evaluate", "POST", form_data)
                    
                    if result and "analysis" in result:
                        evaluation_results.append({
                            "resume_name": resume_name,
                            "resume_id": resume_id,
                            "analysis": result["analysis"]
                        })
                    
                    # Update progress
                    progress_bar.progress((i + 1) / len(selected_resumes))
                
                status_text.text("✅ Evaluation completed!")
                
                # Step 4: Show Results
                if evaluation_results:
                    st.subheader("📊 Step 4: Evaluation Results")
                    
                    # Sort by relevance score
                    evaluation_results.sort(key=lambda x: x["analysis"]["relevance_score"], reverse=True)
                    
                    # Show summary
                    st.success(f"✅ Successfully evaluated {len(evaluation_results)} resumes!")
                    
                    # Display results
                    for i, result in enumerate(evaluation_results):
                        analysis = result["analysis"]
                        
                        # Create expandable section for each result
                        with st.expander(f"#{i+1} {result['resume_name']} - Score: {analysis['relevance_score']}/100 - {analysis['verdict']} Fit", expanded=(i==0)):
                            
                            # Score and verdict
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Relevance Score", f"{analysis['relevance_score']}/100")
                            with col2:
                                verdict_color = {"High": "🟢", "Medium": "🟡", "Low": "🔴"}
                                st.metric("Verdict", f"{verdict_color.get(analysis['verdict'], '⚪')} {analysis['verdict']}")
                            with col3:
                                st.metric("Hard Match", f"{analysis['score_breakdown']['hard_match_score']:.2f}")
                            with col4:
                                st.metric("Semantic Match", f"{analysis['score_breakdown']['semantic_match_score']:.2f}")
                            
                            # Missing elements
                            st.subheader("🎯 Gap Analysis")
                            missing = analysis.get("missing_elements", {})
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if missing.get("skills"):
                                    st.write("**Missing Skills:**")
                                    for skill in missing["skills"][:5]:  # Show top 5
                                        st.write(f"• {skill}")
                                else:
                                    st.write("✅ **No missing skills identified**")
                            
                            with col2:
                                if missing.get("certifications"):
                                    st.write("**Missing Certifications:**")
                                    for cert in missing["certifications"][:3]:  # Show top 3
                                        st.write(f"• {cert}")
                                else:
                                    st.write("✅ **No missing certifications identified**")
                            
                            # Improvement suggestions
                            st.subheader("💡 Personalized Improvement Suggestions")
                            suggestions = analysis.get("improvement_suggestions", [])
                            if suggestions:
                                for suggestion in suggestions[:3]:  # Show top 3
                                    st.write(f"• {suggestion}")
                            else:
                                st.write("No specific suggestions available.")
                            
                            # Strengths
                            strengths = analysis.get("strengths", [])
                            if strengths:
                                st.subheader("💪 Key Strengths")
                                for strength in strengths[:3]:  # Show top 3
                                    st.write(f"• {strength}")
                    
                    # Download results
                    st.subheader("📥 Download Results")
                    if st.button("📊 Export Results to CSV"):
                        # Create CSV data
                        csv_data = []
                        for result in evaluation_results:
                            analysis = result["analysis"]
                            csv_data.append({
                                "Student Name": result["resume_name"],
                                "Relevance Score": analysis["relevance_score"],
                                "Verdict": analysis["verdict"],
                                "Missing Skills": "; ".join(analysis.get("missing_elements", {}).get("skills", [])[:5]),
                                "Improvement Suggestions": "; ".join(analysis.get("improvement_suggestions", [])[:3])
                            })
                        
                        import pandas as pd
                        df = pd.DataFrame(csv_data)
                        csv = df.to_csv(index=False)
                        
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"evaluation_results_{selected_jd_data['title'].replace(' ', '_')}.csv",
                            mime="text/csv"
                        )

def show_results_page():
    """Show evaluation results page"""
    st.header("📊 Evaluation Results")
    
    # Get job descriptions for filtering
    jds_response = make_api_request("/job-descriptions")
    jds = jds_response.get("job_descriptions", []) if jds_response else []
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        jd_filter = st.selectbox(
            "Filter by Job Description",
            ["All"] + [f"{jd['title']} - {jd['company']}" for jd in jds],
            key="jd_filter"
        )
    
    with col2:
        verdict_filter = st.selectbox(
            "Filter by Verdict",
            ["All", "High", "Medium", "Low"],
            key="verdict_filter"
        )
    
    with col3:
        min_score = st.slider(
            "Minimum Score",
            min_value=0,
            max_value=100,
            value=0,
            key="min_score"
        )
    
    # Get results
    params = {}
    if jd_filter != "All":
        jd_id = jds[jd_filter.split(" - ")[0] == [jd['title'] for jd in jds].index(jd_filter.split(" - ")[0])]["id"]
        params["job_description_id"] = jd_id
    
    if verdict_filter != "All":
        params["verdict"] = verdict_filter
    
    if min_score > 0:
        params["min_score"] = min_score
    
    # Build query string
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    endpoint = f"/results?{query_string}" if query_string else "/results"
    
    results_response = make_api_request(endpoint)
    
    if results_response and results_response.get("results"):
        results = results_response["results"]
        
        # Display results in a table
        st.subheader(f"📋 Results ({len(results)} found)")
        
        # Create DataFrame
        df = pd.DataFrame(results)
        
        # Format the DataFrame for display
        display_df = df[["student_name", "job_title", "company", "relevance_score", "verdict", "evaluation_date"]].copy()
        display_df.columns = ["Student", "Job Title", "Company", "Score", "Verdict", "Date"]
        display_df["Score"] = display_df["Score"].astype(str) + "%"
        
        # Color code verdicts
        def color_verdict(val):
            if val == "High":
                return "background-color: #d4edda; color: #155724"
            elif val == "Medium":
                return "background-color: #fff3cd; color: #856404"
            elif val == "Low":
                return "background-color: #f8d7da; color: #721c24"
            return ""
        
        styled_df = display_df.style.applymap(color_verdict, subset=["Verdict"])
        st.dataframe(styled_df, use_container_width=True)
        
        # Detailed view
        st.subheader("🔍 Detailed Analysis")
        
        selected_idx = st.selectbox(
            "Select a result to view details",
            range(len(results)),
            format_func=lambda x: f"{results[x]['student_name']} - {results[x]['job_title']} ({results[x]['relevance_score']}%)"
        )
        
        if selected_idx is not None:
            selected_result = results[selected_idx]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Relevance Score", f"{selected_result['relevance_score']}%")
                st.metric("Verdict", selected_result['verdict'])
                st.metric("Hard Match Score", f"{selected_result['hard_match_score']:.2f}")
                st.metric("Semantic Match Score", f"{selected_result['semantic_match_score']:.2f}")
            
            with col2:
                st.subheader("Missing Skills")
                missing_skills = selected_result.get("missing_skills", [])
                if missing_skills:
                    for skill in missing_skills[:5]:  # Show top 5
                        st.write(f"• {skill}")
                else:
                    st.write("No missing skills identified")
                
                st.subheader("Improvement Suggestions")
                suggestions = selected_result.get("improvement_suggestions", [])
                if suggestions:
                    for suggestion in suggestions[:3]:  # Show top 3
                        st.write(f"• {suggestion}")
                else:
                    st.write("No suggestions available")
    
    else:
        st.info("No evaluation results found. Upload some resumes and job descriptions to get started.")

def show_manage_page():
    """Show data management page"""
    st.header("🗂️ Data Management")
    
    # Create tabs
    tab1, tab2 = st.tabs(["📋 Resumes", "📄 Job Descriptions"])
    
    with tab1:
        st.subheader("Uploaded Resumes")
        
        resumes_response = make_api_request("/resumes")
        if resumes_response and resumes_response.get("resumes"):
            resumes = resumes_response["resumes"]
            
            # Create DataFrame
            df = pd.DataFrame(resumes)
            df["upload_date"] = pd.to_datetime(df["upload_date"]).dt.strftime("%Y-%m-%d %H:%M")
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Summary statistics
            st.subheader("📊 Resume Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Resumes", len(resumes))
            
            with col2:
                unique_skills = set()
                for resume in resumes:
                    unique_skills.update(resume.get("skills", []))
                st.metric("Unique Skills", len(unique_skills))
            
            with col3:
                recent_uploads = len([r for r in resumes if pd.to_datetime(r["upload_date"]) > datetime.now() - timedelta(days=7)])
                st.metric("Uploads (Last 7 days)", recent_uploads)
        
        else:
            st.info("No resumes uploaded yet.")
    
    with tab2:
        st.subheader("Uploaded Job Descriptions")
        
        jds_response = make_api_request("/job-descriptions")
        if jds_response and jds_response.get("job_descriptions"):
            jds = jds_response["job_descriptions"]
            
            # Create DataFrame
            df = pd.DataFrame(jds)
            df["upload_date"] = pd.to_datetime(df["upload_date"]).dt.strftime("%Y-%m-%d %H:%M")
            
            # Display table
            st.dataframe(df, use_container_width=True)
            
            # Summary statistics
            st.subheader("📊 Job Description Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Job Descriptions", len(jds))
            
            with col2:
                unique_companies = len(set(jd["company"] for jd in jds if jd["company"]))
                st.metric("Unique Companies", unique_companies)
            
            with col3:
                recent_uploads = len([jd for jd in jds if pd.to_datetime(jd["upload_date"]) > datetime.now() - timedelta(days=7)])
                st.metric("Uploads (Last 7 days)", recent_uploads)
        
        else:
            st.info("No job descriptions uploaded yet.")

if __name__ == "__main__":
    main()
