#!/usr/bin/env python
# coding: utf-8

"""
Test script for ARAGOG Medical Domain Restriction
Tests that the system only responds to medical queries and rejects non-medical queries
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from multi_domains_medical_final_rag_model import MemoryEfficientRAGPipeline, config, DOMAINS

def test_domain_restriction():
    """Test medical domain restriction functionality"""
    
    print("\n" + "="*80)
    print("ARAGOG MEDICAL - DOMAIN RESTRICTION TEST")
    print("="*80)
    
    # Initialize pipeline
    print("\n🔧 Initializing RAG pipeline...")
    pipeline = MemoryEfficientRAGPipeline(config, DOMAINS)
    print("✅ Pipeline ready\n")
    
    # Test cases
    test_cases = [
        # Medical queries (should be processed)
        {
            "query": "What are the symptoms of diabetes?",
            "expected": "medical",
            "category": "Medical - Disease"
        },
        {
            "query": "How to treat high blood pressure?",
            "expected": "medical",
            "category": "Medical - Treatment"
        },
        {
            "query": "What causes heart disease?",
            "expected": "medical",
            "category": "Medical - Causes"
        },
        {
            "query": "Is chest pain a sign of a heart attack?",
            "expected": "medical",
            "category": "Medical - Symptoms"
        },
        {
            "query": "What are the side effects of chemotherapy?",
            "expected": "medical",
            "category": "Medical - Side Effects"
        },
        
        # Non-medical queries (should be rejected)
        {
            "query": "Who won the last World Cup?",
            "expected": "non-medical",
            "category": "Sports"
        },
        {
            "query": "What is the best movie of 2024?",
            "expected": "non-medical",
            "category": "Entertainment"
        },
        {
            "query": "How do I code in Python?",
            "expected": "non-medical",
            "category": "Technology"
        },
        {
            "query": "What is the capital of France?",
            "expected": "non-medical",
            "category": "General Knowledge"
        },
        {
            "query": "Who is the current president of USA?",
            "expected": "non-medical",
            "category": "Politics"
        },
        {
            "query": "What is the best restaurant in New York?",
            "expected": "non-medical",
            "category": "Food/Travel"
        },
        {
            "query": "Tell me about the latest iPhone",
            "expected": "non-medical",
            "category": "Technology"
        },
        {
            "query": "Who won the NBA championship?",
            "expected": "non-medical",
            "category": "Sports"
        }
    ]
    
    # Run tests
    print("\n" + "="*80)
    print("RUNNING TESTS")
    print("="*80 + "\n")
    
    passed = 0
    failed = 0
    results = []
    
    for i, test in enumerate(test_cases, 1):
        query = test["query"]
        expected = test["expected"]
        category = test["category"]
        
        print(f"\n[Test {i}/{len(test_cases)}] {category}")
        print(f"Query: {query}")
        print(f"Expected: {expected}")
        
        try:
            result = pipeline.run_query(query)
            answer = result.get("answer", "")
            is_out_of_domain = result.get("is_out_of_domain", False)
            
            # Define expected rejection message
            rejection_message = "This application is ARAGOG Medical, designed exclusively to provide medical and healthcare-related information. Please ask a medical-related question."
            
            # Check if result matches expectation
            if expected == "medical":
                # Should get a medical answer (not the rejection message)
                if is_out_of_domain or answer == rejection_message:
                    status = "❌ FAILED"
                    failed += 1
                    reason = "Medical query was rejected"
                else:
                    status = "✅ PASSED"
                    passed += 1
                    reason = "Medical query processed correctly"
            else:  # expected == "non-medical"
                # Should get the rejection message
                if is_out_of_domain and answer == rejection_message:
                    status = "✅ PASSED"
                    passed += 1
                    reason = "Non-medical query rejected correctly"
                else:
                    status = "❌ FAILED"
                    failed += 1
                    reason = "Non-medical query was not rejected"
            
            print(f"Result: {status}")
            print(f"Reason: {reason}")
            print(f"Answer preview: {answer[:100]}...")
            
            results.append({
                "test": i,
                "category": category,
                "query": query,
                "expected": expected,
                "status": status,
                "reason": reason
            })
            
        except Exception as e:
            print(f"Result: ❌ ERROR")
            print(f"Error: {str(e)}")
            failed += 1
            results.append({
                "test": i,
                "category": category,
                "query": query,
                "expected": expected,
                "status": "❌ ERROR",
                "reason": str(e)
            })
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"\nTotal Tests: {len(test_cases)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
    
    # Print detailed results
    print("\n" + "="*80)
    print("DETAILED RESULTS")
    print("="*80)
    
    medical_tests = [r for r in results if "Medical" in r["category"]]
    non_medical_tests = [r for r in results if "Medical" not in r["category"]]
    
    print("\n📋 Medical Queries:")
    for r in medical_tests:
        print(f"  {r['status']} [{r['category']}] {r['query'][:50]}...")
    
    print("\n📋 Non-Medical Queries:")
    for r in non_medical_tests:
        print(f"  {r['status']} [{r['category']}] {r['query'][:50]}...")
    
    print("\n" + "="*80)
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Domain restriction is working correctly.")
    else:
        print(f"⚠️ {failed} test(s) failed. Please review the implementation.")
    print("="*80 + "\n")
    
    return passed, failed


if __name__ == "__main__":
    try:
        passed, failed = test_domain_restriction()
        sys.exit(0 if failed == 0 else 1)
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
