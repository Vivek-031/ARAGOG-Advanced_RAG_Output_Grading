"""
Test to verify SHORT concise answers (5-8 sentences) in plain text paragraph format
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_short_format(query, description):
    """Test if the answer is short, concise, and without formatting"""
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
            
            print("ANSWER:")
            print("-" * 80)
            print(answer)
            print("-" * 80)
            
            # Count sentences (approximate)
            sentence_count = answer.count('.') + answer.count('!') + answer.count('?')
            word_count = len(answer.split())
            
            # Check for structured formatting
            has_headings = any(x in answer for x in ['**1.', '**2.', '**3.', 'DIRECT ANSWER:', 'MEDICAL EXPLANATION:'])
            has_bullets = '- ' in answer and answer.count('- ') > 2
            has_numbered_list = bool(sum(1 for x in ['1.', '2.', '3.', '4.', '5.', '6.'] if x in answer[:100]) > 2)
            
            print(f"\n📊 FORMAT CHECK:")
            print(f"   Sentences: ~{sentence_count}")
            print(f"   Words: {word_count}")
            print(f"   Has section headings: {'❌ YES (BAD)' if has_headings else '✅ NO (GOOD)'}")
            print(f"   Has bullet lists: {'❌ YES (BAD)' if has_bullets else '✅ NO (GOOD)'}")
            print(f"   Has numbered lists: {'❌ YES (BAD)' if has_numbered_list else '✅ NO (GOOD)'}")
            
            # Overall assessment
            is_short = sentence_count <= 12 and word_count <= 200
            is_plain_text = not (has_headings or has_bullets or has_numbered_list)
            
            if is_short and is_plain_text:
                print(f"\n✅ PASS: Answer is short and in plain text paragraph format")
            elif is_plain_text:
                print(f"\n⚠️  PARTIAL: Plain text format but could be shorter")
            elif is_short:
                print(f"\n⚠️  PARTIAL: Short but has structured formatting")
            else:
                print(f"\n❌ FAIL: Answer is too long or has structured formatting")
                
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

# Test cases
print("\n" + "="*80)
print("TESTING SHORT CONCISE ANSWER FORMAT")
print("="*80)

test_short_format(
    "I missed my blood pressure medication today. What should I do?",
    "Blood Pressure Medication"
)

test_short_format(
    "Can I take ibuprofen with coffee?",
    "Simple Medication Question"
)

test_short_format(
    "What causes high cholesterol?",
    "General Health Question"
)

test_short_format(
    "My child has a fever. Should I give them aspirin?",
    "Pediatric Question"
)

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
print("\nExpected: Short paragraphs (5-8 sentences), NO headings, NO bullet lists")
print("="*80 + "\n")
