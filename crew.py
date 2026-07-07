from crewai import Crew, Process

from agents import create_agents
from Task import create_tasks
from tools import get_yt_tool


def blog(channel_url, topic):
    """
    Creates a dynamic Crew for any YouTube channel.
    """
    yt_tool = get_yt_tool(channel_url)
    blog_researcher, blog_writer = create_agents(yt_tool)
    researcher_task, writer_task = create_tasks(
        blog_researcher,
        blog_writer,
        yt_tool
    )

    crew = Crew(
        agents=[
            blog_researcher,
            blog_writer
        ],
        tasks=[
            researcher_task,
            writer_task
        ],
        process=Process.sequential,
        verbose=True,
        memory=False,
        cache=False,
        max_rpm=75,
        share_crew=False,
    )

    result = crew.kickoff(
        inputs={
            "topic": topic,
            "channel": channel_url
        }
    )

    return str(result)