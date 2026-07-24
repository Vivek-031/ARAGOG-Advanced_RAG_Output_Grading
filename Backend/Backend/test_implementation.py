#!/usr/bin/env python
# coding: utf-8

"""
Verification script for ARAGOG implementation
Tests:
1. Medical queries → RAG pipeline
2. General queries → Normal LLM response
3. Irrelevant queries → Polite guidance message
"""

import sys
import os

sys.path.append(os.path.dirname(__file__))

from multi_domains_medical_final_rag_model import MemoryEfficientRAGPipeline, config, DOMAINS

def test_query_routing():
    """Test query classification and routing"""
    
    print("\n" + "="*80)
    print("ARAGOG IMPLEMENTATION VERIFICATION")
    print("="*80)
    
    print("\n🔧 Initializing pipeline...")
    pipeline = MemoryEfficientRAGPipeline(config, DOMAINS)
    print("✅ Pipeline ready\n")
    
    # Test cases
    test_cases = [
        # Medical queries
        {
            "query": "What are the symptoms of diabetes?",
            "expected_type": "medical",
            "description": "Medical - Disease symptoms"
        },
        {
            "query": "How to treat high blood pressure?",
            "expected_type": "medical",
            "description": "Medical - Treatment"
        },
        
        # General queries
        {
            "query": "What is 25 * 16?",
            "expected_type": "general",
            "description": "General - Math"
        },
        {
            "query": "Explain quicksort algorithm",
            "expected_type": "general",
            "description": "General - Computer Science"
        },
        {
            "query": "What is the capital of France?",
            "expected_type": "general",
            "description": "General - Geography"
        },
        
        # Irrelevant queries
        {
            "query": "xyz",
            "expected_type": "irrelevant",
            "description": "Irrelevant - Nonsensical"
        },
        {
            "query": "a",
            "expected_type": "irrelevant",
            "description": "Irrelevant - Too short"
        }
    ]
    
    print("\n" + "="*80)
    print("TESTING QUERY ROUTING")
    print("="*80 + "\n")
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        query = test["query"]
        expected = test["expected_type"]
        desc = test["description"]
        
        print(f"[Test {i}/{len(test_cases)}] {desc}")
        print(f"Query: '{query}'")
        print(f"Expected: {expected}")
        
        try:
            result = pipeline.run_query(query)
            actual_type = result.get("query_type", "unknown")
            answer = result.get("answer", "")
            
            if actual_type == expected:
                status = "✅ PASSED"
                passed += 1
            else:
                status = "❌ FAILED"
                failed += 1
            
            print(f"Actual: {actual_type}")
            print(f"Status: {status}")
            
            # Show answer preview
            if answer:
                preview = answer[:150] + "..." if len(answer) > 150 else answer
                print(f"Answer: {preview}")
            
            print()
            
        except Exception as e:
            print(f"Status: ❌ ERROR")
            print(f"Error: {str(e)}\n")
            failed += 1
    
    # Summary
    print("="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"\nTotal Tests: {len(test_cases)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
    
    # Expected messages
    print("\n" + "="*80)
    print("EXPECTED BEHAVIOR")
    print("="*80)
    print("\n1. Medical queries → Detailed medical answer with RAG")
    print("2. General queries → Direct answer (handled by LLM in API)")
    print("3. Irrelevant queries → 'Please ask a question related to medicine, healthcare, biology, or medical history.'")
    
    print("\n" + "="*80)
    if failed == 0:
        print("🎉 ALL TESTS PASSED!")
    else:
        print(f"⚠️ {failed} test(s) failed")
    print("="*80 + "\n")
    
    return passed, failed


if __name__ == "__main__":
    try:
        passed, failed = test_query_routing()
        sys.exit(0 if failed == 0 else 1)
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
