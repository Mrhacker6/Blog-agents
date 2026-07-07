from crewai import Agent, LLM
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)


def create_agents(yt_tool):
    blog_researcher = Agent(
        role="YouTube Research Specialist",
        goal=(
            "Search the provided YouTube channel and gather the most relevant "
            "information about {topic}."
        ),
        verbose=True,
        memory=False,
        backstory=(
            "You are an experienced AI researcher with over 16 years of expertise "
            "in Machine Learning, Deep Learning, NLP, Generative AI, LLMs, "
            "Transformers, Fine-Tuning, RAG, LangChain, and AI Agents. "
            "You specialize in extracting valuable insights from YouTube videos "
            "and presenting them in a structured format."
        ),
        llm=llm,
        tools=[yt_tool],
        allow_delegation=False,
    )

    blog_writer = Agent(
        role="Technical Blog Writer",
        goal=(
            "Write a professional, engaging, and easy-to-understand blog "
            "using the research collected about {topic}."
        ),
        verbose=True,
        memory=False,
        backstory=(
            "You are a senior technical content writer who transforms complex "
            "technical concepts into engaging blog posts. Your blogs are SEO-friendly, "
            "well-structured, and written in simple language while maintaining "
            "technical accuracy."
        ),
        llm=llm,
        allow_delegation=False,
    )

    return blog_researcher, blog_writer