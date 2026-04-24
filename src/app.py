import streamlit as st
import requests
from pdf_utils import markdown_to_pdf

RESEARCH_URL   = "http://localhost:8000/research"
COMPARE_URL    = "http://localhost:8000/compare"
PLANNER_URL    = "http://localhost:8000/plan"
STRUCTURED_URL = "http://localhost:8000/structured-report"

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 AI Research Assistant")
st.markdown("Powered by **CrewAI** · **GPT-4o-mini** · **Tavily Search**")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Research Topic",
    "⚖️ Compare Topics",
    "🗺️ Research Planner",
    "📋 Structured Report"
])

# ── TAB 1: Research ───────────────────────────────────────

with tab1:
    topic = st.text_input(
        label="Enter a research topic",
        placeholder="e.g. Future of quantum computing",
        max_chars=200
    )
    if st.button("Generate Report", type="primary", use_container_width=True, key="research_btn"):
        if not topic or len(topic.strip()) < 3:
            st.error("Please enter a valid topic (at least 3 characters).")
        else:
            with st.spinner("Researching... this may take 1-2 minutes."):
                try:
                    response = requests.post(
                        RESEARCH_URL, json={"topic": topic}, timeout=300
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Report generated successfully!")
                        st.divider()
                        st.markdown(data["report"])
                        pdf_bytes = markdown_to_pdf(data["report"], title=topic)
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_bytes,
                            file_name=f"{topic[:30].replace(' ', '_')}_report.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Try a simpler topic.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Make sure FastAPI is running on port 8000.")

# ── TAB 2: Compare ────────────────────────────────────────

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        topic1 = st.text_input("Topic 1", placeholder="e.g. Python", max_chars=100)
    with col2:
        topic2 = st.text_input("Topic 2", placeholder="e.g. JavaScript", max_chars=100)

    if st.button("Compare Topics", type="primary", use_container_width=True, key="compare_btn"):
        if not topic1 or not topic2 or len(topic1.strip()) < 3 or len(topic2.strip()) < 3:
            st.error("Please enter both topics (at least 3 characters each).")
        else:
            with st.spinner(f"Comparing '{topic1}' vs '{topic2}'... this may take 1-2 minutes."):
                try:
                    response = requests.post(
                        COMPARE_URL,
                        json={"topic1": topic1, "topic2": topic2},
                        timeout=300
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Comparison report generated!")
                        st.divider()
                        st.markdown(data["report"])
                        pdf_bytes = markdown_to_pdf(
                            data["report"], title=f"{topic1} vs {topic2}"
                        )
                        st.download_button(
                            label="📥 Download PDF Comparison",
                            data=pdf_bytes,
                            file_name=f"{topic1[:15]}_vs_{topic2[:15]}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Try simpler topics.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Make sure FastAPI is running on port 8000.")

# ── TAB 3: Research Planner ───────────────────────────────

with tab3:
    st.markdown("Break any topic into focused sub-questions before researching.")
    query = st.text_input(
        label="Enter your research query",
        placeholder="e.g. How does machine learning work?",
        max_chars=200,
        key="planner_input"
    )
    if st.button("Generate Research Plan", type="primary", use_container_width=True, key="planner_btn"):
        if not query or len(query.strip()) < 3:
            st.error("Please enter a valid query (at least 3 characters).")
        else:
            with st.spinner("Generating research plan... (~10 seconds)"):
                try:
                    response = requests.post(
                        PLANNER_URL, json={"query": query}, timeout=120
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Research plan ready!")
                        st.divider()
                        st.markdown(data["plan"])
                        st.info(
                            "💡 Tip: Copy any sub-question into the "
                            "**Research Topic** or **Structured Report** tab for a full report."
                        )
                        pdf_bytes = markdown_to_pdf(data["plan"], title=f"Research Plan: {query}")
                        st.download_button(
                            label="📥 Download PDF Plan",
                            data=pdf_bytes,
                            file_name=f"plan_{query[:30].replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.Timeout:
                    st.error("Request timed out.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Make sure FastAPI is running on port 8000.")

# ── TAB 4: Structured Report ──────────────────────────────

with tab4:
    st.markdown("Generate a full academic-style report with abstract, core concepts, applications, and conclusion.")
    struct_query = st.text_input(
        label="Enter your topic",
        placeholder="e.g. Blockchain technology in supply chain",
        max_chars=200,
        key="structured_input"
    )
    if st.button("Generate Structured Report", type="primary", use_container_width=True, key="structured_btn"):
        if not struct_query or len(struct_query.strip()) < 3:
            st.error("Please enter a valid topic (at least 3 characters).")
        else:
            with st.spinner("Generating structured report... this may take 1-2 minutes."):
                try:
                    response = requests.post(
                        STRUCTURED_URL, json={"query": struct_query}, timeout=300
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Structured report ready!")
                        st.divider()
                        st.markdown(data["report"])
                        pdf_bytes = markdown_to_pdf(data["report"], title=struct_query)
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_bytes,
                            file_name=f"report_{struct_query[:30].replace(' ', '_')}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Try a simpler topic.")
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Make sure FastAPI is running on port 8000.")