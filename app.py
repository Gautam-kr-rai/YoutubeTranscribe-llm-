import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# prompt="""You are Yotube video summarizer. You will be taking the transcript text
# and summarizing the entire video and providing the important summary in points
# within 250 words. Please provide the summary of the text given here:  """

# prompt = """You are a professional summarizer for YouTube videos. Please analyze the transcript provided and extract all essential information to form a well-rounded summary. Organize your response into these sections:

# 1. **Main Topic**: Briefly describe the primary focus or subject of the video.
# 2. **Key Points**: Summarize major ideas, arguments, or explanations covered, presented as bullet points for clarity.
# 3. **Important Quotes or Insights**: Highlight any direct quotes or noteworthy insights that enhance the understanding of the topic.
# 4. **Actionable Steps or Tips (if applicable)**: If the video offers advice or instructions, list them clearly here.
# 5. **Conclusion**: Provide a concise summary of the main takeaways, including the speaker's final thoughts or conclusions.

# Limit the entire summary to 300 words, ensuring the most relevant details are presented. Use clear, concise language to maintain readability."""


prompt = """You are an academic content summarizer and question generator focused on maximizing detail and coverage for exam preparation. Using the provided transcript, create the following:

1. **Comprehensive Notes**: Summarize the video content in an organized format, covering key concepts, definitions, explanations, examples, and applications as thoroughly as possible. Include any formulas, processes, or frameworks presented.

2. **Exam-Style Questions and Answers**:
   - **Multiple-Choice Questions (MCQs)**: Generate all possible MCQs based on the content, ensuring comprehensive coverage of each concept and detail. For each question:
     - Provide 4 answer options, clearly marking the correct one.
   - **Short Answer Questions**: Write concise questions to test knowledge of definitions, concepts, and explanations.
   - **Long Answer Questions**: Frame questions that encourage critical thinking and analysis, summarizing ideal answer points.

Focus on including every detail from the transcript to ensure a thorough understanding and test preparation. The response should cover all relevant topics extensively, ensuring that every aspect of the academic content is reflected in both the notes and the questions."""



## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter🎥-->🗒️")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)




