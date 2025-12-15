import re

def generate_slide_content(section_text):
    """
    Generates structured slide content (headline, bullets, notes) from a text section.
    
    Args:
        section_text (str): A block of text representing a key section.
        
    Returns:
        dict: Structured slide data, or None if the section is too short.
    """
    # Simple sentence splitting
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', section_text.strip())
    
    # Filter out empty or very short sentences
    sentences = [s.strip() for s in sentences if len(s.strip().split()) > 4]

    if len(sentences) < 2:
        return None # Not enough content for a slide

    # 1. Headline: First sentence (limit length)
    headline = sentences[0]
    if len(headline.split()) > 20:
        headline = ' '.join(headline.split()[:20]) + '...'
    
    # 2. Bullets: Next two sentences (ensure they are short)
    bullets = [s for s in sentences[1:3] if len(s.split()) < 15]
    
    # 3. Speaker Notes (for TTS): A slightly simplified version
    notes = f"Let's explore the concept of {headline.split(':')[0].strip()} in more detail."

    return {
        'title': headline,
        'bullets': bullets,
        'notes': notes,
        # Visual Query is just the title for simple icon selection
        'visual_query': headline.split(':')[0].strip()
    }