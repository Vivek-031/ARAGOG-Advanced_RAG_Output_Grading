"""
Test script to verify updated medical assistant behavior
Tests that common medical questions receive comprehensive 6-step answers
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_medical_question(query, description):
    """Test a medical question and display the response"""
    print("\n" + "="*80)
    print(f"TEST: {description}")
    print("="*80)
    print(f"Query: {query}\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/ask",
            json={"query": query},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status: SUCCESS")
            print(f"Mode: {result.get('mode', 'N/A')}")
            print(f"Confidence: {result.get('confidence', 0.0):.2f}")
            print(f"Domains: {', '.join(result.get('domains', []))}")
            print(f"\nAnswer Preview (first 500 chars):")
            print("-" * 80)
            answer = result.get('answer', 'No answer')
            print(answer[:500])
            if len(answer) > 500:
                print(f"... [+{len(answer) - 500} more characters]")
            print("-" * 80)
            
            # Check for 6-step structure
            steps_found = []
            if "DIRECT ANSWER" in answer or "1." in answer:
                steps_found.append("1. Direct Answer")
            if "MEDICAL EXPLANATION" in answer or "2." in answer:
                steps_found.append("2. Medical Explanation")
            if "SAFETY CONCERNS" in answer or "3." in answer:
                steps_found.append("3. Safety Concerns")
            if "WHAT TO DO" in answer or "4." in answer:
                steps_found.append("4. What To Do")
            if "WHEN TO SEE" in answer or "5." in answer:
                steps_found.append("5. When to See Doctor")
            if "EMERGENCY" in answer or "6." in answer:
                steps_found.append("6. Emergency Signs")
            
            if steps_found:
                print(f"\n✅ Structure check: Found {len(steps_found)} step markers")
                for step in steps_found:
                    print(f"   • {step}")
            else:
                print(f"\n⚠️ Structure check: No clear 6-step structure detected")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

# Test cases
print("\n" + "="*80)
print("TESTING UPDATED MEDICAL ASSISTANT BEHAVIOR")
print("="*80)

# Test 1: Blood pressure medication (should use fallback with 6-step structure)
test_medical_question(
    "I missed my blood pressure medication today. What should I do?",
    "Blood Pressure Medication Question"
)

# Test 2: Pediatric fever (should use fallback with 6-step structure)
test_medical_question(
    "My 18-month-old has a fever of 102°F and is pulling at their ear. Is it safe to give aspirin?",
    "Pediatric Fever Question"
)

# Test 3: Pregnancy medication (should use fallback with 6-step structure)
test_medical_question(
    "I'm pregnant and taking warfarin for blood clots. Is this safe?",
    "Pregnancy Medication Question"
)

# Test 4: General diabetes question (should use fallback or RAG)
test_medical_question(
    "What should I do if I forgot to take my metformin this morning?",
    "Diabetes Medication Question"
)

# Test 5: Common symptom question (should use RAG pipeline)
test_medical_question(
    "I have chest pain when I exercise. Should I be worried?",
    "Chest Pain Symptom Question"
)

print("\n" + "="*80)
print("TESTING COMPLETE")
print("="*80)
print("\nExpected behavior:")
print("✅ All answers should use 6-step structure")
print("✅ No 'I couldn't find enough information' responses")
print("✅ Comprehensive medical guidance provided")
print("✅ Safety disclaimers included")
print("="*80 + "\n")
