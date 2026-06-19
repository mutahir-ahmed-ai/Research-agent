import streamlit as st
import os
import sys
from io import StringIO
from agent.research_agent import create_research_agent

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 AI Research Agent")
st.markdown("Enter a research topic and the agent will search the web and generate a PDF report.")

topic = st.text_input(
    "Research Topic",
    placeholder="e.g. Latest trends in NLP and LLMs 2026"
)

if st.button("Generate Research Report", type="primary"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        st.info("Agent is working... this may take 30–60 seconds.")

        log_output = StringIO()
        
        with st.spinner("Researching and generating your PDF report..."):
            try:
                agent = create_research_agent()

                old_stdout = sys.stdout
                sys.stdout = log_output

                result = agent.invoke({
                    "input": f"""Research the following topic thoroughly and generate a PDF report.
                    
Topic: {topic}

Instructions:
- Search the web at least 2-3 times with different queries to gather comprehensive information
- After gathering enough information, create a well-structured report with this exact format:
# {topic}

## Executive Summary
(2-3 sentence overview)

## Key Findings
- Finding 1
- Finding 2  
- Finding 3
- Finding 4
- Finding 5

## Conclusion
(2-3 sentence conclusion)

- Then call generate_pdf_report with the complete formatted content above"""
                })

                sys.stdout = old_stdout
                agent_log = log_output.getvalue()

                with st.expander("🧠 Agent Reasoning Steps", expanded=False):
                    st.text(agent_log)

                pdf_path = "/tmp/research_report.pdf"
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()

                    st.success("✅ Research report generated successfully!")

                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_bytes,
                        file_name=f"{topic[:40].replace(' ', '_')}_report.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("PDF was not generated. Check agent reasoning steps above.")
                    sys.stdout = old_stdout

            except Exception as e:
                sys.stdout = old_stdout
                st.error(f"Agent error: {str(e)}")
                with st.expander("Error Details"):
                    st.text(log_output.getvalue())
