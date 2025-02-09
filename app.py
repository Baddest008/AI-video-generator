import openai
import moviepy.editor as mp
import os
import elevenlabs
from pytrends.request import TrendReq

# Set up API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = "your_elevenlabs_api_key_here"
openai.api_key = OPENAI_API_KEY

def get_trending_topics():
    """Fetches trending topics from Google Trends."""
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=["trending now"])
    trends = pytrends.trending_searches()
    return trends.head(5).values.flatten().tolist()

def generate_script(prompt):
    """Generates a video script using OpenAI's GPT API."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def generate_voice(script, output_audio="output_audio.mp3"):
    """Generates AI voice from text using ElevenLabs API."""
    audio = elevenlabs.generate(text=script, voice="Rachel", api_key=ELEVEN_API_KEY)
    elevenlabs.save(audio, output_audio)
    print("🎤 AI Voice Generated!")

def create_video(script, audio_file, output_video="output.mp4"):
    """Creates a simple video with text and audio."""
    text_clip = mp.TextClip(script, fontsize=50, color='white', size=(1080, 720))
    text_clip = text_clip.set_duration(10)
    audio = mp.AudioFileClip(audio_file)
    text_clip = text_clip.set_audio(audio)
    text_clip.write_videofile(output_video, fps=24)

if __name__ == "__main__":
    trending_topics = get_trending_topics()
    print("🔥 Trending Topics:", trending_topics)
    
    user_prompt = input("Enter your video topic or choose from trends: ")
    script = generate_script(user_prompt)
    print("📜 Generated Script:", script)

    generate_voice(script)  # Generate AI voice
    create_video(script, "output_audio.mp3")  # Create video with AI voice