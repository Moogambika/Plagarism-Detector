import gradio as gr
from plagiarism_checker_multilingual import MultilingualPlagiarismDetector
import PyPDF2
import time

# Initialize with multilingual pre-trained Hugging Face model
detector = MultilingualPlagiarismDetector()

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def get_severity_color(percentage):
    """Return color based on plagiarism severity"""
    if percentage >= 75:
        return "#d32f2f", "Critical", "🚨"
    elif percentage >= 50:
        return "#f57c00", "High", "⚠️"
    elif percentage >= 25:
        return "#fbc02d", "Moderate", "⚡"
    else:
        return "#388e3c", "Low", "✅"

def create_progress_bar(percentage):
    """Create a visual progress bar"""
    color, severity, icon = get_severity_color(percentage)
    
    return f"""
    <div style="margin: 20px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 18px; font-weight: 600; color: #1a237e;">Plagiarism Score</span>
            <span style="font-size: 24px; font-weight: 700; color: {color};">{icon} {percentage:.1f}%</span>
        </div>
        <div style="background: #e0e0e0; border-radius: 10px; height: 30px; overflow: hidden; box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);">
            <div style="background: linear-gradient(90deg, {color}, {color}aa); width: {percentage}%; height: 100%; 
                        border-radius: 10px; transition: width 0.5s ease; display: flex; align-items: center; justify-content: flex-end; padding-right: 10px;">
                <span style="color: white; font-weight: 600; font-size: 12px;">{severity}</span>
            </div>
        </div>
    </div>
    """

def check_plagiarism_interface(file1, file2, threshold, progress=gr.Progress()):
    """Main function for Gradio with progress tracking"""
    
    if not file1 or not file2:
        return "", "<div style='text-align: center; padding: 40px; color: #757575;'>⚠️ Please upload both documents</div>"
    
    progress(0.2, desc="📄 Extracting text from documents...")
    time.sleep(0.3)
    
    # Extract text
    if file1.name.endswith('.pdf'):
        text1 = extract_text_from_pdf(file1)
    else:
        text1 = file1.read().decode('utf-8')
    
    if file2.name.endswith('.pdf'):
        text2 = extract_text_from_pdf(file2)
    else:
        text2 = file2.read().decode('utf-8')
    
    progress(0.5, desc="🤖 Analyzing with AI model...")
    time.sleep(0.5)
    
    # Check plagiarism using multilingual pre-trained Hugging Face model
    pct, matches = detector.check_plagiarism(text1, text2, threshold)
    
    progress(0.8, desc="📊 Generating report...")
    time.sleep(0.3)
    
    total_sentences = len(detector.split_into_sentences(text1))
    color, severity, icon = get_severity_color(pct)
    
    # Create beautiful report
    report = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <h1 style="margin: 0; font-size: 32px; font-weight: 700;">🔍 Plagiarism Analysis Report</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px;">Powered by Hugging Face Multilingual AI 🤗🌍</p>
    </div>
    
    {create_progress_bar(pct)}
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(102,126,234,0.4);">
            <div style="font-size: 36px; font-weight: 700; margin-bottom: 5px;">{total_sentences}</div>
            <div style="font-size: 14px; opacity: 0.9;">Total Sentences</div>
        </div>
        
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 25px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(245,87,108,0.4);">
            <div style="font-size: 36px; font-weight: 700; margin-bottom: 5px;">{len(matches)}</div>
            <div style="font-size: 14px; opacity: 0.9;">Matches Found</div>
        </div>
        
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 25px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(79,172,254,0.4);">
            <div style="font-size: 36px; font-weight: 700; margin-bottom: 5px;">{int(threshold*100)}%</div>
            <div style="font-size: 14px; opacity: 0.9;">Threshold Used</div>
        </div>
        
        <div style="background: linear-gradient(135deg, {color}dd 0%, {color} 100%); padding: 25px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            <div style="font-size: 36px; font-weight: 700; margin-bottom: 5px;">{severity}</div>
            <div style="font-size: 14px; opacity: 0.9;">Severity Level</div>
        </div>
    </div>
    
    <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; border-left: 5px solid #667eea; margin: 20px 0;">
        <h3 style="margin: 0 0 10px 0; color: #1a237e; font-size: 16px;">🤗 Model Information</h3>
        <p style="margin: 5px 0; color: #424242; font-size: 14px;"><strong>Model:</strong> paraphrase-multilingual-MiniLM-L12-v2</p>
        <p style="margin: 5px 0; color: #424242; font-size: 14px;"><strong>Languages:</strong> Tamil, Hindi, English, Telugu, Bengali + 45 more</p>
        <p style="margin: 5px 0; color: #424242; font-size: 14px;"><strong>Type:</strong> Sentence Transformer (Pre-trained BERT)</p>
    </div>
    """
    
    # Detailed matches with beautiful cards
    matches_html = """
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px;">
        <h2 style="margin: 0; font-size: 24px; font-weight: 600;">🔍 Detailed Match Analysis</h2>
    </div>
    """
    
    if matches:
        for idx, match in enumerate(matches, 1):
            similarity_pct = match['similarity'] * 100
            bar_color, _, _ = get_severity_color(similarity_pct)
            
            matches_html += f"""
            <div style="background: white; border-radius: 12px; padding: 25px; margin: 15px 0; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.1); border-left: 6px solid {bar_color};
                        transition: transform 0.2s, box-shadow 0.2s;">
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: #1a237e; font-size: 18px; font-weight: 600;">
                        Match #{idx}
                    </h3>
                    <div style="background: {bar_color}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600; font-size: 14px;">
                        {similarity_pct:.1f}% Similar
                    </div>
                </div>
                
                <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <div style="color: #e65100; font-weight: 600; font-size: 12px; text-transform: uppercase; margin-bottom: 8px;">
                        📄 Document 1 (Original)
                    </div>
                    <div style="color: #424242; line-height: 1.6; font-size: 15px;">
                        {match['original']}
                    </div>
                </div>
                
                <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; border-radius: 8px; margin: 10px 0;">
                    <div style="color: #0d47a1; font-weight: 600; font-size: 12px; text-transform: uppercase; margin-bottom: 8px;">
                        📄 Document 2 (Matched)
                    </div>
                    <div style="color: #424242; line-height: 1.6; font-size: 15px;">
                        {match['matched']}
                    </div>
                </div>
                
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #e0e0e0;">
                    <span style="color: #757575; font-size: 12px;">Sentence Position: #{match['sentence_num']}</span>
                </div>
            </div>
            """
    else:
        matches_html += """
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 40px; border-radius: 15px; text-align: center; color: white;
                    box-shadow: 0 10px 30px rgba(56,239,125,0.3);">
            <div style="font-size: 64px; margin-bottom: 20px;">✅</div>
            <h3 style="margin: 0; font-size: 28px; font-weight: 700;">No Plagiarism Detected!</h3>
            <p style="margin: 15px 0 0 0; font-size: 16px; opacity: 0.9;">
                The documents appear to be original and unique.
            </p>
        </div>
        """
    
    progress(1.0, desc="✅ Complete!")
    return report, matches_html

# Custom CSS for even better styling
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif !important;
}

.gradio-container {
    max-width: 1400px !important;
}

.gr-button-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 12px 32px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
}

.gr-button-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102,126,234,0.6) !important;
}

.gr-file {
    border: 2px dashed #667eea !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

.gr-file:hover {
    border-color: #764ba2 !important;
    background: #f8f9ff !important;
}

footer {
    display: none !important;
}
"""

# Create stunning Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), css=custom_css, title="🤗🌍 Multilingual Plagiarism Detector") as demo:
    
    gr.HTML("""
    <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin-bottom: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2);">
        <h1 style="color: white; font-size: 48px; margin: 0; font-weight: 700; letter-spacing: -1px;">
            🤗🌍 Multilingual Plagiarism Detector
        </h1>
        <p style="color: rgba(255,255,255,0.95); font-size: 20px; margin: 15px 0 0 0; font-weight: 400;">
            AI-Powered Plagiarism Detection Across 50+ Languages
        </p>
        <div style="margin-top: 20px; display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; color: white; font-size: 14px; backdrop-filter: blur(10px);">
                ✨ Tamil
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; color: white; font-size: 14px; backdrop-filter: blur(10px);">
                🌟 Hindi
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; color: white; font-size: 14px; backdrop-filter: blur(10px);">
                💫 English
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; color: white; font-size: 14px; backdrop-filter: blur(10px);">
                ⚡ +47 More
            </span>
        </div>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("""
            ### 📄 Document 1
            <p style="color: #757575; font-size: 14px;">Upload the original document</p>
            """)
            file1 = gr.File(
                label="", 
                file_types=['.pdf', '.txt'],
                file_count="single"
            )
        
        with gr.Column(scale=1):
            gr.Markdown("""
            ### 📄 Document 2
            <p style="color: #757575; font-size: 14px;">Upload the document to check</p>
            """)
            file2 = gr.File(
                label="", 
                file_types=['.pdf', '.txt'],
                file_count="single"
            )
    
    with gr.Row():
        threshold = gr.Slider(
            0.5, 1.0, 
            value=0.8, 
            step=0.05,
            label="🎯 Similarity Threshold",
            info="Adjust sensitivity: Lower = catch more matches | Higher = stricter detection"
        )
    
    check_btn = gr.Button(
        "🔍 Analyze Documents with AI", 
        variant="primary", 
        size="lg",
        scale=1
    )
    
    gr.HTML("""
    <div style="text-align: center; margin: 20px 0; padding: 15px; background: #f5f5f5; border-radius: 10px;">
        <p style="margin: 0; color: #757575; font-size: 14px;">
            ⚡ Powered by Hugging Face Transformers • 🚀 Lightning Fast Analysis • 🔒 Secure & Private
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            report_output = gr.HTML()
        
        with gr.Column(scale=1):
            matches_output = gr.HTML()
    
    check_btn.click(
        fn=check_plagiarism_interface,
        inputs=[file1, file2, threshold],
        outputs=[report_output, matches_output]
    )
    
    gr.HTML("""
    <div style="margin-top: 40px; padding: 30px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 15px;">
        <h3 style="color: #1a237e; margin: 0 0 20px 0; font-size: 24px;">📚 How It Works</h3>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 32px; margin-bottom: 10px;">📤</div>
                <h4 style="color: #667eea; margin: 0 0 10px 0;">1. Upload Documents</h4>
                <p style="color: #757575; margin: 0; font-size: 14px;">Upload PDFs or text files in any supported language</p>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 32px; margin-bottom: 10px;">🤖</div>
                <h4 style="color: #667eea; margin: 0 0 10px 0;">2. AI Analysis</h4>
                <p style="color: #757575; margin: 0; font-size: 14px;">Pre-trained multilingual BERT analyzes sentence similarity</p>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 32px; margin-bottom: 10px;">📊</div>
                <h4 style="color: #667eea; margin: 0 0 10px 0;">3. Get Results</h4>
                <p style="color: #757575; margin: 0; font-size: 14px;">View detailed plagiarism report with matched sentences</p>
            </div>
            
            <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="font-size: 32px; margin-bottom: 10px;">🌍</div>
                <h4 style="color: #667eea; margin: 0 0 10px 0;">4. Cross-Language</h4>
                <p style="color: #757575; margin: 0; font-size: 14px;">Detects plagiarism even across different languages!</p>
            </div>
        </div>
    </div>
    
    <div style="margin-top: 30px; padding: 25px; background: white; border-radius: 15px; border: 2px solid #667eea;">
        <h3 style="color: #1a237e; margin: 0 0 15px 0; font-size: 20px;">🌐 Supported Languages (50+)</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 10px;">
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Tamil (தமிழ்)</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Hindi (हिन्दी)</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">English</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Telugu</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Bengali</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Marathi</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Gujarati</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Kannada</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Malayalam</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Spanish</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">French</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">German</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Chinese</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Japanese</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">Korean</span>
            <span style="background: #e8eaf6; color: #3f51b5; padding: 6px 12px; border-radius: 15px; font-size: 13px;">+ 35 More!</span>
        </div>
    </div>
    
    <div style="margin-top: 30px; text-align: center; padding: 20px; background: #f5f5f5; border-radius: 10px;">
        <p style="margin: 0; color: #424242; font-size: 14px;">
            Built with ❤️ by Moogambika Govindaraj
        </p>
        
    </div>
    """)

if __name__ == "__main__":
    demo.launch(share=False)