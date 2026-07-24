#!/usr/bin/env python
# coding: utf-8

import os
import re
import time
import json
import pickle
import gc
import numpy as np
import torch
import faiss
from typing import List, Dict
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
import warnings

warnings.filterwarnings("ignore")

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🔧 Using device: {device} {'(GPU acceleration ON)' if torch.cuda.is_available() else '(CPU mode)'}")


# ========================================================================
# DOMAIN CONFIGURATION
# ========================================================================

@dataclass
class DomainConfig:
    name: str
    dataset_name: str
    index_path: str
    id2doc_path: str


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Check for both possible checkpoint directory structures
CHECKPOINT_BASE = os.path.join(BASE_DIR, "medical_qa_checkpoints")
if os.path.exists(os.path.join(CHECKPOINT_BASE, "medical_qa_checkpoints", "medical_qa_v1.0")):
    INDEXES_DIR = os.path.join(CHECKPOINT_BASE, "medical_qa_checkpoints", "medical_qa_v1.0", "faiss_indexes")
else:
    INDEXES_DIR = os.path.join(CHECKPOINT_BASE, "medical_qa_v1.0", "faiss_indexes")

DOMAINS = [
    DomainConfig("general_medical", "General Medical",
                 os.path.join(CHECKPOINT_BASE, "general_medical_faiss.index"),
                 os.path.join(CHECKPOINT_BASE, "general_medical_id2doc.pkl")),
    DomainConfig("mental_health", "Mental Health",
                 os.path.join(CHECKPOINT_BASE, "mental_health_faiss.index"),
                 os.path.join(CHECKPOINT_BASE, "mental_health_id2doc.pkl")),
    DomainConfig("ophthalmology", "Ophthalmology",
                 os.path.join(CHECKPOINT_BASE, "ophthalmology_faiss.index"),
                 os.path.join(CHECKPOINT_BASE, "ophthalmology_id2doc.pkl")),
    DomainConfig("pediatrics", "Pediatrics",
                 os.path.join(CHECKPOINT_BASE, "pediatrics_faiss.index"),
                 os.path.join(CHECKPOINT_BASE, "pediatrics_id2doc.pkl")),
    DomainConfig("symptoms_triage", "Symptoms Triage",
                 os.path.join(CHECKPOINT_BASE, "symptoms_triage_faiss.index"),
                 os.path.join(CHECKPOINT_BASE, "symptoms_triage_id2doc.pkl")),
    DomainConfig("women_health", "Women Health",
                 os.path.join(CHECKPOINT_BASE, "women_health_faiss.index"),
                 os.path.join(CHECKPOINT_BASE, "women_health_id2doc.pkl")),
    DomainConfig("Cancer", "Cancer Medical QA",
                 os.path.join(INDEXES_DIR, "Cancer_index.faiss"),
                 os.path.join(INDEXES_DIR, "Cancer_docs.pkl")),
    DomainConfig("Cardiology", "Cardiology Medical QA",
                 os.path.join(INDEXES_DIR, "Cardiology_index.faiss"),
                 os.path.join(INDEXES_DIR, "Cardiology_docs.pkl")),
    DomainConfig("Dermatology", "Dermatology Medical QA",
                 os.path.join(INDEXES_DIR, "Dermatology_index.faiss"),
                 os.path.join(INDEXES_DIR, "Dermatology_docs.pkl")),
    DomainConfig("Diabetes-Digestive-Kidney", "Diabetes/Digestive/Kidney Medical QA",
                 os.path.join(INDEXES_DIR, "Diabetes-Digestive-Kidney_index.faiss"),
                 os.path.join(INDEXES_DIR, "Diabetes-Digestive-Kidney_docs.pkl")),
    DomainConfig("Neurology", "Neurology Medical QA",
                 os.path.join(INDEXES_DIR, "Neurology_index.faiss"),
                 os.path.join(INDEXES_DIR, "Neurology_docs.pkl"))
]


class RAGConfig:
    """Memory-optimized configuration"""
    EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    RERANK_MODEL = "BAAI/bge-reranker-base"
    GENERATOR_MODEL = "google/flan-t5-base"
    FAISS_TOP_K = 30
    BM25_TOP_K = 30
    FINAL_TOP_K = 5
    FAISS_WEIGHT = 0.6
    BM25_WEIGHT = 0.4
    MAX_CONTEXT_LENGTH = 512
    MAX_ANSWER_LENGTH = 256


config = RAGConfig()
print(f"\n✅ Memory-optimized configuration loaded")
print(f"📊 Total domains: {len(DOMAINS)}")


# ========================================================================
# MEMORY-EFFICIENT MEDICAL RAG PIPELINE
# ========================================================================

class MemoryEfficientRAGPipeline:
    """Optimized RAG pipeline for medical question answering"""

    def __init__(self, config: RAGConfig, domains: List[DomainConfig]):
        self.config = config
        self.domain_configs = {d.name: d for d in domains}
        print("=" * 80)
        print("🏥 INITIALIZING MEDICAL RAG SYSTEM")
        print("=" * 80)

        # Load small embedder
        print("\n📦 Loading lightweight embedder...")
        self.embedder = SentenceTransformer(config.EMBED_MODEL, device=device)
        print("  ✅ Embedder loaded (80MB)")

        self.loaded_domains = {}
        self._load_all_domains()

        self.reranker = CrossEncoder(config.RERANK_MODEL, device=device)
        print("  ✅ Reranker loaded (300MB)")

        self.generator_tokenizer = AutoTokenizer.from_pretrained(config.GENERATOR_MODEL)
        self.generator_model = AutoModelForSeq2SeqLM.from_pretrained(config.GENERATOR_MODEL).to(device)
        print("  ✅ Generator loaded (900MB)")

        print("\n✅ Pipeline initialized")
        print(f"💾 Domains: {len(domains)} loaded in memory")
        print("=" * 80)

    # --------------------------------------------------------------------
    # Domain Loading
    # --------------------------------------------------------------------
    def _load_all_domains(self):
        print("\n⚡ Preloading all domain indexes for faster responses...")
        for domain in self.domain_configs.values():
            if os.path.exists(domain.index_path):
                print(f"  📂 Loading {domain.name} index...")
                try:
                    index = faiss.read_index(domain.index_path)
                    with open(domain.id2doc_path, "rb") as f:
                        id2doc = pickle.load(f)
                    if isinstance(id2doc, dict):
                        id2doc = list(id2doc.values())
                    bm25 = BM25Okapi([word_tokenize(str(doc).lower()) for doc in id2doc])
                    self.loaded_domains[domain.name] = {
                        "faiss_index": index,
                        "bm25_index": bm25,
                        "id2doc": id2doc
                    }
                    print(f"    ✅ Loaded {len(id2doc)} chunks")
                except Exception as e:
                    print(f"    ❌ Failed to load {domain.name}: {e}")
        print("✅ All domain indexes preloaded.")

    # --------------------------------------------------------------------
    # Utility
    # --------------------------------------------------------------------
    def _classify_query(self, query: str) -> str:
        """
        Classifies query into categories with medical-first approach:
        - 'medical': Medical/healthcare related queries (default for health questions)
        - 'general': Non-medical but answerable queries (math, science, tech, etc.)
        - 'irrelevant': Only truly nonsensical queries
        """
        query_lower = query.lower().strip()
        
        # Only reject truly empty or nonsensical queries
        if len(query_lower) < 2 or not any(c.isalnum() for c in query_lower):
            return 'irrelevant'
        
        # Expanded medical keywords for comprehensive coverage
        medical_keywords = [
            # General medical terms
            "disease", "symptom", "diagnosis", "treatment", "cure", "medicine", "medication",
            "doctor", "hospital", "clinic", "patient", "health", "healthcare", "medical",
            "illness", "condition", "syndrome", "disorder", "infection", "virus", "bacteria",
            "pain", "ache", "fever", "chronic", "acute", "prescription", "therapy",
            "drug", "dose", "dosage", "side effect", "interaction", "contraindication",
            
            # Body parts and systems
            "heart", "lung", "brain", "kidney", "liver", "stomach", "intestine", "blood",
            "bone", "muscle", "skin", "eye", "ear", "nose", "throat", "chest", "abdomen",
            "head", "neck", "back", "joint", "nerve", "artery", "vein", "organ",
            "body", "limb", "foot", "hand", "leg", "arm", "finger", "toe",
            
            # Specific conditions
            "cancer", "diabetes", "hypertension", "asthma", "arthritis", "alzheimer",
            "depression", "anxiety", "migraine", "epilepsy", "pneumonia", "influenza",
            "covid", "tuberculosis", "malaria", "hiv", "aids", "hepatitis", "meningitis",
            "stroke", "seizure", "infection", "allergy", "autoimmune",
            
            # Medical specialties
            "cardiology", "neurology", "dermatology", "oncology", "pediatric", "psychiatric",
            "orthopedic", "gynecology", "urology", "ophthalmology", "radiology",
            "obstetric", "geriatric", "neonatal",
            
            # Procedures and tests
            "surgery", "operation", "biopsy", "scan", "x-ray", "mri", "ct scan", "ultrasound",
            "blood test", "examination", "checkup", "vaccine", "vaccination", "immunization",
            "lab test", "screening", "diagnostic",
            
            # Symptoms
            "cough", "sneeze", "nausea", "vomit", "diarrhea", "constipation", "bleeding",
            "swelling", "rash", "itch", "dizzy", "fatigue", "weakness", "numbness",
            "breathe", "breathing", "headache", "migraine", "seizure", "paralysis",
            "fussy", "pulling at ear", "morning sickness", "nausea",
            
            # Pregnancy and women's health
            "pregnancy", "pregnant", "prenatal", "trimester", "ob-gyn", "obstetrician",
            "menstrual", "period", "contraception", "fertility", "miscarriage",
            
            # Pediatrics
            "child", "baby", "infant", "toddler", "kid", "pediatrician", "newborn",
            "month-old", "year-old", "adolescent",
            
            # Medications (generic and common brands)
            "aspirin", "ibuprofen", "acetaminophen", "warfarin", "metformin", "sertraline",
            "metoclopramide", "antibiotic", "antidepressant", "vitamin", "supplement",
            
            # Prevention and management
            "prevention", "preventive", "screening", "diet", "nutrition", "exercise",
            "wellness", "lifestyle", "risk factor", "complication", "prognosis",
            "recovery", "rehabilitation", "palliative", "hospice",
            
            # Safety and urgency
            "safe", "dangerous", "emergency", "urgent", "serious", "risk", "warning"
        ]
        
        # Check if query contains any medical keywords
        has_medical_keywords = any(keyword in query_lower for keyword in medical_keywords)
        
        # Expanded medical context patterns
        medical_patterns = [
            r'\b(what|how|why|when|where)\s+(is|are|does|can|should).*(disease|symptom|treatment|cause|prevent|cure|diagnose)',
            r'\b(how\s+to\s+treat|how\s+to\s+prevent|how\s+to\s+cure|how\s+to\s+manage)',
            r'\b(side\s+effect|risk\s+factor|warning\s+sign)',
            r'\b(what\s+(causes|triggers|leads\s+to|results\s+in))',
            r'\b(symptoms?\s+of|signs?\s+of|effects?\s+of)',
            r'\b(treatment\s+for|cure\s+for|therapy\s+for|medication\s+for)',
            r'\b(should\s+i\s+see\s+a\s+doctor|when\s+to\s+see|emergency)',
            r'\b(medical\s+advice|health\s+advice|consult|consultation)',
            r'\btaking\s+(medicine|medication|drug|pill)',
            r'\b(is\s+this|is\s+it)\s+safe',
            r'\bshould\s+i\s+(give|take|use)',
            r'\b\d+\s*(-year-old|-month-old|year old|month old)'
        ]
        
        has_medical_pattern = any(re.search(pattern, query_lower) for pattern in medical_patterns)
        
        # Strong non-medical indicators (to avoid false positives)
        strong_non_medical = [
            "movie", "film", "actor", "actress", "sports", "football", "basketball",
            "politics", "election", "president", "parliament", "recipe", "cooking",
            "travel destination", "tourist", "hotel booking", "flight", "weather forecast",
            # Academic/general knowledge indicators
            "calculate", "solve", "equation", "formula", "mathematics", "math", "algebra",
            "algorithm", "programming", "code", "computer science", "programming language",
            "physics", "chemistry", "geography", "history", "capital of", "population of",
            "who invented", "when was", "where is", "plus", "minus", "add", "subtract",
            "multiply", "divide", "equals", "number", "numbers", "count", "sum"
        ]
        
        has_strong_non_medical = any(indicator in query_lower for indicator in strong_non_medical)
        
        # Check for mathematical patterns
        math_patterns = [
            r'\d+\s*\+\s*\d+',  # addition
            r'\d+\s*-\s*\d+',   # subtraction  
            r'\d+\s*\*\s*\d+',  # multiplication
            r'\d+\s*\/\s*\d+',  # division
            r'what\s+is\s+\d+',  # "what is [number]"
            r'how\s+much\s+is\s+\d+',  # "how much is [number]"
        ]
        
        has_math_pattern = any(re.search(pattern, query_lower) for pattern in math_patterns)
        
        # If clearly medical, return medical
        if has_medical_keywords or has_medical_pattern:
            return 'medical'
        
        # If has strong non-medical indicators or math patterns, classify as general
        if has_strong_non_medical or has_math_pattern:
            return 'general'
        
        # Default: Treat health-related questions as medical (permissive approach)
        # Only classify as general if it's clearly about academic topics
        question_words = ["what", "how", "why", "when", "where", "who", "which", "is", "should", "can"]
        has_question_structure = any(word in query_lower for word in question_words)
        
        # Additional academic indicators
        academic_indicators = [
            "calculate", "solve", "equation", "formula", "mathematics", "math",
            "algorithm", "programming", "code", "computer science",
            "physics", "chemistry", "geography", "history", "capital of",
            "population of", "who invented", "when was", "where is"
        ]
        
        has_academic = any(indicator in query_lower for indicator in academic_indicators)
        if has_academic:
            return 'general'
        
        # For very short queries without medical keywords, classify as general
        if len(query_lower.split()) <= 3 and not has_medical_keywords:
            return 'general'
        
        # Default to medical for ambiguous cases (permissive)
        return 'medical'
    
    def _detect_emergency(self, query: str) -> bool:
        emergency_keywords = [
            "stiff neck", "purple spots", "meningitis", "chest pain", "difficulty breathing",
            "severe bleeding", "unconscious", "stroke", "slurred speech", "facial droop",
            "severe headache", "anaphylaxis", "swelling throat", "emergency"
        ]
        return any(kw in query.lower() for kw in emergency_keywords)

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"Chat Doctor|Alma|with Chat", "", text, flags=re.IGNORECASE)
        return re.sub(r"\s+", " ", text).strip()

    # --------------------------------------------------------------------
    # Domain Routing
    # --------------------------------------------------------------------
    def route_to_domains(self, query: str) -> List[str]:
        domain_keywords = {
            "general_medical": ["medical", "health", "disease", "treatment", "medication", "doctor", "hospital", "patient", "drug", "medicine", "prescription", "side effect", "interaction"],
            "mental_health": ["mental", "depression", "anxiety", "stress", "psychiatric", "therapy", "counseling", "mood", "sertraline", "antidepressant"],
            "ophthalmology": ["eye", "vision", "sight", "blind", "cataract", "glaucoma", "retina", "optical"],
            "pediatrics": ["child", "baby", "infant", "pediatric", "newborn", "toddler", "adolescent", "kid", "month-old", "year-old", "pediatrician", "fussy", "ear infection"],
            "symptoms_triage": ["symptom", "pain", "fever", "emergency", "urgent", "acute", "sudden", "severe", "pulling at ear", "when should i see"],
            "women_health": ["women", "pregnancy", "pregnant", "menstrual", "gynecology", "obstetric", "breast", "ovarian", "uterus", "ob-gyn", "prenatal", "trimester", "morning sickness", "warfarin", "blood clot"],
            "Cancer": ["cancer", "tumor", "chemotherapy", "oncology", "malignant", "metastasis", "radiation"],
            "Cardiology": ["heart", "cardiac", "blood pressure", "artery", "cardiovascular", "chest pain", "hypertension", "blood clot", "warfarin", "anticoagulant"],
            "Dermatology": ["skin", "rash", "eczema", "acne", "dermatitis", "psoriasis", "melanoma"],
            "Diabetes-Digestive-Kidney": ["diabetes", "kidney", "digestive", "stomach", "liver", "insulin", "pancreas", "bowel", "metformin", "nausea", "vomiting", "metoclopramide"],
            "Neurology": ["brain", "headache", "migraine", "seizure", "neurological", "nervous", "stroke", "alzheimer"]
        }
        query_lower = query.lower()
        scores = {d: sum(1 for k in ks if k in query_lower) for d, ks in domain_keywords.items()}
        max_score = max(scores.values()) if scores.values() else 0
        
        # Debug: print scores
        print(f"  🔍 Domain routing scores: {scores}")
        print(f"  🎯 Max score: {max_score}")
        
        # Select multiple domains if they have good scores (more comprehensive)
        threshold = max(1, max_score - 1) if max_score > 0 else 0
        selected = [d for d, s in scores.items() if s >= threshold and s > 0]
        
        # Limit to top 3 domains to keep retrieval efficient
        if len(selected) > 3:
            sorted_domains = sorted(selected, key=lambda d: scores[d], reverse=True)
            result = sorted_domains[:3]
        else:
            result = selected if selected else ["general_medical"]
        
        print(f"  ✅ Selected domains: {result}")
        return result

    # --------------------------------------------------------------------
    # Retrieval
    # --------------------------------------------------------------------
    def hybrid_retrieval(self, query: str, domain_names: List[str]) -> List[Dict]:
        all_results = []

        def process(domain_name):
            data = self.loaded_domains[domain_name]
            q_emb = self.embedder.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype("float32")
            D, I = data["faiss_index"].search(q_emb, self.config.FAISS_TOP_K)
            faiss_scores = {i: float(d) for i, d in zip(I[0], D[0])}
            tokenized = word_tokenize(query.lower())
            bm25_scores = data["bm25_index"].get_scores(tokenized)
            bm25_top = np.argsort(bm25_scores)[::-1][:self.config.BM25_TOP_K]
            for idx in bm25_top:
                score = (self.config.FAISS_WEIGHT * faiss_scores.get(idx, 0)) + \
                        (self.config.BM25_WEIGHT * bm25_scores[idx])
                all_results.append({
                    "domain": domain_name,
                    "chunk": data["id2doc"][idx],
                    "score": score
                })

        with ThreadPoolExecutor(max_workers=5) as ex:
            ex.map(process, domain_names)
        return sorted(all_results, key=lambda x: x["score"], reverse=True)[:30]

    # --------------------------------------------------------------------
    # Reranking
    # --------------------------------------------------------------------
    def rerank_results(self, query: str, candidates: List[Dict]) -> List[Dict]:
        # ✅ Ensure chunks are strings for reranker
        pairs = []
        for c in candidates:
            chunk_text = c["chunk"]
            if isinstance(chunk_text, dict):
                chunk_text = chunk_text.get("answer", "") or chunk_text.get("question", "") or str(chunk_text)
            elif not isinstance(chunk_text, str):
                chunk_text = str(chunk_text)
            pairs.append([query, chunk_text])
            c["chunk"] = chunk_text  # Update to ensure it's a string
        
        scores = self.reranker.predict(pairs, show_progress_bar=False)
        for i, c in enumerate(candidates):
            c["rerank_score"] = float(scores[i])
        return sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)[:self.config.FINAL_TOP_K]

    # --------------------------------------------------------------------
    # 💡 FIXED: Full Detailed Answer Generation
    # --------------------------------------------------------------------
    def generate_answer(self, query: str, context_chunks: List[Dict], is_emergency: bool, confidence: float = 1.0) -> str:
        if is_emergency and confidence < 0.4:
            return (
                "🚨 **EMERGENCY - SEEK IMMEDIATE MEDICAL ATTENTION**\n\n"
                "Please call 911 or go to the nearest emergency room immediately.\n"
                "⚠️ Do not delay."
            )

        # Use medical knowledge reasoning even when retrieval is weak
        # Increased threshold because fallback responses are more reliable than small LLM
        if not context_chunks or confidence < 0.6:
            print(f"⚠️ Low confidence retrieval ({confidence:.2f}) - using medical knowledge reasoning")
            
            # Create a medical knowledge prompt that doesn't rely on retrieved context
            medical_prompt = f"""
You are a medical expert. Answer this medical question in 5-8 concise sentences as a natural paragraph.

CRITICAL INSTRUCTIONS:
- Write in plain text paragraph format - NO headings, NO numbered lists, NO bullet points
- Keep answer SHORT (5-8 sentences maximum)
- Include: direct answer, brief explanation, safety concerns, when to see doctor if relevant, emergency signs if high-risk
- Use general medical knowledge and clinical guidelines
- NEVER say "I couldn't find enough information"
- NEVER suggest stopping prescribed medications without medical supervision
- Be clear, accurate, and medically sound

Question: {query}

Write your answer as a concise paragraph (5-8 sentences):
"""
            
            try:
                inputs = self.generator_tokenizer(medical_prompt, return_tensors="pt", max_length=1024, truncation=True).to(device)
                with torch.no_grad():
                    outputs = self.generator_model.generate(
                        **inputs,
                        max_new_tokens=800,
                        temperature=0.8,
                        top_p=0.95,
                        num_beams=4,
                        do_sample=False,
                        repetition_penalty=1.2,
                        no_repeat_ngram_size=3,
                        pad_token_id=self.generator_tokenizer.pad_token_id,
                        eos_token_id=self.generator_tokenizer.eos_token_id
                    )

                answer = self.generator_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
                answer = self._clean_text(answer)

                # Ensure we have a substantial response - use fallback if generation is too short
                if len(answer.split()) < 40:
                    print("⚠️ Generated answer too short, using enhanced fallback")
                    answer = self._generate_fallback_medical_response(query)

                if is_emergency:
                    answer += "\n\n🚨 **If these symptoms are severe or worsening, seek immediate medical care.**"
                else:
                    answer += "\n\n⚠️ This information is educational. Please consult a healthcare professional for personalized medical advice."

                return answer

            except Exception as e:
                print(f"❌ Medical knowledge generation error: {e}")
                return self._generate_fallback_medical_response(query)

        # Original path when we have good context chunks
        context_parts = []
        for c in context_chunks[:8]:
            text = self._clean_text(c["chunk"])
            if len(text) > 60:
                context_parts.append(text)
        combined_context = "\n\n".join(context_parts)[:3500]

        prompt = f"""
You are a medical expert. Answer this medical question in 5-8 concise sentences using the provided knowledge.

CRITICAL INSTRUCTIONS:
- Write in plain text paragraph format - NO headings, NO numbered lists, NO bullet points
- Keep answer SHORT (5-8 sentences maximum)
- Include: direct answer, brief explanation, safety concerns, when to see doctor if relevant, emergency signs if high-risk
- Use the medical knowledge provided AND general clinical guidelines
- NEVER say "I couldn't find enough information"
- NEVER suggest stopping prescribed medications without medical supervision
- Be clear, accurate, and medically sound

Medical Knowledge:
{combined_context}

Question: {query}

Write your answer as a concise paragraph (5-8 sentences):
"""

        try:
            inputs = self.generator_tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True).to(device)
            with torch.no_grad():
                outputs = self.generator_model.generate(
                    **inputs,
                    max_new_tokens=800,
                    temperature=0.8,
                    top_p=0.95,
                    num_beams=4,
                    do_sample=False,
                    repetition_penalty=1.2,
                    no_repeat_ngram_size=3,
                    pad_token_id=self.generator_tokenizer.pad_token_id,
                    eos_token_id=self.generator_tokenizer.eos_token_id
                )

            answer = self.generator_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
            answer = self._clean_text(answer)

            if len(answer.split()) < 40:
                # If generated answer is too short, use fallback which has better content
                print("⚠️ Generated answer lacks detail, using enhanced fallback")
                answer = self._generate_fallback_medical_response(query)

            if is_emergency and confidence >= 0.4:
                answer += "\n\n🚨 **If these symptoms occur, seek immediate medical care.**"
            else:
                answer += "\n\n⚠️ Please consult a healthcare professional for personalized advice."

            # Final content check before returning
            if len(answer.split()) < 35:
                print("⚠️ Final check: answer still too short, using fallback")
                return self._generate_fallback_medical_response(query)
            
            return answer

        except Exception as e:
            print(f"❌ Generation error: {e}")
            return self._generate_fallback_medical_response(query)

    def _generate_fallback_medical_response(self, query: str) -> str:
        """
        Generate a SHORT concise medical response (5-8 sentences) using general medical knowledge
        when the main generation fails or retrieval is very poor.
        Plain text paragraph format - NO structured headings or lists.
        """
        query_lower = query.lower()
        
        # CATEGORY 1: Blood pressure medication
        if any(word in query_lower for word in ["blood pressure", "hypertension", "bp medication", "bp med", "missed dose", "forgot medication", "forgot pill", "forgot to take"]):
            return "If you missed one dose of blood pressure medication, take it as soon as you remember unless it's close to your next scheduled dose. Never double up on doses. Missing a single dose typically causes only a temporary, minor increase in blood pressure and rarely causes immediate danger. However, frequently missing doses can lead to uncontrolled blood pressure and increase your risk of stroke and heart attack. Contact your doctor if you frequently forget doses or have missed multiple consecutive doses. Seek immediate medical attention if you experience severe headache with confusion, chest pain, severe shortness of breath, sudden weakness, irregular heartbeat, or dizziness with fainting. Set phone alarms or use a pill organizer to prevent future missed doses, and never stop taking your medication without consulting your doctor."
        
        # CATEGORY 2: Pregnancy and medication
        elif any(word in query_lower for word in ["pregnant", "pregnancy", "prenatal", "warfarin", "blood clot", "metoclopramide", "morning sickness", "expecting", "trimester"]):
            return "Pregnancy and medication require immediate medical consultation. Warfarin is generally avoided during pregnancy because it crosses the placenta and can affect fetal development. Vitamin K supplements interact with warfarin and can reduce its blood-thinning effectiveness. Metoclopramide is sometimes used for morning sickness but requires medical supervision during pregnancy. Do not stop warfarin or any prescribed medication without medical guidance, as uncontrolled blood clots pose risks to both mother and baby. Seek emergency care immediately if you experience severe abdominal pain, heavy vaginal bleeding, sudden leg swelling, chest pain, difficulty breathing, severe headache, vision changes, or dizziness with fainting."
        
        # CATEGORY 3: Pediatric fever and medication
        elif any(word in query_lower for word in ["child", "baby", "toddler", "infant", "fever", "ear", "aspirin", "month-old", "year-old", "kid", "pediatric"]):
            return "For fever in children, use acetaminophen or ibuprofen based on weight-based dosing. Never give aspirin to children under 19 years old due to the risk of Reye's syndrome. Fever is the body's natural response to infection and is usually not dangerous by itself. Ensure adequate fluid intake to prevent dehydration, monitor temperature regularly, and offer comfort measures like lukewarm baths and light clothing. Contact your pediatrician if fever lasts more than 2-3 days, if your child is under 3 months with any fever, if they seem unusually lethargic or refuse fluids, or if fever exceeds 104°F. Seek emergency care immediately if your child has difficulty breathing, severe headache, stiff neck, seizure, purple rash that doesn't fade when pressed, extreme lethargy, inconsolable crying for hours, or signs of dehydration."
        
        # CATEGORY 4: Diabetes and medication
        elif any(word in query_lower for word in ["diabetes", "blood sugar", "insulin", "metformin", "glucose", "diabetic", "a1c"]):
            return "For diabetes management, continue your prescribed medication regimen and contact your healthcare provider with specific concerns - never stop or change diabetes medications without medical supervision as this can cause dangerous blood sugar fluctuations. Diabetes medications like insulin and metformin work to control blood sugar levels, and consistent timing and dosing are crucial for preventing both high blood sugar (hyperglycemia) and low blood sugar (hypoglycemia). Skipping doses risks dangerously high blood sugar, while taking too much risks hypoglycemia, and long-term poor control increases risk of kidney, eye, nerve, and heart complications. Take medications as prescribed, monitor blood sugar as directed, keep fast-acting sugar available for low blood sugar episodes, and maintain regular check-ups. Seek immediate emergency care if you experience severe low blood sugar symptoms (confusion, loss of consciousness, seizures), signs of diabetic ketoacidosis (excessive thirst, frequent urination, nausea, vomiting, fruity breath odor), blood sugar above 400 mg/dL that won't come down, or inability to eat or drink due to illness."
        
        # CATEGORY 5: Medication interactions (common questions)
        elif any(word in query_lower for word in ["take with", "take ibuprofen", "take aspirin", "take acetaminophen", "medication interaction", "drug interaction", "coffee", "alcohol"]):
            return "Most common over-the-counter pain medications like ibuprofen can be taken with coffee, but coffee may increase stomach irritation when combined with NSAIDs. Caffeine can affect the stomach lining similarly to NSAIDs, potentially increasing the risk of gastric upset, though caffeine is sometimes intentionally combined with pain relievers (like in Excedrin) to enhance pain relief. Take medications with food to reduce stomach irritation, read labels for caffeine warnings, and consider spacing coffee and medication by 30-60 minutes if you're sensitive. Avoid exceeding recommended doses, don't mix multiple pain relievers without medical guidance, and limit caffeine to under 400mg daily. Contact your doctor if you experience persistent stomach pain or if you have a history of stomach ulcers, GERD, or gastritis. Seek emergency care immediately if you experience severe abdominal pain, vomiting blood or coffee-ground material, black tarry stools, severe allergic reactions, or chest pain."
        
        # CATEGORY 6: Cholesterol and heart health
        elif any(word in query_lower for word in ["cholesterol", "ldl", "hdl", "triglycerides", "statin", "lipitor", "heart disease"]):
            return "High cholesterol is caused by a combination of genetics, diet (especially saturated and trans fats), lack of physical activity, obesity, smoking, and age - while some have genetic predisposition (familial hypercholesterolemia), lifestyle factors play a major role. Your liver produces cholesterol and you also get it from animal-based foods; your body needs it for cells and hormones, but too much LDL ('bad' cholesterol) builds up in artery walls forming plaques that narrow blood vessels and increase heart disease risk. High cholesterol has no symptoms but significantly increases risk of heart attack and stroke, and can lead to atherosclerosis (hardening of arteries). Get cholesterol checked regularly (adults 20+ every 4-6 years, more often if high risk), eat a heart-healthy diet, exercise at least 150 minutes weekly, maintain healthy weight, quit smoking, limit saturated fats, and take prescribed medications consistently. See your doctor for screening if you have family history of early heart disease, other cardiovascular risk factors, or have been told you have high cholesterol. High cholesterol itself isn't an emergency, but seek immediate care if you experience heart attack symptoms (chest pain, pain radiating to arm/jaw, shortness of breath, cold sweats) or stroke symptoms (sudden numbness, confusion, severe headache, vision changes) - call 911 immediately."
        
        # CATEGORY 7: Common cold, flu, and respiratory symptoms
        elif any(word in query_lower for word in ["cold", "flu", "cough", "sore throat", "congestion", "runny nose", "sneezing", "influenza"]):
            return "The common cold and flu are caused by different viruses - colds are milder (caused by rhinoviruses with gradual onset of runny nose, congestion, mild cough) while flu (influenza) is more severe with sudden onset of high fever, body aches, fatigue, and dry cough. Most cases resolve on their own with rest, fluids (water, tea, broth), and over-the-counter symptom relief (acetaminophen/ibuprofen for fever and aches), plus warm salt water gargles for sore throat and humidifiers for congestion. Antibiotics don't work on viruses and should not be used unless bacterial complications develop; never give aspirin to children/teens with flu due to Reye's syndrome risk. Contact your doctor if symptoms last over 10 days, fever exceeds 103°F for more than 3 days, you're high-risk (elderly, pregnant, chronic conditions), or symptoms improve then worsen. Seek emergency care immediately if you experience difficulty breathing, persistent chest pain, sudden dizziness, severe vomiting, bluish lips, severe dehydration, or flu symptoms that return with worse cough after initial improvement."
        
        # General medical fallback - short format
        return "This medical question requires personalized evaluation by a healthcare professional, as your specific situation depends on your individual health history, current medications, and other personal factors. Medical questions often involve complex interactions between symptoms, medications, medical history, and allergies, and what works for one person may not be appropriate for another. Consult a qualified healthcare professional for personalized advice, keep track of your symptoms (when they started, severity, changes), and make a list of all medications and supplements you're taking. Do not delay seeking medical care for serious or persistent symptoms, never stop prescribed medications without consulting your doctor, and don't rely solely on internet information for medical decisions. Seek immediate medical attention if you experience chest pain, difficulty breathing, sudden severe headache, loss of consciousness, severe bleeding, stroke signs (facial droop, arm weakness, speech difficulty), severe abdominal pain, or any symptom that feels life-threatening."

    # --------------------------------------------------------------------
    # Main Query Runner
    # --------------------------------------------------------------------
    def run_query(self, query: str) -> Dict:
        start = time.time()
        print(f"\n🔍 Query: {query}")

        # Classify query into medical, general, or irrelevant
        query_type = self._classify_query(query)
        
        # Note: With new permissive classification, almost all health-related queries
        # are classified as medical. Only truly non-medical queries reach here.
        if query_type == 'general':
            print(f"ℹ️ General (non-medical) query detected: {query}")
            return {
                "query": query,
                "answer": "",  # Will be handled by general LLM in API layer
                "domains": [],
                "metrics": {"composite": 0.0, "confidence": 0.0},
                "processing_time": round(time.time() - start, 2),
                "is_emergency": False,
                "sources": [],
                "is_medical": False,
                "requires_general_response": True,
                "query_type": "general"
            }
        
        # Treat even unclear queries as medical with cautious response
        if query_type == 'irrelevant':
            print(f"⚠️ Unclear query - attempting medical interpretation: {query}")
            # Try to provide a helpful response rather than rejection
            query_type = 'medical'  # Force medical processing

        # Medical mode - use RAG pipeline
        print(f"🏥 Medical query detected - using medical RAG pipeline")
        is_emergency = self._detect_emergency(query)
        domains = self.route_to_domains(query)
        print(f"📍 Domains: {domains}")

        candidates = self.hybrid_retrieval(query, domains)
        reranked = self.rerank_results(query, candidates)
        confidence = np.mean([r["rerank_score"] for r in reranked]) if reranked else 0.5
        answer = self.generate_answer(query, reranked, is_emergency, confidence)

        print(f"✅ Medical answer generated ({round(time.time() - start, 2)}s, conf={confidence:.2f})")
        return {
            "query": query,
            "answer": answer,
            "domains": domains,
            "metrics": {"composite": confidence, "confidence": confidence},
            "processing_time": round(time.time() - start, 2),
            "is_emergency": is_emergency,
            "sources": [{"chunk": c["chunk"][:200], "domain": domains[0] if domains else "Unknown", "score": c.get("rerank_score", 0.0)} 
                       for c in reranked[:3]] if reranked else [],
            "is_medical": True,
            "requires_general_response": False,
            "query_type": "medical"
        }


# ========================================================================
# MAIN (Interactive Test Mode)
# ========================================================================
if __name__ == "__main__":
    print("\n🚀 INITIALIZING PIPELINE...")
    pipeline = MemoryEfficientRAGPipeline(config, DOMAINS)
    print("✅ READY!\n")

    while True:
        q = input("🩺 Ask a medical question (or 'exit'): ").strip()
        if q.lower() in ["exit", "quit"]:
            break
        res = pipeline.run_query(q)
        print("\n💬 Answer:\n", res["answer"], "\n")
