🤗🌍 Multilingual AI Plagiarism Detector
A powerful plagiarism detection tool that works across 50+ languages including Tamil, English, Hindi, Telugu, and more. Built using Hugging Face's state-of-the-art multilingual sentence transformers.

✨ Features
🌍 Multilingual Support: Detects plagiarism in 50+ languages (Tamil, Hindi, English, Telugu, Bengali, Spanish, French, Chinese, and more)
🔄 Cross-Language Detection: Can detect plagiarism even between different languages (e.g., Tamil original vs English translation)
📄 Multiple File Formats: Supports PDF and TXT file uploads
🎯 Pre-trained Models: Uses Hugging Face's paraphrase-multilingual-MiniLM-L12-v2 - no training required!
📊 Interactive Dashboard: Beautiful Gradio interface with detailed similarity reports
⚙️ Adjustable Threshold: Customize similarity threshold (0.5-1.0) for different use cases
🚀 Real-time Processing: Fast sentence-level plagiarism detection

🛠️ Tech Stack
Framework: Python 3.8+
ML Model: Hugging Face Transformers (paraphrase-multilingual-MiniLM-L12-v2)
UI: Gradio
Libraries: PyTorch, Scikit-learn, PyPDF2, NumPy
Deployment: Compatible with Hugging Face Spaces

📦 Installation
Clone the repository
bashgit clone https://github.com/yourusername/multilingual-plagiarism-detector.git
cd multilingual-plagiarism-detector
Create virtual environment
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies
bashpip install -r requirements.txt
🚀 Usage

Run the application

bashpython app.py

Open your browser


Navigate to http://localhost:7860
Upload two documents (PDF or TXT)
Adjust similarity threshold if needed
Click "Check Plagiarism"

📝 Requirements
Create a requirements.txt file with:
txttransformers==4.35.0
torch==2.1.0
scikit-learn==1.3.2
numpy==1.24.3
gradio==4.8.0
PyPDF2==3.0.1
🌐 Supported Languages
Indian Languages: Tamil (தமிழ்), Hindi (हिन्दी), Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu
European Languages: English, Spanish, French, German, Italian, Portuguese, Russian, Dutch, Polish
Asian Languages: Chinese, Japanese, Korean, Thai, Vietnamese, Indonesian
And 30+ more languages!

📊 How It Works
Text Extraction: Extracts text from uploaded PDF/TXT files
Sentence Segmentation: Splits documents into individual sentences
Embedding Generation: Converts sentences to 384-dimensional vectors using pre-trained multilingual BERT
Similarity Calculation: Computes cosine similarity between sentence embeddings
Report Generation: Identifies and highlights matching sentences above threshold

🎯 Use Cases

Academic Integrity: Check student assignments and research papers
Content Verification: Verify originality of articles and blog posts
Translation Checking: Detect if content is translated plagiarism
Multi-language Documents: Compare documents across different languages
Legal Documents: Verify originality of contracts and agreements

🧪 Example
pythonfrom plagiarism_checker_multilingual import MultilingualPlagiarismDetector

# Initialize detector
detector = MultilingualPlagiarismDetector()

# Check plagiarism
doc1 = "Your first document text here"
doc2 = "Your second document text here"

plagiarism_pct, matches = detector.check_plagiarism(doc1, doc2, threshold=0.8)

print(f"Plagiarism: {plagiarism_pct:.1f}%")
print(f"Matching sentences: {len(matches)}")
🔧 Configuration
Adjust the similarity threshold in the Gradio interface:

0.5-0.6: Loose matching (catch paraphrased content)
0.7-0.8: Moderate matching (recommended)
0.9-1.0: Strict matching (only near-identical sentences)

📈 Model Performance

Model: paraphrase-multilingual-MiniLM-L12-v2
Parameters: 118M
Embedding Dimension: 384
Languages: 50+
Training Data: Billions of multilingual sentence pairs

Hugging Face for the amazing multilingual transformer models
Sentence Transformers for pre-trained models
Gradio for the beautiful UI framework

👩‍💻 Author
Moogambika Govindaraj

Portfolio: moogambika.github.io/portfolio
LinkedIn: linkedin.com/in/moogambika-govindaraj
GitHub: @Moogambika
Email: moogambikagovindaraj@gmail.com
