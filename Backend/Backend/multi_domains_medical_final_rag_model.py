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
            "Cancer": ["cancer", "tumor", "chemotherapy", "oncology", "malignant"],
            "Cardiology": ["heart", "cardiac", "blood pressure", "artery", "cardiovascular"],
            "Dermatology": ["skin", "rash", "eczema", "acne", "dermatitis"],
            "Diabetes-Digestive-Kidney": ["diabetes", "kidney", "digestive", "stomach", "liver", "insulin"],
            "Neurology": ["brain", "headache", "migraine", "seizure", "neurological", "nervous"]
        }
        query_lower = query.lower()
        scores = {d: sum(1 for k in ks if k in query_lower) for d, ks in domain_keywords.items()}
        max_score = max(scores.values()) if scores.values() else 0
        
        # Debug: print scores
        print(f"  🔍 Domain routing scores: {scores}")
        print(f"  🎯 Max score: {max_score}")
        
        top = [d for d, s in scores.items() if s == max_score and s > 0]
        result = top if top else ["Cardiology"]
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

        if not context_chunks:
            return (
                "I couldn't find enough relevant information to answer this accurately.\n\n"
                "⚠️ Please consult a qualified healthcare professional."
            )

        context_parts = []
        for c in context_chunks[:8]:
            text = self._clean_text(c["chunk"])
            if len(text) > 60:
                context_parts.append(text)
        combined_context = "\n\n".join(context_parts)[:3500]

        prompt = f"""
You are an expert medical assistant providing detailed, factual answers.
Use the context to answer completely.

Context:
{combined_context}

Question: {query}

Write a professional, structured answer including:
1. Explanation and causes
2. Common symptoms
3. Treatment or management
4. When to seek medical help
End with a clear disclaimer.
"""

        try:
            inputs = self.generator_tokenizer(prompt, return_tensors="pt", max_length=1024, truncation=True).to(device)
            with torch.no_grad():
                outputs = self.generator_model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=0.6,
                    top_p=0.9,
                    num_beams=4,
                    do_sample=False,
                    repetition_penalty=1.15,
                    pad_token_id=self.generator_tokenizer.pad_token_id,
                    eos_token_id=self.generator_tokenizer.eos_token_id
                )

            answer = self.generator_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
            answer = self._clean_text(answer)

            if len(answer.split()) < 40:
                best_chunk = self._clean_text(context_chunks[0]["chunk"])
                sentences = sent_tokenize(best_chunk)
                answer = " ".join(sentences[:10])

            if is_emergency and confidence >= 0.4:
                answer += "\n\n🚨 **If these symptoms occur, seek immediate medical care.**"
            else:
                answer += "\n\n⚠️ Please consult a healthcare professional for personalized advice."

            return answer

        except Exception as e:
            print(f"❌ Generation error: {e}")
            fallback = self._clean_text(context_chunks[0]["chunk"])
            return fallback + "\n\n⚠️ Please consult a healthcare professional."

    # --------------------------------------------------------------------
    # Main Query Runner
    # --------------------------------------------------------------------
    def run_query(self, query: str) -> Dict:
        start = time.time()
        print(f"\n🔍 Query: {query}")

        is_emergency = self._detect_emergency(query)
        domains = self.route_to_domains(query)
        print(f"📍 Domains: {domains}")

        candidates = self.hybrid_retrieval(query, domains)
        reranked = self.rerank_results(query, candidates)
        confidence = np.mean([r["rerank_score"] for r in reranked]) if reranked else 0.5
        answer = self.generate_answer(query, reranked, is_emergency, confidence)

        print(f"✅ Answer generated ({round(time.time() - start, 2)}s, conf={confidence:.2f})")
        return {
            "query": query,
            "answer": answer,
            "domains": domains,
            "metrics": {"composite": confidence, "confidence": confidence},  # ✅ Include both keys for compatibility
            "processing_time": round(time.time() - start, 2),
            "is_emergency": is_emergency,
            "sources": [{"chunk": c["chunk"][:200], "domain": domains[0] if domains else "Unknown", "score": c.get("rerank_score", 0.0)} 
                       for c in reranked[:3]] if reranked else []
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
