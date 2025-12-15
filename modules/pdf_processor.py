import pdfplumber

def extract_key_sections(pdf_path, N=8):
    """
    Extracts text from the PDF and returns the N longest sections as key topics.
    
    Args:
        pdf_path (str): Path to the input PDF file.
        N (int): Number of key sections/slides to target.
        
    Returns:
        list: A list of strings, where each string is a raw text section.
    """
    try:
        all_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Get text, clean up excessive whitespace/newlines
                page_text = page.extract_text(x_tolerance=1).replace('\n', ' ')
                all_text += page_text + "\n\n"
                
        # Split by double newline to get paragraphs/sections
        # Filter out very short sections that are likely footnotes or headers
        sections = [s.strip() for s in all_text.split('\n\n') if len(s.strip()) > 100]
        
        # Sort sections by length and take the top N longest ones
        sections.sort(key=len, reverse=True)
        
        print(f"    - Extracted {len(sections)} substantial text sections.")
        return sections[:N]

    except Exception as e:
        print(f"Error during PDF processing: {e}")
        return []

if __name__ == '__main__':
    # Simple test run (requires a sample.pdf in the root)
    # sections = extract_key_sections('../assets/sample.pdf')
    # print(f"Found {len(sections)} sections.")
    pass