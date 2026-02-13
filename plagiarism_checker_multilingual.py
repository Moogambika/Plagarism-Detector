from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MultilingualPlagiarismDetector:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Initialize with multilingual pre-trained Hugging Face model
        
        Supports 50+ languages including:
        - English, Tamil, Hindi, Telugu, Bengali, Marathi
        - Spanish, French, German, Chinese, Japanese, Korean
        - And many more!
        
        Args:
            model_name: Name of pre-trained multilingual model from Hugging Face Hub
        """
        print(f"Loading multilingual pre-trained model: {model_name}")
        
        # Load pre-trained tokenizer from Hugging Face
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Load pre-trained model from Hugging Face
        self.model = AutoModel.from_pretrained(model_name)
        
        # Set to evaluation mode (no training!)
        self.model.eval()
        
        print("✅ Multilingual model loaded successfully!")
        print("   Supports: Tamil, English, Hindi, Telugu, Bengali, and 45+ more languages")
    
    def get_embedding(self, text):
        """
        Convert text to embedding using pre-trained multilingual model
        Works for ANY language - NO TRAINING REQUIRED!
        """
        # Tokenize using pre-trained tokenizer
        inputs = self.tokenizer(text, return_tensors="pt", 
                               padding=True, truncation=True, max_length=512)
        
        # Get embeddings using pre-trained model (no gradient computation)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.numpy()[0]
    
    def split_into_sentences(self, text):
        """Split text into sentences - works for multiple languages"""
        # Handle multiple sentence endings (English, Tamil, Hindi, etc.)
        sentences = text.replace('!', '.').replace('?', '.').replace('।', '.').replace('|', '.').split('.')
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    def check_plagiarism(self, text1, text2, threshold=0.8):
        """
        Check plagiarism between two texts using multilingual pre-trained model
        Works even if documents are in DIFFERENT languages!
        
        Returns:
            plagiarism_percentage: float
            matching_sentences: list of dicts
        """
        # Split into sentences
        sentences1 = self.split_into_sentences(text1)
        sentences2 = self.split_into_sentences(text2)
        
        if not sentences1 or not sentences2:
            return 0, []
        
        print(f"Analyzing {len(sentences1)} sentences from Doc1 vs {len(sentences2)} from Doc2")
        print("Using multilingual pre-trained embeddings (supports Tamil, Hindi, English, etc.)...")
        
        # Get embeddings using pre-trained model
        embeddings1 = [self.get_embedding(s) for s in sentences1]
        embeddings2 = [self.get_embedding(s) for s in sentences2]
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(embeddings1, embeddings2)
        
        # Find matches
        matches = []
        for i, sent1 in enumerate(sentences1):
            max_sim = np.max(similarity_matrix[i])
            if max_sim >= threshold:
                best_match_idx = np.argmax(similarity_matrix[i])
                matches.append({
                    'original': sent1,
                    'matched': sentences2[best_match_idx],
                    'similarity': float(max_sim),
                    'sentence_num': i + 1
                })
        
        plagiarism_pct = (len(matches) / len(sentences1)) * 100
        
        return plagiarism_pct, matches

# Example usage showing multilingual capability
if __name__ == "__main__":
    print("="*60)
    print("MULTILINGUAL PLAGIARISM DETECTOR")
    print("="*60)
    
    # Initialize detector (downloads multilingual pre-trained model)
    detector = MultilingualPlagiarismDetector()
    
    print("\n" + "="*60)
    print("MODEL INFO:")
    print("- Source: Hugging Face Model Hub")
    print("- Model: paraphrase-multilingual-MiniLM-L12-v2")
    print("- Languages: 50+ including Tamil, Hindi, English")
    print("- Pre-trained: YES ✅")
    print("- Training required: NO ❌")
    print("="*60 + "\n")
    
    # Test with English
    doc1_en = """
    Machine learning is a subset of artificial intelligence. It enables computers 
    to learn from data without being explicitly programmed.
    """
    
    doc2_en = """
    ML is part of AI technology. It allows systems to learn from data automatically.
    """
    
    print("Test 1: English documents")
    pct, matches = detector.check_plagiarism(doc1_en, doc2_en)
    print(f"Plagiarism: {pct:.1f}%\n")
    
    # Test with Tamil (example)
    doc1_ta = """
    இயந்திர கற்றல் செயற்கை நுண்ணறிவின் ஒரு பகுதி. இது கணினிகள் தரவுகளிலிருந்து கற்றுக்கொள்ள உதவுகிறது.
    """
    
    doc2_ta = """
    இயந்திர கற்றல் AI தொழில்நுட்பத்தின் பகுதியாகும். இது அமைப்புகளை தானாக தரவுகளிலிருந்து கற்க அனுமதிக்கிறது.
    """
    
    print("Test 2: Tamil documents")
    pct_ta, matches_ta = detector.check_plagiarism(doc1_ta, doc2_ta)
    print(f"Plagiarism: {pct_ta:.1f}%\n")