# source_code.py
from dotenv import load_dotenv
import os 
from google import genai
from gtts import gTTS
from io import BytesIO
import re

load_dotenv()

api_key = os.getenv("Google_API_key")

if not api_key:
    raise ValueError("API key not found. Please set the 'Google_API_key' environment variable.")    

client = genai.Client(api_key=api_key)

def create_advanced_prompt(images, style):
    BASE_PROMPT = f"""
    You are a senior Indian Army Colonel who has cleared NDA, IMA, and the SSB selection process
    and has served in multiple leadership and operational roles.

    You are currently evaluating a candidates response for the Thematic Apperception Test (TAT).

    Based on the given image, generate a realistic, psychologically sound TAT story that would
    receive a FULL SCORE (10/10) from an SSB board.

    CORE RULES (MANDATORY):
    
    - Maximum length: 200 words.
    - give a title to story according to the style of story
    - Story must reflect strong Officer Like Qualities (OLQs) such as leadership, initiative,
    responsibility, planning, teamwork, emotional stability, and problem-solving.
    - The main character must take proactive, logical, and positive action.
    - Avoid fantasy, exaggeration, melodrama, or unrealistic heroism.
    - Tone must be mature, calm, and practical.

    CONTENT RULES:
    - Use Indian names or Indian locations wherever appropriate.
    - References may be Indian or international but must remain realistic.
    - Story must follow a clear structure: situation → challenge → action → positive outcome.
    - The character should contribute positively to society, duty, or a team.

    IMPORTANT:
    - Do NOT mention tests, assessments, SSB, OLQs, or evaluation.
    - Write naturally as if authored by a sincere defence aspirant.
    """
    
    style_instructions = {
        "Humorous": "\n**Incorporate light-hearted humor while maintaining realism.",
        "Dramatic": "\n**Add dramatic elements to enhance engagement without exaggeration.",
        "Romantic": "\n**Include subtle romantic elements that fit naturally within the story.",
        "Suspenseful": "\n**Build suspense through realistic challenges and resolutions.",
        "Inspirational": "\n**Craft an uplifting narrative that inspires positive action.",
        "Comedy": "\n**Weave in comedic elements that are tasteful and relevant.",  # Fixed typo: Comediy -> Comedy
        "Thriller": "\n**Create a thrilling atmosphere with realistic tension and resolution.",
        "Sci-fi": "\n**Incorporate science fiction elements while keeping the story plausible."
    }
    
    return BASE_PROMPT + style_instructions.get(style, "")

def generate_story_from_images(images, style):
    prompt = create_advanced_prompt(images, style)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[*images, prompt],
    )
    return response.text

def clean_text_for_audio(text):
    """Clean text for better audio pronunciation"""
    if not text:
        return ""
    
    # Remove markdown formatting but keep punctuation for better speech
    text = re.sub(r'\*\*|\*|##|#|`|_', '', text)  # Remove markdown
    
    # Clean up common issues
    text = re.sub(r'\\n', ' ', text)  # Replace newlines with spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    
    # Ensure proper sentence spacing
    text = re.sub(r'\.(?=\S)', '. ', text)  # Add space after period if missing
    text = re.sub(r'\?(?=\S)', '? ', text)  # Add space after question mark if missing
    text = re.sub(r'!(?=\S)', '! ', text)   # Add space after exclamation if missing
    
    # Clean up quotes
    text = text.replace('"', '').replace("'", '')
    
    # Remove any non-printable characters
    text = ''.join(char for char in text if char.isprintable() or char in ' .,!?;:-')
    
    return text.strip()

def narrate_story(story_text):
    try:
        if not story_text:
            return None
            
        # Clean the text for better audio
        cleaned_text = clean_text_for_audio(story_text)
        
        # Check if text is not empty after cleaning
        if not cleaned_text or len(cleaned_text.strip()) < 10:
            return None
        
        # Create audio
        tts = gTTS(text=cleaned_text, lang='en', slow=False)
        
        # Save to BytesIO
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        
        # Get the audio data
        audio_data = audio_fp.getvalue()
        
        # Verify audio data is not empty
        if audio_data and len(audio_data) > 1000:  # At least 1KB of audio
            return audio_data
        else:
            return None
            
    except Exception as e:
        print(f"Audio generation error: {e}")
        return None