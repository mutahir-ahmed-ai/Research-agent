**🔍 AI Research Agent**

An autonomous AI agent that researches any topic by searching the web, synthesizing findings, and generating a formatted downloadable PDF report — powered by the ReAct reasoning pattern.

**🚀 Live Demo**

What It Does

Type any research topic → the agent autonomously decides how many searches to run, synthesizes the results, and produces a structured PDF report with cited sources.

The agent doesn't follow a fixed script. It reasons step by step:


Thought: What do I need to find out?
Action: Call a tool (web search or PDF generator)
Observation: What did I get back? Is it enough?
Repeat until the agent decides it has sufficient information


This is the ReAct loop (Reasoning + Acting) — the agent controls its own research process rather than executing a hardcoded sequence of steps.


Demo

Example topic: Latest trends in NLP and LLMs 2026

The agent:


Searches "NLP and LLMs trends 2026" → reads results
Searches "recent LLM research papers 2026" → reads results
Searches "latest advancements NLP applications 2026" → decides it has enough
Generates a structured PDF with Executive Summary, Key Findings, Conclusion, and Sources


Expand the 🧠 Agent Reasoning Steps panel in the UI to see every Thought → Action → Observation in real time.


Features


Autonomous web research — agent searches multiple times with refined queries
ReAct reasoning visible — full Thought/Action/Observation trace shown in UI
PDF generation — formatted report with title, sections, bullet points, and sources
Inline PDF viewer — view the report directly in the browser without downloading
Source filtering — agent instructed to cite only credible sources (news, government, academic) — no social media links
Persistent state — PDF and reasoning trace survive button clicks via st.session_state



Architecture

User Input (topic)
      ↓
AgentExecutor (LangChain)
      ↓
  ReAct Loop:
  Thought → Action → Observation (repeats)
      ↓              ↓
  search_web    generate_pdf_report
  (Tavily API)  (ReportLab)
      ↓
  PDF saved to /tmp/
      ↓
  PyMuPDF renders pages as images → st.image (avoids browser CSP issues)
      ↓
  Download + Inline View buttons

Two Tools

search_web — calls Tavily API, returns top 3 results with title, URL, and content. The agent reads the docstring to decide when to call this tool.

generate_pdf_report — takes the agent's synthesized content, parses # and ## markdown markers, and builds a formatted PDF using ReportLab. Called only after the agent judges it has enough information.

Why the Docstring Matters

The LLM never sees the tool's code — it only reads the function name and docstring to decide which tool to call and when. The generate_pdf_report docstring explicitly says "use ONLY after you have searched at least twice" — that instruction is what stops the agent from generating a report after a single search.


Tech Stack

ComponentToolAgent FrameworkLangChain AgentExecutor + create_react_agentReasoning PatternReAct (Thought → Action → Observation)Web SearchTavily API (free tier)LLMLlama 3.3 70B via Groq API (free tier)PDF GenerationReportLabPDF RenderingPyMuPDF (fitz)UIStreamlitDeploymentStreamlit Cloud


Project Structure

Research-agent/
├── agent/
│   └── research_agent.py     # AgentExecutor setup + ReAct prompt
├── tools/
│   ├── search_tool.py        # Tavily web search tool
│   └── pdf_tool.py           # ReportLab PDF generator
├── app.py                    # Streamlit UI + session state
├── requirements.txt
├── .gitignore
└── README.md


Run Locally

bashgit clone https://github.com/mutahir-ahmed-ai/Research-agent
cd Research-agent
pip install -r requirements.txt

Create .streamlit/secrets.toml:

tomlGROQ_API_KEY = "your_groq_key_here"
TAVILY_API_KEY = "your_tavily_key_here"

bashstreamlit run app.py

API Keys (both free):


Groq: console.groq.com
Tavily: tavily.com



Key Technical Decisions

Why hand-write the ReAct prompt instead of using hub.pull()?

LangChain's hub now blocks public prompt pulls by default due to serialization security concerns. Writing the prompt directly makes the agent's reasoning template fully visible and controllable — and removes a runtime network dependency.

Why PyMuPDF instead of embedding PDF in an iframe?

Chrome and most modern browsers block data: URI iframes due to Content-Security-Policy headers. PyMuPDF renders each PDF page as a PNG image server-side — no browser PDF renderer involved, works everywhere.

Why truncate search result content?

Tavily occasionally returns results with large amounts of HTML noise (comment threads, tracking URLs). Truncating content per result keeps each LLM call within Groq's tokens-per-minute limit while preserving the information that matters.


Related Projects


HR Assistant Chatbot — RAG on PDF documents
YouTube Q&A Bot — Dynamic RAG on video transcripts
Savour Restaurant AI — LLM customer service bot



Author

Mutahir Ahmed — AI Developer | NLP & RAG Systems

LinkedIn · GitHub
