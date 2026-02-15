🌍 Multilingual AI Plagiarism Detector

A production-ready plagiarism detection system supporting 50+ languages, including Tamil, Hindi, English, Telugu, Bengali, Spanish, French, and Chinese.

Built using Hugging Face’s multilingual sentence transformers, the system detects both direct and cross-language plagiarism with high semantic accuracy.

🚀 Key Features

🌐 Multilingual Detection – Supports 50+ global languages

🔄 Cross-Language Matching – Detects translated plagiarism (e.g., Tamil ↔ English)

📄 Multiple File Support – PDF & TXT uploads

🎯 Pre-trained Transformer Model – No custom training required

📊 Interactive Dashboard – Clean UI with detailed similarity reports

⚙️ Adjustable Similarity Threshold (0.5–1.0)

⚡ Real-Time Sentence-Level Comparison

🧠 Model & Architecture

This project uses paraphrase-multilingual-MiniLM-L12-v2 from Hugging Face.

Model Details:

118M parameters

384-dimensional sentence embeddings

Trained on billions of multilingual sentence pairs

Supports 50+ languages

🔎 Detection Pipeline

Text Extraction – Extracts content from PDF/TXT

Sentence Segmentation – Splits documents into sentences

Embedding Generation – Converts sentences to vector representations

Similarity Computation – Uses cosine similarity

Report Generation – Highlights matches above threshold

🛠️ Tech Stack

Language: Python 3.8+

ML Framework: Hugging Face Transformers

Backend: PyTorch

UI: Gradio

Libraries: Scikit-learn, NumPy, PyPDF2

Deployment-ready for Hugging Face Spaces.

📦 Installation
git clone https://github.com/yourusername/multilingual-plagiarism-detector.git
cd multilingual-plagiarism-detector
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt


Run the app:

python app.py


Open:
http://localhost:7860

⚙️ Configuration

Adjust similarity threshold:

0.5–0.6 → Loose matching (detect paraphrasing)

0.7–0.8 → Recommended balanced detection

0.9–1.0 → Strict (near-identical matches only)

📊 Performance Highlights
Metric	Value
Languages Supported	50+
Embedding Size	384
Model Parameters	118M
Detection Level	Sentence-based semantic similarity
Cross-Language Support	✅
🎯 Use Cases

🎓 Academic integrity verification

🌐 Cross-language plagiarism detection

📰 Article & blog originality checks

📄 Legal & contract validation

🌍 Multilingual document comparison

👩‍💻 Author

Moogambika Govindaraj
AI & Data Science Enthusiast
