import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("API_KEY"))

prompt="""You are a YouTube video summarizer. Your task is to read the provided transcript of a YouTube video and create a concise summary, highlighting the key points. Follow these guidelines:

Focus on Key Points: Identify the most important information and main ideas.
Be Concise: Limit the summary to 250 words.
Use Bullet Points: Present the information in clear, easy-to-read bullet points.
Avoid Repetition: Summarize without repeating information.
Maintain Context: Ensure the summary captures the context of the video.
Please summarize the text given here: """


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        ampersand_position = video_id.find('&')
        if ampersand_position != -1:
            video_id = video_id[:ampersand_position]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
      
def extract_yt_title(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        ampersand_position = video_id.find('&')
        if ampersand_position != -1:
            video_id = video_id[:ampersand_position]
        
        
        # Set up the youtube data API client
        api_key = os.getenv("YT_KEY")
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Request video details
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        
       
        # Extract and return the title
        title = response['items'][0]['snippet']['title']

        return title

    except Exception as e:
        raise e
      
      
      
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YTsum - Get summarized")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    
    st.title(extract_yt_title(youtube_link))
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)











