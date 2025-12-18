"""Test detailed answer generation with new parameters"""
import time
import requests
import json

BASE_URL = "http://localhost:5000"

print("="*80)
print("Testing Detailed Answer Generation")
print("="*80)

# Test queries
test_queries = [
    {
        "query": "What are the symptoms of migraine?",
        "expected": "Detailed 5-6 sentence explanation"
    },
    {
        "query": "What are the early symptoms of a stroke?",
        "expected": "Emergency warning with high confidence for stroke keywords"
    }
]

for i, test in enumerate(test_queries, 1):
    print(f"\n{'='*80}")
    print(f"Test {i}: {test['query']}")
    print(f"Expected: {test['expected']}")
    print(f"{'='*80}\n")
    
    try:
        start = time.time()
        
        response = requests.post(
            f"{BASE_URL}/api/ask",
            json={"query": test['query']},
            timeout=120
        )
        
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Status: 200 OK")
            print(f"⏱️  Response Time: {elapsed:.2f}s")
            print(f"🎯 Confidence: {data.get('confidence', 0.0):.2f}")
            print(f"📚 Domains: {', '.join(data.get('domains', []))}")
            print(f"🚨 Emergency: {data.get('is_emergency', False)}")
            print(f"📏 Answer Length: {len(data.get('answer', ''))} chars")
            print(f"\n📝 Answer:")
            print("-"*80)
            print(data.get('answer', 'No answer'))
            print("-"*80)
            
            # Verify answer quality
            answer = data.get('answer', '')
            answer_length = len(answer)
            
            if answer_length < 100:
                print("⚠️  WARNING: Answer seems too short!")
            elif answer_length > 200:
                print(f"✅ Good: Answer is detailed ({answer_length} chars)")
            
            # Check for emergency handling
            if "stroke" in test['query'].lower():
                if data.get('is_emergency'):
                    print("✅ Emergency correctly detected")
                    if data.get('confidence', 0) >= 0.4:
                        if "EMERGENCY WARNING" in answer or "call 911" in answer.lower():
                            print("✅ Emergency warning included with AI answer")
                        else:
                            print("⚠️  Emergency warning should be included")
                
        else:
            print(f"❌ ERROR: Status code {response.status_code}")
            print(response.text)
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (>120s)")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
print("Testing Complete")
print("="*80)
print("\n📊 Summary:")
print("- Test 1 should show detailed medical answer (5-6 sentences)")
print("- Test 2 should show emergency warning + AI answer (high confidence)")
print("- Both should have answer length > 200 chars")
print("- Generation parameters: temp=0.7, top_p=0.95, max_new_tokens=300")
