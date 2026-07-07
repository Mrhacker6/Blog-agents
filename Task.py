from crewai import Task


def create_tasks(blog_researcher, blog_writer, yt_tool):

    researcher = Task(
        description="""
        Search ONLY the provided YouTube channel.

        Channel:
        {channel}

        Find videos related to:
        {topic}

        Use the YoutubeChannelSearchTool exactly once.

        Extract:
        - Main concepts
        - Key takeaways
        - Tools/frameworks mentioned
        - Practical applications
        """,
        expected_output="""
        Provide:
        1. Video Summary
        2. Key Concepts
        3. Tools Mentioned
        4. Examples
        5. Practical Applications
        """,
        tools=[yt_tool],
        agent=blog_researcher,
    )

    write_task = Task(
        description="""
        Using the research from the previous task,
        write a detailed, SEO-friendly blog article on {topic}.

        The blog should include:

        - Catchy Title
        - Introduction
        - Well-structured headings
        - Examples
        - Key Takeaways
        - Conclusion
        """,
        expected_output="""
        A markdown blog containing:

        # Title

        ## Introduction

        ## Main Sections

        ## Key Takeaways

        ## Conclusion
        """,
        agent=blog_writer,
        async_execution=False,
        output_file="generated_blog.md",
    )

    return researcher, write_task