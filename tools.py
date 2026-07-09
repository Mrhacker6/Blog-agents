from crewai_tools import YoutubeChannelSearchTool

def get_yt_tool(channel_url, api_key):
    return YoutubeChannelSearchTool(
        youtube_channel_url=channel_url,
        config={
            "llm": {
                "provider": "google",
                "config": {
                    "model": "gemini-2.5-flash",
                    "api_key": api_key,
                },
            }
        },
    )
