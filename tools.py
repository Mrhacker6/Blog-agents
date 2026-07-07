from crewai_tools import YoutubeChannelSearchTool

def get_yt_tool(channel_url):
    return YoutubeChannelSearchTool(youtube_channel_url=channel_url)
