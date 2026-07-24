"""
Test to verify that answers contain FULL CONTENT, not just section headers
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_content_richness(query, description):
    """Test if the answer contains actual content under each section"""
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
            answer = result.get('answer', 'No answer')
            
            print("FULL ANSWER:")
            print("-" * 80)
            print(answer)
            print("-" * 80)
            
            # Check content richness
            word_count = len(answer.split())
            sentence_count = answer.count('.') + answer.count('!') + answer.count('?')
            
            print(f"\n📊 CONTENT METRICS:")
            print(f"   Total words: {word_count}")
            print(f"   Sentences: {sentence_count}")
            print(f"   Characters: {len(answer)}")
            
            # Check if it's just headers or has real content
            if word_count < 50:
                print("   ❌ FAIL: Answer too short - likely just headers")
            elif sentence_count < 10:
                print("   ⚠️  WARNING: Low sentence count - may lack detail")
            else:
                print("   ✅ PASS: Appears to have substantial content")
            
            # Check for section headers
            sections = [
                "Direct Answer", "DIRECT ANSWER",
                "Medical Explanation", "MEDICAL EXPLANATION",
                "Safety Concerns", "SAFETY CONCERNS",
                "What to Do", "WHAT TO DO",
                "When to See", "WHEN TO SEE",
                "Emergency", "EMERGENCY"
            ]
            
            sections_found = sum(1 for s in sections if s in answer)
            print(f"   Section headers found: {sections_found}")
            
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

# Test with common medical questions
print("\n" + "="*80)
print("TESTING CONTENT RICHNESS OF MEDICAL ANSWERS")
print("="*80)

test_content_richness(
    "I missed my blood pressure medication today. What should I do?",
    "Blood Pressure Medication"
)

test_content_richness(
    "Can I take ibuprofen with coffee?",
    "Simple Medication Interaction"
)

test_content_richness(
    "What causes high cholesterol?",
    "General Medical Question"
)

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
print("\nExpectation: Each answer should have 100+ words with detailed content")
print("="*80 + "\n")
