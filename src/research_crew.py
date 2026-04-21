import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM, Process
from crewai_tools import TavilySearchTool

load_dotenv()

llm = LLM(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

search_tool = TavilySearchTool(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=5
)

# ── AGENTS ────────────────────────────────────────────────

researcher = Agent(
    role="Web Researcher",
    goal="Search the web and collect detailed, factual information on the given topic",
    backstory=(
        "You are an expert research analyst. You use web search to find "
        "current, accurate information and compile it thoroughly."
    ),
    tools=[search_tool],
    llm=llm,
    verbose=True
)

summarizer = Agent(
    role="Content Summarizer",
    goal="Summarize raw research findings into clear, concise key points",
    backstory=(
        "You are a skilled content editor who takes detailed research and "
        "distills it into the most important insights without losing accuracy."
    ),
    llm=llm,
    verbose=True
)

report_writer = Agent(
    role="Report Writer",
    goal=(
        "Format research findings into well-structured, clearly written reports "
        "in multiple formats depending on the task."
    ),
    backstory=(
        "You are a professional technical writer who presents research "
        "in multiple formats to serve different reader needs — from quick "
        "summaries to in-depth structured reports."
    ),
    llm=llm,
    verbose=True
)

# ── FEATURE 1: Research Report ────────────────────────────

def build_crew(topic: str) -> Crew:

    research_task = Task(
        description=(
            f"Search the web for comprehensive information on: '{topic}'. "
            "Collect at least 5 key findings with their source URLs."
        ),
        expected_output=(
            "A detailed list of findings about the topic, each with a source URL."
        ),
        agent=researcher
    )

    summarize_task = Task(
        description=(
            "Take the research findings provided and summarize them into "
            "5-7 concise bullet points. Focus on the most important and "
            "interesting insights. Do not include URLs in the summary."
        ),
        expected_output=(
            "A bullet-point summary of 5-7 key insights from the research."
        ),
        agent=summarizer,
        context=[research_task]
    )

    report_task = Task(
        description=(
            f"""Using the summarized research, generate three different formats 
of answers for the topic: '{topic}'.

Follow this exact output format:

---
## Concise Answer
(2-3 lines, direct and to the point)

---
## Detailed Explanation
(well-structured, clear, and informative — 3 to 4 paragraphs)

---
## Key Insights
- (5-7 bullet points highlighting the most important facts)

Rules:
- Keep answers factual and well-structured
- Avoid repetition between sections
- Use simple but precise language
- Do not include irrelevant information
            """
        ),
        expected_output=(
            "A structured markdown response with three sections: "
            "Concise Answer, Detailed Explanation, and Key Insights."
        ),
        agent=report_writer,
        context=[summarize_task]
    )

    crew = Crew(
        agents=[researcher, summarizer, report_writer],
        tasks=[research_task, summarize_task, report_task],
        process=Process.sequential,
        verbose=True
    )

    return crew

# ── FEATURE 2: Comparison Report ─────────────────────────

def build_comparison_crew(topic1: str, topic2: str) -> Crew:

    comparison_research_task = Task(
        description=(
            f"Search the web and collect factual information on both of these topics:\n"
            f"Topic 1: '{topic1}'\n"
            f"Topic 2: '{topic2}'\n"
            "Gather key facts, use cases, advantages, and limitations for each."
        ),
        expected_output=(
            f"A factual summary covering key facts, use cases, advantages, "
            f"and limitations for both '{topic1}' and '{topic2}' with source URLs."
        ),
        agent=researcher
    )

    comparison_report_task = Task(
        description=(
            f"""Using the research findings, compare '{topic1}' and '{topic2}'.

Follow this exact output format:

---
## Overview
- Brief explanation of {topic1}
- Brief explanation of {topic2}

---
## Key Differences
- (Point-wise comparison between the two topics)

---
## Comparison Table
| Feature | {topic1} | {topic2} |
|---------|----------|----------|
| Definition | | |
| Use Cases | | |
| Advantages | | |
| Limitations | | |

---
## When to Use What
- {topic1}: (scenarios where this is preferred)
- {topic2}: (scenarios where this is preferred)

Rules:
- Keep it concise but informative
- Avoid vague statements
- Ensure the table is properly formatted markdown
- Avoid repetition between sections
            """
        ),
        expected_output=(
            "A structured markdown comparison with Overview, Key Differences, "
            "Comparison Table, and When to Use What sections."
        ),
        agent=report_writer,
        context=[comparison_research_task]
    )

    crew = Crew(
        agents=[researcher, report_writer],
        tasks=[comparison_research_task, comparison_report_task],
        process=Process.sequential,
        verbose=True
    )

    return crew

# ── FEATURE 3: Research Planner ───────────────────────────

def build_planner_crew(query: str) -> Crew:

    planner_task = Task(
        description=(
            f"""You are a research planner. Given the user query below, break it into 
3-5 important sub-questions that would help in understanding the topic deeply.

Query: '{query}'

Rules:
- Cover fundamentals, applications, and key concepts
- Keep questions specific and useful
- Do not repeat similar questions
- Each question should explore a different angle of the topic

Follow this exact output format:

---
## Research Plan for: {query}

### Sub-Questions to Explore:

- **Question 1:** (covering fundamentals)
- **Question 2:** (covering how it works)
- **Question 3:** (covering real-world applications)
- **Question 4:** (covering advantages and limitations)
- **Question 5:** (covering future scope or trends)

---
### Why These Questions Matter:
(2-3 lines explaining how answering these questions will give a complete 
understanding of the topic)
            """
        ),
        expected_output=(
            "A structured research plan with 3-5 specific sub-questions "
            "and a brief explanation of why they matter."
        ),
        agent=report_writer
    )

    crew = Crew(
        agents=[report_writer],
        tasks=[planner_task],
        process=Process.sequential,
        verbose=True
    )

    return crew

# ── FEATURE 4: Structured Report ─────────────────────────

def build_structured_report_crew(query: str) -> Crew:

    research_task = Task(
        description=(
            f"Search the web for comprehensive information on: '{query}'. "
            "Collect detailed facts, core concepts, real-world applications, "
            "and key insights with source URLs."
        ),
        expected_output=(
            "A detailed collection of facts, concepts, applications, and "
            f"insights about '{query}' with source URLs."
        ),
        agent=researcher
    )

    structured_report_task = Task(
        description=(
            f"""Using the research findings, generate a fully structured report 
on the topic: '{query}'.

Follow this exact output format:

---
# {{title}}

---
## Abstract
(3-4 lines summarizing the entire topic clearly)

---
## Introduction
(2-3 paragraphs introducing the topic, its background, and why it matters)

---
## Core Concepts / Explanation
(Detailed explanation of the core ideas, mechanisms, or principles involved)

---
## Key Insights
- (6-8 bullet points highlighting the most important facts and findings)

---
## Applications
(Real-world use cases and practical applications — can use sub-headings)

---
## Conclusion
(2-3 paragraphs wrapping up the topic, current state, and future outlook)

Rules:
- Use clear headings exactly as shown
- Keep it informative but concise
- Avoid repetition across sections
- Do not include source URLs in the report
            """
        ),
        expected_output=(
            "A complete structured markdown report with Title, Abstract, "
            "Introduction, Core Concepts, Key Insights, Applications, "
            "and Conclusion sections."
        ),
        agent=report_writer,
        context=[research_task]
    )

    crew = Crew(
        agents=[researcher, report_writer],
        tasks=[research_task, structured_report_task],
        process=Process.sequential,
        verbose=True
    )

    return crew


# ── TEST RUN ──────────────────────────────────────────────

if __name__ == "__main__":
    topic = "Impact of Large Language Models on software development in 2025"
    crew = build_crew(topic)
    result = crew.kickoff()
    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60)
    print(result)