# ARAGOG Medical - 11-Domain Upgrade Guide

## Configuration Complete ✅

The backend has been successfully updated to support **11 medical domains** instead of 5.

---

## Updated DOMAINS Configuration

The following 11 domains are now configured in `multi_domains_medical_final_rag_model.py`:

### New Domains (6)
1. **general_medical** - General Medical
2. **mental_health** - Mental Health
3. **ophthalmology** - Ophthalmology
4. **pediatrics** - Pediatrics
5. **symptoms_triage** - Symptoms Triage
6. **women_health** - Women Health

### Existing Domains (5)
7. **Cancer** - Cancer Medical QA
8. **Cardiology** - Cardiology Medical QA
9. **Dermatology** - Dermatology Medical QA
10. **Diabetes-Digestive-Kidney** - Diabetes/Digestive/Kidney Medical QA
11. **Neurology** - Neurology Medical QA

---

## Required FAISS Index Files

### ✅ Files Already Available (5 domains)
Located in: `medical_qa_checkpoints/medical_qa_v1.0/faiss_indexes/`

- ✅ `Cancer_index.faiss` + `Cancer_docs.pkl`
- ✅ `Cardiology_index.faiss` + `Cardiology_docs.pkl`
- ✅ `Dermatology_index.faiss` + `Dermatology_docs.pkl`
- ✅ `Diabetes-Digestive-Kidney_index.faiss` + `Diabetes-Digestive-Kidney_docs.pkl`
- ✅ `Neurology_index.faiss` + `Neurology_docs.pkl`

### ❌ Files MISSING (6 domains)
Required location: `medical_qa_checkpoints/`

You need to obtain/create these 12 files:

1. `general_medical_faiss.index`
2. `general_medical_id2doc.pkl`
3. `mental_health_faiss.index`
4. `mental_health_id2doc.pkl`
5. `ophthalmology_faiss.index`
6. `ophthalmology_id2doc.pkl`
7. `pediatrics_faiss.index`
8. `pediatrics_id2doc.pkl`
9. `symptoms_triage_faiss.index`
10. `symptoms_triage_id2doc.pkl`
11. `women_health_faiss.index`
12. `women_health_id2doc.pkl`

---

## How to Obtain Missing Index Files

### Option 1: Download from Kaggle Dataset
If these indexes were created in Kaggle, you need to:
1. Go to your Kaggle notebook output
2. Download the `medical_rag_indexes` folder
3. Extract the 6 new domain files
4. Place them in `Backend\Backend\medical_qa_checkpoints\`

### Option 2: Generate Locally
If you have the source medical datasets, you can generate the indexes:

```python
# Script to create FAISS indexes for each domain
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np

# Load your medical QA dataset
# Example: dataset = load_dataset("your_dataset_name")

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# For each domain:
# 1. Extract Q&A pairs
# 2. Create embeddings
# 3. Build FAISS index
# 4. Save index and id2doc mapping

# Example for general_medical:
documents = [...]  # Your medical documents
embeddings = embedder.encode(documents, convert_to_numpy=True, normalize_embeddings=True)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings.astype('float32'))

# Save
faiss.write_index(index, "medical_qa_checkpoints/general_medical_faiss.index")
with open("medical_qa_checkpoints/general_medical_id2doc.pkl", "wb") as f:
    pickle.dump(documents, f)
```

---

## File Structure

After obtaining all files, your directory should look like:

```
Backend/Backend/
├── medical_qa_checkpoints/
│   ├── general_medical_faiss.index          ← NEW
│   ├── general_medical_id2doc.pkl           ← NEW
│   ├── mental_health_faiss.index            ← NEW
│   ├── mental_health_id2doc.pkl             ← NEW
│   ├── ophthalmology_faiss.index            ← NEW
│   ├── ophthalmology_id2doc.pkl             ← NEW
│   ├── pediatrics_faiss.index               ← NEW
│   ├── pediatrics_id2doc.pkl                ← NEW
│   ├── symptoms_triage_faiss.index          ← NEW
│   ├── symptoms_triage_id2doc.pkl           ← NEW
│   ├── women_health_faiss.index             ← NEW
│   ├── women_health_id2doc.pkl              ← NEW
│   └── medical_qa_v1.0/
│       └── faiss_indexes/
│           ├── Cancer_index.faiss           ✅ EXISTS
│           ├── Cancer_docs.pkl              ✅ EXISTS
│           ├── Cardiology_index.faiss       ✅ EXISTS
│           ├── Cardiology_docs.pkl          ✅ EXISTS
│           ├── Dermatology_index.faiss      ✅ EXISTS
│           ├── Dermatology_docs.pkl         ✅ EXISTS
│           ├── Diabetes-Digestive-Kidney_index.faiss  ✅ EXISTS
│           ├── Diabetes-Digestive-Kidney_docs.pkl     ✅ EXISTS
│           ├── Neurology_index.faiss        ✅ EXISTS
│           └── Neurology_docs.pkl           ✅ EXISTS
├── multi_domains_medical_final_rag_model.py ✅ UPDATED
└── app.py                                    ✅ NO CHANGES NEEDED
```

---

## Updated Domain Routing Keywords

The routing logic now includes keywords for all 11 domains:

- **general_medical**: medical, health, disease, treatment, medication, doctor, hospital, patient
- **mental_health**: mental, depression, anxiety, stress, psychiatric, therapy, counseling, mood
- **ophthalmology**: eye, vision, sight, blind, cataract, glaucoma, retina, optical
- **pediatrics**: child, baby, infant, pediatric, newborn, toddler, adolescent, kid
- **symptoms_triage**: symptom, pain, fever, emergency, urgent, acute, sudden, severe
- **women_health**: women, pregnancy, menstrual, gynecology, obstetric, breast, ovarian, uterus
- **Cancer**: cancer, tumor, chemotherapy, oncology, malignant, metastasis, radiation
- **Cardiology**: heart, cardiac, blood pressure, artery, cardiovascular, chest pain, hypertension
- **Dermatology**: skin, rash, eczema, acne, dermatitis, psoriasis, melanoma
- **Diabetes-Digestive-Kidney**: diabetes, kidney, digestive, stomach, liver, insulin, pancreas, bowel
- **Neurology**: brain, headache, migraine, seizure, neurological, nervous, stroke, alzheimer

Default domain if no match: **general_medical** (changed from "Cardiology")

---

## Starting the Backend

### Partial Mode (5 domains only)
If you **don't have the 6 new index files yet**, the backend will:
- Load the 5 existing domains successfully
- Skip the 6 missing domains (with error messages in logs)
- Still function but with limited domain coverage

```bash
cd Backend\Backend
python app.py
```

Expected startup log (partial mode):
```
================================================================================
*** INITIALIZING OPTIMIZED MEDICAL RAG PIPELINE ***
================================================================================

⚡ Preloading all domain indexes for faster responses...
  📂 Loading general_medical index...
    ❌ Failed to load general_medical: [Errno 2] No such file or directory
  📂 Loading mental_health index...
    ❌ Failed to load mental_health: [Errno 2] No such file or directory
  ...
  📂 Loading Cancer index...
    ✅ Loaded 15234 chunks
  📂 Loading Cardiology index...
    ✅ Loaded 45678 chunks
  ...
================================================================================
[OK] MEDICAL RAG PIPELINE READY!
Available Domains: 5 (out of 11 configured)
Memory-optimized mode active
================================================================================
```

### Full Mode (11 domains)
After obtaining all 6 missing index files:

Expected startup log (full mode):
```
================================================================================
*** INITIALIZING OPTIMIZED MEDICAL RAG PIPELINE ***
================================================================================

⚡ Preloading all domain indexes for faster responses...
  📂 Loading general_medical index...
    ✅ Loaded 710919 chunks
  📂 Loading mental_health index...
    ✅ Loaded 22565 chunks
  📂 Loading ophthalmology index...
    ✅ Loaded 57979 chunks
  📂 Loading pediatrics index...
    ✅ Loaded 19888 chunks
  📂 Loading symptoms_triage index...
    ✅ Loaded 147907 chunks
  📂 Loading women_health index...
    ✅ Loaded 35421 chunks
  📂 Loading Cancer index...
    ✅ Loaded 15234 chunks
  📂 Loading Cardiology index...
    ✅ Loaded 45678 chunks
  📂 Loading Dermatology index...
    ✅ Loaded 12345 chunks
  📂 Loading Diabetes-Digestive-Kidney index...
    ✅ Loaded 23456 chunks
  📂 Loading Neurology index...
    ✅ Loaded 10234 chunks
✅ All domain indexes preloaded.
================================================================================
[OK] MEDICAL RAG PIPELINE READY!
Available Domains: 11
Memory-optimized mode active
================================================================================
```

---

## Verification Commands

### Check Configuration
```bash
python -c "from multi_domains_medical_final_rag_model import DOMAINS; print(f'Total domains: {len(DOMAINS)}'); [print(f'  {i+1}. {d.name}') for i, d in enumerate(DOMAINS)]"
```

Expected output:
```
Total domains: 11
  1. general_medical
  2. mental_health
  3. ophthalmology
  4. pediatrics
  5. symptoms_triage
  6. women_health
  7. Cancer
  8. Cardiology
  9. Dermatology
  10. Diabetes-Digestive-Kidney
  11. Neurology
```

### Check Available Domains API
```bash
curl http://localhost:5000/api/domains
```

Expected response:
```json
{
  "domains": [
    {"name": "general_medical", "dataset": "General Medical", "has_index": true/false},
    {"name": "mental_health", "dataset": "Mental Health", "has_index": true/false},
    ...
  ],
  "total": 11
}
```

### Test Query
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What are symptoms of depression?", "user_id": 1, "session_id": "test_123"}'
```

Expected: Routes to **mental_health** domain

---

## Code Changes Summary

### File: `multi_domains_medical_final_rag_model.py`

#### Change 1: DOMAINS Configuration (Lines 54-88)
**Before:** 5 domains
**After:** 11 domains (6 new + 5 existing)

#### Change 2: Domain Routing Keywords (Lines 295-320)
**Before:** 5 domain keywords
**After:** 11 domain keywords with comprehensive coverage

#### Change 3: Default Fallback Domain (Line 318)
**Before:** `["Cardiology"]`
**After:** `["general_medical"]`

### File: `app.py`
**No changes required** - Already imports `DOMAINS` correctly

---

## Memory Optimization Settings

The configuration uses CPU-friendly models:
- **Embedder**: `sentence-transformers/all-MiniLM-L6-v2` (80MB)
- **Reranker**: `BAAI/bge-reranker-base` (300MB)
- **Generator**: `google/flan-t5-base` (900MB)
- **Device**: CPU (set in `multi_domains_medical_final_rag_model.py:30`)

Total RAM usage: ~6-7GB during query processing

---

## Testing Checklist

After obtaining all index files:

- [ ] Backend starts without errors
- [ ] Logs show "Available Domains: 11"
- [ ] All 11 domains load successfully
- [ ] `/api/health` returns `available_domains: 11`
- [ ] `/api/domains` returns all 11 domains
- [ ] Medical queries route to correct domains
- [ ] General medical queries use `general_medical` domain
- [ ] Mental health queries use `mental_health` domain
- [ ] Pediatric queries use `pediatrics` domain
- [ ] Women's health queries use `women_health` domain
- [ ] Emergency queries use `symptoms_triage` domain
- [ ] Chat history still saves correctly
- [ ] Authentication endpoints work unchanged

---

## Rollback Instructions

If you need to revert to the 5-domain setup:

```bash
cd Backend\Backend
git checkout multi_domains_medical_final_rag_model.py
python app.py
```

Or manually restore the original DOMAINS list from lines 54-70.

---

## Next Steps

1. **Obtain the 6 missing FAISS index files** (see "How to Obtain Missing Index Files" section)
2. **Place files in correct directory** (`medical_qa_checkpoints/`)
3. **Start the backend**: `python app.py`
4. **Verify logs show all 11 domains loading**
5. **Test with queries from different medical domains**
6. **Monitor memory usage** (should stay under 7GB)

---

## Support

If domains fail to load:
- Check file paths are correct
- Verify `.faiss` and `.pkl` files exist in pairs
- Check file permissions
- Review backend startup logs for specific errors
- Ensure files are not corrupted (try re-downloading)

**Configuration Status**: ✅ Code Updated | ⏳ Awaiting Index Files

**Last Updated**: December 18, 2024
