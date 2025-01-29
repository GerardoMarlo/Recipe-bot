import discord
from discord.ext import commands
import yt_dlp
import os
import env

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Replace 'YOUR_CHANNEL_ID' with the channel ID where you want to post the video
# You can find the channel ID by enabling Developer Mode in Discord and right-clicking the channel
# to copy its ID.
TARGET_CHANNEL_ID = YOUR_CHANNEL_ID  # Example: 123456789012345678

# Function to download the video and get the title
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save videos in the downloads folder
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Download video and extract info
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            video_title = info_dict.get('title', 'Untitled Video')
            return filename, video_title
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None, None

# Command to handle video links
@bot.command()
async def upload_video(ctx, url: str):
    # Fetch the target channel by ID
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    
    if not channel:
        await ctx.send("Could not find the target channel!")
        return

    await ctx.send("Downloading video, please wait...")

    # Download the video and get the title
    filename, video_title = download_video(url)
    
    if filename:
        # Send the video and title to the target channel
        await channel.send(f"**Video Title**: {video_title}")
        await channel.send(file=discord.File(filename))

        # Clean up by deleting the video file after uploading
        os.remove(filename)
    else:
        await ctx.send("Failed to download the video. Please check the URL and try again.")

# Run the bot with the token
bot.run('YOUR_BOT_TOKEN')
