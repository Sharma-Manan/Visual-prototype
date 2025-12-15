import argparse
from pathlib import Path

# Import the core processing functions
from modules.pdf_processor import extract_key_sections
from modules.content_generator import generate_slide_content
from modules.slide_builder import create_pptx
from modules.video_maker import create_video

def run_pipeline(input_pdf, output_dir):
    """Executes the full pipeline: PDF -> Slides -> Video."""
    
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    
    pptx_path = outdir / "slides.pptx"
    video_path = outdir / "video.mp4"
    
    print("\n========================================================")
    print(f"       Infooware Edu Prototype: Running Pipeline        ")
    print("========================================================\n")

    # --- Stage 1: Ingestion & Extraction ---
    print("1. Starting PDF Ingestion & Extraction...")
    key_sections = extract_key_sections(input_pdf, N=8)
    if not key_sections:
        print("   - FAILED: Could not extract sufficient content from PDF. Exiting.")
        return

    # --- Stage 2: Content Generation ---
    print("\n2. Summarizing Key Sections and Generating Slide Content...")
    slide_data = []
    for i, section in enumerate(key_sections):
        content = generate_slide_content(section)
        if content:
            slide_data.append(content)
            print(f"   - Slide {len(slide_data)} Title: {content['title'][:50]}...")

    # --- Stage 3: Slide Assembly ---
    print(f"\n3. Assembling PPTX Slide Deck: {pptx_path}")
    create_pptx(slide_data, pptx_path)
    print("   - SUCCESS: PPTX created.")

    # --- CRITICAL INTERMEDIATE STEP ---
    print("\n========================================================")
    print("      *** ACTION REQUIRED: PPTX to IMAGE CONVERSION ***")
    print("========================================================")
    print("  To proceed, you MUST convert the slides.pptx file into")
    print(f"  individual PNG/JPG images: {outdir}/slide_1.png, /slide_2.png, etc.")
    print("  (Use PowerPoint or LibreOffice 'Export as Images' feature.)")
    print("  Press Enter to continue once images are ready in the output folder...")
    input()
    
    # --- Stage 4: Video Generation ---
    print(f"\n4. Generating Video: {video_path}")
    
    # Generate list of expected image paths
    slide_image_paths = [outdir / f"slide_{i+1}.png" for i in range(len(slide_data))]

    try:
        create_video(slide_data, slide_image_paths, video_path)
        print("\n✅ Pipeline complete!")
        print(f"Output files: {pptx_path.name} and {video_path.name} created in {outdir}/")
    except Exception as e:
        print(f"\n❌ FAILED: Video creation failed. Error: {e}")
        print("   - Check if FFmpeg is installed and if all slide_N.png files exist.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infooware Edu Prototype: PDF to Slides & Video")
    parser.add_argument('--input', required=True, help='Path to the input PDF file (e.g., assets/sample.pdf).')
    parser.add_argument('--outdir', default='output', help='Directory to save the output files.')
    
    args = parser.parse_args()
    
    run_pipeline(args.input, args.outdir)