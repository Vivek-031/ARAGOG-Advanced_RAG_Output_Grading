#!/usr/bin/env python
"""
Test script to verify the medical RAG fixes for the two example queries
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from multi_domains_medical_final_rag_model import MemoryEfficientRAGPipeline, config, DOMAINS

def test_medical_queries():
    print("="*80)
    print("TESTING MEDICAL RAG FIXES")
    print("="*80)
    
    # Initialize pipeline
    print("\n🚀 Initializing pipeline...")
    pipeline = MemoryEfficientRAGPipeline(config, DOMAINS)
    print("✅ Pipeline ready!\n")
    
    # Test queries
    test_queries = [
        "I'm a 28-year-old woman taking warfarin for a blood clot. I just found out I'm pregnant and also started taking prenatal vitamins with vitamin K. My OB-GYN prescribed metoclopramide for morning sickness. Is this safe?",
        "My 18-month-old has had a fever of 102°F for 2 days. Today she's pulling at her ear and seems fussy but is eating normally and playing. My friend said to give her aspirin. Should I do that? When should I see a doctor?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"TEST QUERY {i}:")
        print(f"{'='*60}")
        print(f"Query: {query}\n")
        
        result = pipeline.run_query(query)
        
        print(f"Query Type: {result.get('query_type', 'unknown')}")
        print(f"Is Medical: {result.get('is_medical', False)}")
        print(f"Requires General Response: {result.get('requires_general_response', True)}")
        print(f"Emergency: {result.get('is_emergency', False)}")
        print(f"Confidence: {result.get('metrics', {}).get('confidence', 0):.2f}")
        print(f"Processing Time: {result.get('processing_time', 0):.2f}s")
        
        answer = result.get('answer', '')
        print(f"\nANSWER ({len(answer)} characters):")
        print("-" * 40)
        print(answer)
        print("-" * 40)
        
        # Check if we got a meaningful response (not fallback)
        if "couldn't find enough relevant information" in answer.lower():
            print("❌ FAILED: Still getting fallback response!")
        elif len(answer.split()) < 20:
            print("❌ FAILED: Response too short!")
        else:
            print("✅ SUCCESS: Got meaningful medical response!")
        
        print(f"\n{'='*60}\n")

if __name__ == "__main__":
    test_medical_queries()
