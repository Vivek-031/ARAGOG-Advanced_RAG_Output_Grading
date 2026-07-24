# ARAGOG - Dual-Mode Intelligent Assistant Guide

## Overview
ARAGOG is an intelligent assistant with dual-mode operation:
- **Medical Mode**: Specialized medical information system using RAG pipeline for healthcare queries
- **General Mode**: General-purpose assistant for non-medical queries (math, algorithms, science, education, etc.)

## Core Behavior

### Medical Mode (Healthcare Queries)
When a query is medical or healthcare-related, ARAGOG activates Medical Mode:
- Uses specialized medical RAG pipeline
- Provides evidence-based medical information
- Includes appropriate medical disclaimers
- Covers: diseases, symptoms, diagnosis, prevention, treatment, management, medical education

### General Mode (Non-Medical Queries)
When a query is NOT medical, ARAGOG activates General Mode:
- Uses general-purpose language model
- Provides clear, helpful answers
- **Does NOT include medical warnings or disclaimers**
- **Does NOT force medical context**
- Covers: math, algorithms, science, technology, education, general knowledge

## Implementation Architecture

### 1. Query Classification
Location: `multi_domains_medical_final_rag_model.py` - `_is_medical_query()` method

**Medical Keywords Categories:**
- General medical terms (disease, symptom, treatment, cure, medicine, etc.)
- Body parts and systems (heart, lung, brain, kidney, etc.)
- Specific conditions (diabetes, cancer, hypertension, etc.)
- Medical specialties (cardiology, neurology, dermatology, etc.)
- Procedures and tests (surgery, x-ray, MRI, blood test, etc.)
- Symptoms (cough, pain, fever, nausea, etc.)
- Prevention and management terms

**Non-Medical Indicators:**
- Entertainment (movies, music, celebrities)
- Sports (football, basketball, championships)
- Politics (elections, government, parties)
- Technology (smartphones, apps, programming)
- General knowledge (geography, history, capitals)

**Medical Context Patterns:**
- Question patterns about diseases, symptoms, treatment
- "How to treat/prevent/cure/manage" patterns
- Medical advice and consultation patterns

### 2. Dual-Mode Pipeline Flow

```
User Query
    ↓
Medical Query Detection (_is_medical_query)
    ↓
    ├─→ Medical: TRUE
    │   ├─→ Use Medical RAG Pipeline
    │   ├─→ Domain Routing
    │   ├─→ Hybrid Retrieval (FAISS + BM25)
    │   ├─→ Reranking
    │   ├─→ Medical Answer Generation
    │   └─→ Return with medical disclaimer
    │
    └─→ Medical: FALSE
        ├─→ Set requires_general_response flag
        ├─→ General Response Generation
        └─→ Return WITHOUT medical disclaimer
```

### 3. Response Structure

#### Medical Mode Response
```json
{
  "query": "What are symptoms of diabetes?",
  "answer": "Detailed medical answer... ⚠️ Please consult a healthcare professional for personalized advice.",
  "domains": ["Diabetes-Digestive-Kidney"],
  "confidence": 0.85,
  "processing_time": 1.23,
  "sources": [...],
  "is_emergency": false,
  "is_medical": true,
  "mode": "medical"
}
```

#### General Mode Response
```json
{
  "query": "What is 25 * 16?",
  "answer": "400",
  "domains": [],
  "confidence": 1.0,
  "processing_time": 0.15,
  "sources": [],
  "is_emergency": false,
  "is_medical": false,
  "mode": "general"
}
```

### 4. Key Differences Between Modes

| Aspect | Medical Mode | General Mode |
|--------|-------------|--------------|
| **Pipeline** | Medical RAG (FAISS + BM25 + Reranker) | General LLM (FLAN-T5) |
| **Data Source** | Medical knowledge bases | Model's general training |
| **Disclaimers** | Yes - healthcare professional consultation | No - direct answer only |
| **Context** | Medical domains and sources | No domain context |
| **Warnings** | Emergency detection, medical advice warnings | None |
| **Response Style** | Detailed, educational, cautious | Concise, direct, helpful |

## Critical Safety Rules

### Medical Mode Safety
1. ✅ Provide factual, evidence-based information only
2. ✅ Avoid hallucinations or unsupported claims
3. ✅ Do NOT provide personal diagnosis
4. ✅ Include appropriate disclaimers
5. ✅ Detect emergency situations
6. ✅ Recommend professional consultation

### General Mode Safety
7. ✅ Answer clearly and accurately
8. ✅ Do NOT add medical warnings to non-medical answers
9. ✅ Do NOT force medical context
10. ✅ Do NOT include "consult a doctor" for math/tech/general queries
11. ✅ Keep responses relevant to the query domain

## Usage Examples

### Medical Mode Queries ✅
```
Query: "What are symptoms of diabetes?"
Response: "Diabetes symptoms include increased thirst, frequent urination, 
extreme hunger, unexplained weight loss, fatigue, blurred vision, slow-healing 
sores, and frequent infections... ⚠️ Please consult a healthcare professional 
for personalized advice."
Mode: Medical
```

```
Query: "How to treat high blood pressure?"
Response: "High blood pressure treatment includes lifestyle modifications and 
medications. Lifestyle changes: reduce sodium intake, maintain healthy weight, 
exercise regularly, limit alcohol, manage stress. Medications may include 
ACE inhibitors, beta-blockers, diuretics... ⚠️ Please consult a healthcare 
professional for personalized advice."
Mode: Medical
```

### General Mode Queries ✅
```
Query: "What is 25 * 16?"
Response: "400"
Mode: General
NO medical warnings ✓
```

```
Query: "Explain quicksort algorithm"
Response: "Quicksort is a divide-and-conquer sorting algorithm. It works by 
selecting a pivot element and partitioning the array around the pivot, placing 
smaller elements before it and larger elements after it. The process is 
recursively applied to the sub-arrays."
Mode: General
NO medical warnings ✓
```

```
Query: "What is the capital of France?"
Response: "Paris"
Mode: General
NO medical warnings ✓
```

```
Query: "How does photosynthesis work?"
Response: "Photosynthesis is the process by which plants convert light energy 
into chemical energy. It occurs in chloroplasts and involves two stages: 
light-dependent reactions (producing ATP and NADPH) and light-independent 
reactions (Calvin cycle, producing glucose)."
Mode: General
NO medical warnings ✓
```

## Testing

### Running Dual-Mode Tests
```bash
cd Backend\Backend
python test_dual_mode.py
```

### Test Coverage
The test validates:
- ✅ 5 medical queries (should use Medical Mode with disclaimers)
- ✅ 7 general queries (should use General Mode WITHOUT disclaimers)

Categories tested:
- **Medical**: Disease symptoms, treatment, causes, emergency, side effects
- **General**: Math, algorithms, geography, biology (non-medical), literature, technology, physics

### Critical Validation Points
1. Medical queries handled correctly with RAG pipeline
2. General queries handled correctly with general LLM
3. **General queries do NOT contain medical disclaimers** (most important)
4. Medical queries include appropriate healthcare disclaimers
5. Mode detection accuracy

## Integration Points

### RAG Pipeline (`multi_domains_medical_final_rag_model.py`)
- `_is_medical_query()`: Classifies queries as medical or general
- `run_query()`: Routes to medical RAG or sets general flag
- Returns `is_medical` and `requires_general_response` flags

### Flask API (`app.py`)
- `generate_general_response()`: Handles general query responses
- `POST /api/ask`: Main endpoint with dual-mode routing
- Checks `requires_general_response` flag
- Routes to appropriate response generation

## System Integrity

### What Was NOT Modified
1. ✅ Medical RAG pipeline logic unchanged
2. ✅ Medical query processing unchanged
3. ✅ Database operations unchanged
4. ✅ Authentication unchanged
5. ✅ Session management unchanged
6. ✅ Medical safety rules unchanged

### What Was Added
1. ✅ General query detection
2. ✅ General response generation function
3. ✅ Dual-mode routing in API
4. ✅ Mode flags in response structure
5. ✅ Test suite for dual-mode behavior

## Conversation & Memory Rules

1. Use ONLY explicitly provided conversation context
2. Do NOT assume or hallucinate past conversations
3. Rely entirely on backend-provided context
4. Each query is evaluated independently
5. Mode detection is per-query, not session-based

## Performance Considerations

### Medical Mode
- Processing time: 1-3 seconds
- Uses: FAISS index + BM25 + Cross-encoder reranking
- Memory: ~2GB (loaded models)

### General Mode
- Processing time: 0.1-0.5 seconds
- Uses: FLAN-T5 base model (already loaded for medical mode)
- Memory: No additional overhead (reuses medical pipeline's model)

## Troubleshooting

### Issue: Medical Query in General Mode
**Symptom**: Medical query receives general response without disclaimer

**Solution**:
1. Add missing medical keywords to `medical_keywords` list
2. Add medical pattern to `medical_patterns` if needed
3. Verify query contains clear medical indicators

### Issue: General Query in Medical Mode
**Symptom**: General query receives medical context or disclaimer

**Solution**:
1. Add topic indicator to `non_medical_indicators` list
2. Verify query doesn't contain ambiguous medical terms
3. Check medical pattern matching

### Issue: General Response Has Medical Disclaimer
**Symptom**: Non-medical answer includes "consult a doctor"

**Solution**:
1. This should NOT happen in the current implementation
2. Check that `generate_general_response()` is being used
3. Verify `mode` field in response is "general"
4. Run test suite to identify issue

## Maintenance

### Adding Medical Keywords
Edit `_is_medical_query()` in `multi_domains_medical_final_rag_model.py`:
```python
medical_keywords = [
    # Add new medical terms here
    "new_medical_term",
]
```

### Adding Non-Medical Indicators
```python
non_medical_indicators = [
    # Add new non-medical indicators here
    "new_topic_indicator",
]
```

### Improving General Responses
Modify `generate_general_response()` in `app.py`:
- Adjust temperature for more creative/conservative responses
- Modify prompt template for better answer quality
- Increase max_new_tokens for longer responses

## Compliance Checklist

- ✅ Medical queries receive specialized medical information
- ✅ General queries receive helpful general responses
- ✅ Medical disclaimers ONLY on medical responses
- ✅ No medical warnings on general responses
- ✅ No forced medical context on non-medical queries
- ✅ Clear mode indication in response
- ✅ Accurate query classification
- ✅ All existing functionality preserved
- ✅ No regression in medical or general capabilities

---

**Version**: 2.0 - Dual Mode
**Last Updated**: December 18, 2024
**Status**: ✅ Fully Implemented and Tested
