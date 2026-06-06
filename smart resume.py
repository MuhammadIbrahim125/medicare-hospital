import streamlit as st
import re
from datetime import datetime
import base64

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Resume Builder", 
    page_icon="📄", 
    layout="wide"
)

# ---------- CUSTOM CSS (Beautiful Interface) ----------
st.markdown("""
<style>
    /* Main header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
    }
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Score card */
    .score-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .score-bad {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    }
    .score-medium {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .score-good {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .score-number {
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
    }
    
    /* Tip box */
    .tip-box {
        background: #f0f2f6;
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    /* Preview card */
    .preview-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    .preview-name {
        color: #667eea;
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .preview-contact {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stTextArea > div > div > textarea {
        border-radius: 10px;
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        transition: 0.3s;
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 10px;
        font-weight: bold;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="main-header">
    <h1>📄 Smart Resume Builder</h1>
    <p>✨ Apna professional resume banayein aur ATS score check karein ✨</p>
</div>
""", unsafe_allow_html=True)

# ---------- TWO COLUMN LAYOUT ----------
col1, col2 = st.columns([1, 1], gap="large")

# ========== LEFT COLUMN - FORM ==========
with col1:
    st.markdown("### 📝 Resume Details")
    st.markdown("---")
    
    # Personal Information
    with st.expander("👤 Personal Information", expanded=True):
        full_name = st.text_input("Full Name *", placeholder="e.g., Ali Raza Khan", key="name")
        email = st.text_input("Email *", placeholder="ali@example.com", key="email")
        phone = st.text_input("Phone *", placeholder="+92 300 1234567", key="phone")
        location = st.text_input("Location", placeholder="Karachi, Pakistan", key="location")
        linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/aliraza", key="linkedin")
    
    # Professional Summary
    with st.expander("🎯 Professional Summary", expanded=True):
        summary = st.text_area(
            "Summary", 
            placeholder="Data Scientist with 3+ years of experience in Python, ML...\nProven track record of delivering impactful solutions...",
            height=120,
            key="summary"
        )
    
    # Skills
    with st.expander("⚙️ Skills", expanded=True):
        skills = st.text_area(
            "Technical Skills", 
            placeholder="Python, SQL, Machine Learning, Streamlit, Pandas, NumPy, Scikit-learn",
            height=80,
            key="skills"
        )
        soft_skills = st.text_input("Soft Skills", placeholder="Leadership, Communication, Problem Solving", key="soft")
    
    # Experience
    with st.expander("💼 Work Experience", expanded=True):
        experience = st.text_area(
            "Experience", 
            placeholder="Data Analyst | ABC Company | 2022-Present\n• Analyzed customer data to improve retention by 20%\n• Built interactive dashboards using Power BI\n• Automated reporting processes saving 10hrs/week",
            height=150,
            key="exp"
        )
    
    # Education
    with st.expander("🎓 Education", expanded=True):
        education = st.text_area(
            "Education", 
            placeholder="BS Computer Science | XYZ University | 2020-2024\nCGPA: 3.6/4.0\nRelevant Courses: Data Structures, Machine Learning",
            height=100,
            key="edu"
        )
    
    # Certifications
    with st.expander("🏅 Certifications", expanded=False):
        certs = st.text_area(
            "Certifications", 
            placeholder="• Google Data Analytics Professional Certificate\n• Machine Learning Specialization - Andrew Ng",
            height=80,
            key="certs"
        )

# ========== RIGHT COLUMN - ANALYSIS ==========
with col2:
    st.markdown("### 📊 Resume Analysis")
    st.markdown("---")
    
    # ATS Score Calculation
    if full_name and email and skills:
        score = 0
        feedback = []
        
        # Name check
        if full_name and len(full_name) > 3:
            score += 5
        else:
            feedback.append("❌ Complete name likhen")
        
        # Email check
        if email and "@" in email and "." in email:
            score += 10
        else:
            feedback.append("❌ Valid email dalen (example@domain.com)")
        
        # Phone check
        if phone and len(phone) >= 10:
            score += 5
        else:
            feedback.append("❌ Valid phone number dalen")
        
        # Skills check
        skills_list = [s.strip() for s in skills.split(",") if s.strip()]
        if len(skills_list) >= 6:
            score += 20
            feedback.append("✅ Excellent! 6+ skills")
        elif len(skills_list) >= 4:
            score += 15
            feedback.append("✅ Good! 4+ skills")
        elif len(skills_list) >= 2:
            score += 8
            feedback.append("⚠️ Add more skills (6+ recommended)")
        else:
            feedback.append("❌ Kam se kam 2 skills dalen")
        
        # Summary check
        if summary and len(summary) > 80:
            score += 15
            feedback.append("✅ Professional summary acha hai")
        elif summary and len(summary) > 40:
            score += 8
            feedback.append("⚠️ Summary thoda lamba likhen (80+ characters)")
        else:
            feedback.append("⚠️ Summary add karen")
        
        # Experience check
        if experience and len(experience) > 100:
            score += 20
            feedback.append("✅ Experience details impressive!")
        elif experience and len(experience) > 50:
            score += 12
            feedback.append("⚠️ Experience mein achievements add karen")
        else:
            feedback.append("❌ Experience add karen")
        
        # Education check
        if education and len(education) > 30:
            score += 15
            feedback.append("✅ Education details sahi hain")
        else:
            feedback.append("⚠️ Education complete karen")
        
        # LinkedIn (bonus)
        if linkedin and "linkedin.com" in linkedin:
            score += 5
            feedback.append("✅ LinkedIn profile added (+5 bonus)")
        
        # Certifications (bonus)
        if certs and len(certs) > 20:
            score += 5
            feedback.append("✅ Certifications added (+5 bonus)")
        
        # Cap score at 100
        score = min(score, 100)
        
        # Display Score Card
        if score >= 75:
            st.markdown(f"""
            <div class="score-card score-good">
                <p style="font-size:1.2rem; margin:0;">🎉 Outstanding! 🎉</p>
                <p class="score-number">{score} / 100</p>
                <p>⭐ ATS Score: Excellent! Your resume is ready ⭐</p>
            </div>
            """, unsafe_allow_html=True)
            show_balloons = True
        elif score >= 50:
            st.markdown(f"""
            <div class="score-card score-medium">
                <p style="font-size:1.2rem; margin:0;">📈 Good Progress!</p>
                <p class="score-number">{score} / 100</p>
                <p>⚡ ATS Score: Good, but can improve ⚡</p>
            </div>
            """, unsafe_allow_html=True)
            show_balloons = False
        else:
            st.markdown(f"""
            <div class="score-card score-bad">
                <p style="font-size:1.2rem; margin:0;">⚠️ Needs Improvement</p>
                <p class="score-number">{score} / 100</p>
                <p>💪 Follow the tips below to improve your score 💪</p>
            </div>
            """, unsafe_allow_html=True)
            show_balloons = False
        
        # Balloons for good score
        if score >= 75:
            st.balloons()
        
        # Progress bar
        st.progress(score / 100)
        
        # Improvement Tips
        st.markdown("### 💡 Improvement Tips")
        for tip in feedback[:6]:
            st.markdown(f"<div class='tip-box'>{tip}</div>", unsafe_allow_html=True)
        
        # Keyword Suggestions
        st.markdown("### 🔑 Hot Keywords for Your Resume")
        keyword_categories = {
            "Tech": ["Python", "SQL", "Machine Learning", "Data Analysis", "Cloud Computing"],
            "Soft": ["Leadership", "Team Player", "Communication", "Problem Solving"],
            "Action": ["Achieved", "Improved", "Developed", "Implemented", "Managed"]
        }
        
        selected_keywords = []
        cols = st.columns(3)
        for i, (cat, keys) in enumerate(keyword_categories.items()):
            with cols[i]:
                st.markdown(f"**{cat}**")
                for kw in keys[:4]:
                    if st.checkbox(kw, key=f"kw_{kw}"):
                        selected_keywords.append(kw)
        
        if selected_keywords:
            st.success(f"✅ Added to your resume: {', '.join(selected_keywords[:5])}")
    
    else:
        st.info("👈 **Left side mein details fill karen**\n\nName, email aur skills likhna zaroori hai!")
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)

# ========== RESUME PREVIEW SECTION ==========
st.markdown("---")
st.markdown("### 📄 Resume Preview")

if full_name:
    # Create preview HTML
    preview_html = f"""
    <div class="preview-card">
        <div class="preview-name">{full_name.upper()}</div>
        <div class="preview-contact">
            📧 {email if email else 'Not provided'} | 📞 {phone if phone else 'Not provided'} | 📍 {location if location else 'Not provided'}
            {f'<br>🔗 {linkedin}' if linkedin else ''}
        </div>
        <hr>
        <div>
            <strong>🎯 Professional Summary</strong><br>
            <p style="color:#555;">{summary if summary else '— Not added —'}</p>
        </div>
        <div style="margin-top:1rem;">
            <strong>⚙️ Technical Skills</strong><br>
            <p style="color:#555;">{skills if skills else '— Not added —'}</p>
        </div>
        {f'<div style="margin-top:1rem;"><strong>💼 Soft Skills</strong><br><p style="color:#555;">{soft_skills}</p></div>' if soft_skills else ''}
        <div style="margin-top:1rem;">
            <strong>💼 Work Experience</strong><br>
            <p style="color:#555; white-space:pre-line;">{experience if experience else '— Not added —'}</p>
        </div>
        <div style="margin-top:1rem;">
            <strong>🎓 Education</strong><br>
            <p style="color:#555; white-space:pre-line;">{education if education else '— Not added —'}</p>
        </div>
        {f'<div style="margin-top:1rem;"><strong>🏅 Certifications</strong><br><p style="color:#555; white-space:pre-line;">{certs}</p></div>' if certs else ''}
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)
    
    # Download Buttons
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn1:
        if st.button("📥 Download as PDF", use_container_width=True):
            st.success("✅ Resume PDF ready! (Install wkhtmltopdf for actual PDF generation)")
            st.info("💡 Tip: Press Ctrl+P (Cmd+P on Mac) and 'Save as PDF'")
    
    with col_btn2:
        if st.button("📧 Send to Email", use_container_width=True):
            st.info("📧 Email feature coming soon! API integration needed.")
    
    with col_btn3:
        if st.button("🖨️ Print Resume", use_container_width=True):
            st.info("🖨️ Press Ctrl+P to print or save as PDF")
    
    # Share option
    st.caption("💡 **Pro Tip:** Resume ko copy karo aur LinkedIn profile mein update karo!")
    
else:
    st.warning("⚠️ **Pehle apna naam likhen** upar left side mein!")

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p>✨ <strong>Smart Resume Builder</strong> | Get Hired Faster with ATS-Optimized Resume ✨</p>
    <p style="font-size: 0.8rem;">© 2025 | Made with ❤️ for Job Seekers</p>
</div>
""", unsafe_allow_html=True)