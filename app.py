import streamlit as st
import os
import sys
import fitz
from io import StringIO
from agent.research_agent import create_research_agent

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 AI Research Agent")
st.markdown("Enter a research topic and the agent will search the web and generate a PDF report.")

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
if "agent_log" not in st.session_state:
    st.session_state.agent_log = None
if "report_topic" not in st.session_state:
    st.session_state.report_topic = None
if "show_view" not in st.session_state:
    st.session_state.show_view = False

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
        old_stdout = sys.stdout

        with st.spinner("Researching and generating your PDF report..."):
            try:
                agent = create_research_agent()
                sys.stdout = log_output

                result = agent.invoke({
                    "input": f"""Research the following topic thoroughly and generate a PDF report.

Topic: {topic}

Instructions:
- Search the web at least 2-3 times with different queries to gather comprehensive information
- Keep track of the source URLs returned in each search result
- When selecting which sources to cite, prioritize authoritative sources: news outlets, government websites, official reports, and research papers
- Do NOT include social media links (YouTube, Instagram, Facebook, Twitter/X, TikTok, Reddit) in the Sources section, even if they appeared in search results
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

## Sources
- (list only the credible, non-social-media source URLs you used, one per line)

- Then call generate_pdf_report with the complete formatted content above, including the Sources section"""
                })

                sys.stdout = old_stdout
                agent_log = log_output.getvalue()

                pdf_path = "/tmp/research_report.pdf"
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()

                    st.session_state.pdf_bytes = pdf_bytes
                    st.session_state.agent_log = agent_log
                    st.session_state.report_topic = topic
                    st.session_state.show_view = False

                    st.success("✅ Research report generated successfully!")
                else:
                    st.error("PDF was not generated. Check the reasoning steps below.")
                    with st.expander("🧠 Agent Reasoning Steps", expanded=False):
                        st.text(agent_log)

            except Exception as e:
                sys.stdout = old_stdout
                st.error(f"Agent error: {str(e)}")
                with st.expander("Error Details"):
                    st.text(log_output.getvalue())

if st.session_state.pdf_bytes:
    st.divider()
    st.subheader(f"📄 Report: {st.session_state.report_topic}")

    with st.expander("🧠 Agent Reasoning Steps", expanded=False):
        st.text(st.session_state.agent_log)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👁️ View Report"):
            st.session_state.show_view = not st.session_state.show_view

    with col2:
        st.download_button(
            label="📥 Download PDF",
            data=st.session_state.pdf_bytes,
            file_name=f"{st.session_state.report_topic[:40].replace(' ', '_')}_report.pdf",
            mime="application/pdf"
        )

    if st.session_state.show_view:
        pdf_document = fitz.open(stream=st.session_state.pdf_bytes, filetype="pdf")
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            st.image(img_bytes, use_container_width=True)
        pdf_document.close()
