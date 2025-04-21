import streamlit as st
import sys
import os

# Add the Project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from debugger.implementation import CDebugger

# Initialize session state
if 'debugger' not in st.session_state:
    st.session_state.debugger = CDebugger("debugger")
    st.session_state.version_history = []
    st.session_state.last_analyzed_code = ""
    st.session_state.code_input = ""
    st.session_state.code_changed = False

st.set_page_config(page_title="C Debugger", layout="wide")

st.title("🔍 LLM-Powered C Debugger")
st.write("Paste C code below and get live diagnostics.")

# Reset button in sidebar
if st.sidebar.button("🔄 Reset Debugger", type="primary"):
    # Create a new debugger instance
    st.session_state.debugger = CDebugger("debugger")
    st.session_state.version_history = []
    st.session_state.last_analyzed_code = ""
    st.session_state.code_input = ""
    st.session_state.code_changed = False
    st.success("Debugger reset successfully. Previous code history cleared.")
    st.rerun()

# Text editor for C code
code_input = st.text_area("Your C Code", height=300, key="code_input")

# Update code_changed state
st.session_state.code_changed = st.session_state.code_input != st.session_state.last_analyzed_code

# Submit button
if st.button("Analyze", disabled=not st.session_state.code_changed):
    with st.spinner("Analyzing..."):
        # Run the debugger
        result = st.session_state.debugger.run("analyze_code", props={"code": code_input})
        
        # Update version history
        st.session_state.version_history.append({
            "code": code_input,
            "diagnostics": result,
            "version": len(st.session_state.version_history) + 1
        })
        
        # Update last analyzed code
        st.session_state.last_analyzed_code = code_input
        st.session_state.code_changed = False
        
        st.success("Analysis complete.")

# Display diagnostics
if st.session_state.version_history:
    latest = st.session_state.version_history[-1]
    st.subheader(f"🧠 Version {latest['version']} Diagnostics")
    st.code(latest["diagnostics"])

# Show version history
if st.session_state.version_history:
    st.sidebar.header("🗂️ Version History")
    for entry in reversed(st.session_state.version_history):
        if st.sidebar.button(f"View v{entry['version']}"):
            st.subheader(f"Version {entry['version']} Code")
            st.code(entry['code'], language='c')
            st.subheader(f"Diagnostics for v{entry['version']}")
            st.code(entry['diagnostics'])

