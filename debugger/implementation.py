import time
from motion import Component
import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key="ADD YOUR API KEY HERE")

CDebugger = Component("C-Debugger")

@CDebugger.init_state
def setup():
    return {
        "version_history": [],
        "current_code": "",
        "diagnostics": "No code submitted yet.",
        "is_reset": True  # Flag to indicate if debugger was reset
    }

@CDebugger.serve("analyze_code")
def analyze_code(state, props):
    current_code = props['code']
    
    # If reset or first run, don't reference previous code
    if state.get('is_reset', True):
        prompt = f"""You are a C debugging assistant.
        Here's the code to analyze:
        {current_code}

        Find potential bugs, undefined behavior, or crashes. Provide:
        - The bug
        - Explanation
        - Suggested fix
        """
    else:
        # Not reset, so we can reference previous code
        prompt = f"""You are a C debugging assistant.
        Here's the new code:
        {current_code}

        Here's the previous code:
        {state['current_code']}

        Find bugs, undefined behavior, or crashes introduced in the new version. Provide:
        - The bug
        - Explanation
        - Suggested fix
        """

    return llm(prompt)

def llm(prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

@CDebugger.update("analyze_code")
def update_history(state, props):
    new_version = {
        "code": props['code'],
        "diagnostics": props.serve_result
    }
    updated_history = state["version_history"] + [new_version]
    return {
        "version_history": updated_history,
        "current_code": props['code'],
        "diagnostics": props.serve_result,
        "is_reset": False  # Set to false after first analysis
    }
