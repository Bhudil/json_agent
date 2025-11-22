import streamlit as st
import os
import json
from datetime import datetime
import pdfplumber
from groq import Groq

st.set_page_config(page_title="Universal Credit Act Analyzer", layout="wide")

GROQ_API_KEY = "GROQ_API_KEY"

@st.cache_resource
def get_groq_client():
    return Groq(api_key=GROQ_API_KEY)

def extract_pdf_text(pdf_file):
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting PDF: {str(e)}")
        return None

def analyze_document(text):
    client = get_groq_client()
    
    analysis_prompt = f"""Analyze the following legislative document and provide structured output.

DOCUMENT TEXT:
{text}

Provide output in this JSON format only:
{{
  "summary": ["bullet1", "bullet2", "bullet3", "bullet4", "bullet5"],
  "sections": {{
    "definitions": "text",
    "obligations": "text",
    "responsibilities": "text",
    "eligibility": "text",
    "payments": "text",
    "penalties": "text",
    "record_keeping": "text"
  }},
  "rule_checks": [
    {{"rule": "Act must define key terms", "status": "pass", "evidence": "text", "confidence": 85}},
    {{"rule": "Act must specify eligibility criteria", "status": "pass", "evidence": "text", "confidence": 90}},
    {{"rule": "Act must specify responsibilities of the administering authority", "status": "pass", "evidence": "text", "confidence": 88}},
    {{"rule": "Act must include enforcement or penalties", "status": "pass", "evidence": "text", "confidence": 92}},
    {{"rule": "Act must include payment calculation or entitlement structure", "status": "pass", "evidence": "text", "confidence": 87}},
    {{"rule": "Act must include record-keeping or reporting requirements", "status": "pass", "evidence": "text", "confidence": 89}}
  ]
}}

Return ONLY the JSON object, nothing else."""

    try:
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": analysis_prompt}
            ]
        )
        response_text = message.choices[0].message.content
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            result = json.loads(json_str)
            return result
        except json.JSONDecodeError:
            st.error("Failed to parse response as JSON")
            return None
            
    except Exception as e:
        st.error(f"Error analyzing document: {str(e)}")
        return None

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

with st.sidebar:
    st.title("Configuration")
    
    uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])
    
    if uploaded_file:
        st.session_state.pdf_name = uploaded_file.name
        st.success(f"Loaded: {uploaded_file.name}")
        
        if st.button("Analyze Document", type="primary", use_container_width=True):
            with st.spinner("Extracting PDF..."):
                pdf_text = extract_pdf_text(uploaded_file)
            
            if pdf_text:
                st.info(f"Extracted {len(pdf_text)} characters")
                
                with st.spinner("Analyzing with Groq..."):
                    result = analyze_document(pdf_text)
                
                if result:
                    st.session_state.analysis_result = result
                    st.success("Analysis Complete!")
    
    st.divider()
    
    if st.session_state.analysis_result:
        json_str = json.dumps(st.session_state.analysis_result, indent=2)
        st.download_button(
            label="Download JSON Report",
            data=json_str,
            file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
        
        if st.button("Clear Analysis", use_container_width=True):
            st.session_state.analysis_result = None
            st.session_state.pdf_name = None
            st.rerun()

st.title("Universal Credit Act Analyzer")

if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    st.subheader("Summary")
    for i, point in enumerate(result.get("summary", []), 1):
        st.write(f"{i}. {point}")
    
    st.divider()
    
    st.subheader("Key Legislative Sections")
    
    sections = result.get("sections", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Definitions**")
        st.write(sections.get("definitions", "N/A"))
        
        st.write("**Obligations**")
        st.write(sections.get("obligations", "N/A"))
        
        st.write("**Eligibility**")
        st.write(sections.get("eligibility", "N/A"))
    
    with col2:
        st.write("**Responsibilities**")
        st.write(sections.get("responsibilities", "N/A"))
        
        st.write("**Payments/Entitlements**")
        st.write(sections.get("payments", "N/A"))
        
        st.write("**Record-Keeping**")
        st.write(sections.get("record_keeping", "N/A"))
    
    st.divider()
    
    st.subheader("Rule Compliance Check")
    
    rules = result.get("rule_checks", [])
    
    for rule in rules:
        status = rule.get("status", "").upper()
        confidence = rule.get("confidence", 0)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.write(status)
        
        with col2:
            st.write(f"**{rule.get('rule', 'N/A')}**")
            st.caption(f"Evidence: {rule.get('evidence', 'N/A')}")
        
        with col3:
            st.metric("Confidence", f"{confidence}%")
    
    passed = sum(1 for r in rules if r.get("status") == "pass")
    st.write(f"**Overall: {passed}/{len(rules)} Rules Passed**")
    
    st.divider()
    
    with st.expander("Full JSON Report"):
        st.json(result)

else:
    st.info("Upload a PDF document from the sidebar to begin analysis")