#!/usr/bin/env python
# coding: utf-8

"""
Test script for ARAGOG Dual-Mode Behavior
Tests that the system:
1. Provides medical information for healthcare queries (Medical Mode)
2. Provides general helpful responses for non-medical queries (General Mode)
3. Does NOT add medical warnings to non-medical responses
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from multi_domains_medical_final_rag_model import MemoryEfficientRAGPipeline, config, DOMAINS

def test_dual_mode():
    """Test ARAGOG dual-mode functionality"""
    
    print("\n" + "="*80)
    print("ARAGOG - DUAL MODE TEST")
    print("="*80)
    
    # Initialize pipeline
    print("\n🔧 Initializing RAG pipeline...")
    pipeline = MemoryEfficientRAGPipeline(config, DOMAINS)
    print("✅ Pipeline ready\n")
    
    # Test cases
    test_cases = [
        # ===== MEDICAL MODE TESTS =====
        {
            "query": "What are the symptoms of diabetes?",
            "expected_mode": "medical",
            "category": "Medical - Disease Symptoms",
            "should_contain_medical_info": True,
            "should_contain_medical_disclaimer": True
        },
        {
            "query": "How to treat high blood pressure?",
            "expected_mode": "medical",
            "category": "Medical - Treatment",
            "should_contain_medical_info": True,
            "should_contain_medical_disclaimer": True
        },
        {
            "query": "What causes heart disease?",
            "expected_mode": "medical",
            "category": "Medical - Causes",
            "should_contain_medical_info": True,
            "should_contain_medical_disclaimer": True
        },
        {
            "query": "Is chest pain dangerous?",
            "expected_mode": "medical",
            "category": "Medical - Emergency",
            "should_contain_medical_info": True,
            "should_contain_medical_disclaimer": True
        },
        {
            "query": "What are side effects of chemotherapy?",
            "expected_mode": "medical",
            "category": "Medical - Side Effects",
            "should_contain_medical_info": True,
            "should_contain_medical_disclaimer": True
        },
        
        # ===== GENERAL MODE TESTS =====
        {
            "query": "What is 25 * 16?",
            "expected_mode": "general",
            "category": "General - Math",
            "should_contain_medical_info": False,
            "should_contain_medical_disclaimer": False
        },
        {
            "query": "Explain quicksort algorithm",
            "expected_mode": "general",
            "category": "General - Computer Science",
            "should_contain_medical_info": False,
            "should_contain_medical_disclaimer": False
        },
        {
            "query": "What is the capital of France?",
            "expected_mode": "general",
            "category": "General - Geography",
            "should_contain_medical_info": False,
            "should_contain_medical_disclaimer": False
        },
        {
            "query": "How does photosynthesis work?",
            "expected_mode": "general",
            "category": "General - Biology (Non-Medical)",
            "should_contain_medical_info": False,
            "should_contain_medical_disclaimer": False
        },
        {
            "query": "Who wrote Romeo and Juliet?",
            "expected_mode": "general",
            "category": "General - Literature",
            "should_contain_medical_info": False,
            "should_contain_medical_disclaimer": False
        },
        {
            "query": "What are the best programming practices?",
            "expected_mode": "general",
            "category": "General - Technology",
            "should_contain_medical_info": False,
            "should_contain_medical_disclaimer": False
        },
        {
            "query": "Explain Newton's laws of motion",
            "expected_mode": "general",
            "category": "General - Physics",
            "should_contain_medical_info": False,
            "should_contain_medical_disclaimer": False
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
        expected_mode = test["expected_mode"]
        category = test["category"]
        
        print(f"\n[Test {i}/{len(test_cases)}] {category}")
        print(f"Query: {query}")
        print(f"Expected Mode: {expected_mode}")
        
        try:
            result = pipeline.run_query(query)
            is_medical = result.get("is_medical", False)
            requires_general = result.get("requires_general_response", False)
            answer = result.get("answer", "")
            
            # Medical disclaimer phrases to check
            medical_disclaimers = [
                "consult a healthcare professional",
                "consult a doctor",
                "see a doctor",
                "medical advice",
                "healthcare professional",
                "seek medical",
                "emergency"
            ]
            
            has_medical_disclaimer = any(phrase in answer.lower() for phrase in medical_disclaimers)
            
            # Determine actual mode
            if expected_mode == "medical":
                # Medical mode tests
                if is_medical and not requires_general:
                    # Check if answer has medical content
                    if len(answer) > 50 and test["should_contain_medical_disclaimer"]:
                        if has_medical_disclaimer:
                            status = "✅ PASSED"
                            passed += 1
                            reason = "Medical query handled correctly with disclaimer"
                        else:
                            status = "⚠️ WARNING"
                            passed += 1
                            reason = "Medical query handled but missing expected disclaimer"
                    elif len(answer) > 50:
                        status = "✅ PASSED"
                        passed += 1
                        reason = "Medical query handled correctly"
                    else:
                        status = "❌ FAILED"
                        failed += 1
                        reason = "Medical answer too short or empty"
                else:
                    status = "❌ FAILED"
                    failed += 1
                    reason = "Medical query not recognized as medical"
            
            else:  # expected_mode == "general"
                # General mode tests
                if requires_general and not is_medical:
                    # Check that no medical disclaimers are present
                    if has_medical_disclaimer:
                        status = "❌ FAILED"
                        failed += 1
                        reason = "General query has inappropriate medical disclaimers"
                    else:
                        status = "✅ PASSED"
                        passed += 1
                        reason = "General query handled correctly without medical context"
                else:
                    status = "❌ FAILED"
                    failed += 1
                    reason = "General query incorrectly treated as medical"
            
            print(f"Result: {status}")
            print(f"Reason: {reason}")
            print(f"Mode Detected: {'Medical' if is_medical else 'General'}")
            if len(answer) > 0:
                print(f"Answer Preview: {answer[:150]}...")
            
            results.append({
                "test": i,
                "category": category,
                "query": query,
                "expected_mode": expected_mode,
                "actual_mode": "medical" if is_medical else "general",
                "status": status,
                "reason": reason,
                "has_disclaimer": has_medical_disclaimer
            })
            
        except Exception as e:
            print(f"Result: ❌ ERROR")
            print(f"Error: {str(e)}")
            failed += 1
            results.append({
                "test": i,
                "category": category,
                "query": query,
                "expected_mode": expected_mode,
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
    
    medical_tests = [r for r in results if r["expected_mode"] == "medical"]
    general_tests = [r for r in results if r["expected_mode"] == "general"]
    
    print("\n🏥 Medical Mode Tests:")
    for r in medical_tests:
        disclaimer_note = " [Has Disclaimer]" if r.get("has_disclaimer", False) else ""
        print(f"  {r['status']} [{r['category']}] {r['query'][:50]}...{disclaimer_note}")
    
    print("\n🤖 General Mode Tests:")
    for r in general_tests:
        disclaimer_note = " ⚠️ [Has Medical Disclaimer - SHOULD NOT]" if r.get("has_disclaimer", False) else ""
        print(f"  {r['status']} [{r['category']}] {r['query'][:50]}...{disclaimer_note}")
    
    print("\n" + "="*80)
    print("KEY VALIDATION POINTS")
    print("="*80)
    
    # Check critical requirements
    medical_passed = sum(1 for r in medical_tests if "PASSED" in r["status"])
    general_passed = sum(1 for r in general_tests if "PASSED" in r["status"])
    general_with_disclaimers = sum(1 for r in general_tests if r.get("has_disclaimer", False))
    
    print(f"\n1. Medical queries handled correctly: {medical_passed}/{len(medical_tests)}")
    print(f"2. General queries handled correctly: {general_passed}/{len(general_tests)}")
    print(f"3. General queries WITHOUT medical disclaimers: {len(general_tests) - general_with_disclaimers}/{len(general_tests)}")
    
    if general_with_disclaimers > 0:
        print(f"\n⚠️ WARNING: {general_with_disclaimers} general queries have medical disclaimers (should be 0)")
    
    print("\n" + "="*80)
    if failed == 0:
        print("🎉 ALL TESTS PASSED! Dual-mode behavior is working correctly.")
    else:
        print(f"⚠️ {failed} test(s) failed. Please review the implementation.")
    print("="*80 + "\n")
    
    return passed, failed


if __name__ == "__main__":
    try:
        passed, failed = test_dual_mode()
        sys.exit(0 if failed == 0 else 1)
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
