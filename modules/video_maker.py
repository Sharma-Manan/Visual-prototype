from moviepy import concatenate_videoclips, ImageClip, AudioFileClip, CompositeAudioClip
from moviepy import resize as vfx_resize  # Robust fix for Ken Burns
from pathlib import Path
from gtts import gTTS
import os
import shutil
import time

# Directory to store temporary audio files
TEMP_DIR = "temp_audio" 

def generate_tts_audio(text, filename):
    """Generates an audio file from text using gTTS (Google Text-to-Speech)."""
    
    print(f"    - Generating audio: {filename}...")
    try:
        tts = gTTS(text=text, lang='en')
        tts.save(filename)
        
        # Check if the file was actually written before proceeding
        filepath = Path(filename)
        if not filepath.exists():
             # If file doesn't exist after saving, raise an error
             raise FileNotFoundError("File creation failed unexpectedly.")
             
        print("    - Audio generated successfully.")
    except Exception as e:
        # Fallback to prevent crash if gTTS fails (e.g., no internet)
        print(f"    - WARNING: gTTS failed ({e}). Attempting to create silent audio placeholder.")
        try:
            # Create a silent audio file to prevent moviepy from crashing
            AudioFileClip(None).set_duration(len(text.split()) * 0.5).write_audiofile(filename)
        except:
             raise Exception(f"CRITICAL: Failed to generate audio file placeholder for {filename}. Check dependencies.")


def create_video(slide_data, slide_image_paths, out_path):
    """
    Creates an animated MP4 video from slide images and generated narration.
    """
    if len(slide_data) != len(slide_image_paths):
        raise ValueError("Mismatched data and image counts. Ensure all slides were exported.")

    final_clips = []
    Path(TEMP_DIR).mkdir(exist_ok=True)

    try:
        for i, data in enumerate(slide_data):
            image_path = slide_image_paths[i]
            audio_path = Path(TEMP_DIR) / f"audio_{i}.mp3"
            
            # 1. Generate TTS Audio
            generate_tts_audio(data['notes'], str(audio_path))
            audio_clip = AudioFileClip(str(audio_path))
            
            # Use audio duration + 1s for the slide duration
            duration = audio_clip.duration + 1 
            
            # 2. Load Slide Image and Apply Ken Burns Effect (Slow Zoom-in)
            image_clip = ImageClip(image_path, duration=duration)
            
            # Apply Ken Burns Effect using the directly imported resize function (vfx_resize)
            # This is the final robust fix for the "fx not found" error
            image_clip = vfx_resize(image_clip, 
                                   newsize=lambda t: 1.0 + 0.1 * (t / duration),
                                   width=image_clip.w * 1.1)

            # 3. Assemble clip with audio
            clip = image_clip.set_audio(audio_clip)
            final_clips.append(clip)
            
        # Concatenate all clips
        final_video = concatenate_videoclips(final_clips, method="compose")
        final_video = final_video.fadeout(1.0).fadein(1.0)
        
        # Set final audio (narration only, no BG music)
        final_video = final_video.set_audio(final_video.audio) 

        # Output MP4 
        # Using preset='ultrafast' for quick prototype output
        final_video.write_videofile(str(out_path), fps=24, codec='libx264', preset='ultrafast')
    
    finally:
        # Clean up temporary audio directory
        shutil.rmtree(TEMP_DIR, ignore_errors=True)