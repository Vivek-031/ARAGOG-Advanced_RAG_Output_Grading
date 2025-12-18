# Medical RAG Backend Integration

This document describes the integration of the Medical RAG (Retrieval-Augmented Generation) system into the backend.

## Overview

The Medical RAG system provides intelligent medical question answering using:
- **HyDE (Hypothetical Document Embeddings)**: Generates hypothetical medical answers to improve retrieval
- **Domain Routing**: Automatically routes queries to appropriate medical domains (Cardiology, Dermatology, General)
- **Vector Search**: Uses FAISS for efficient similarity search across medical datasets
- **LLM Reranking**: Uses transformer models to rerank and synthesize final answers

## Architecture

```
Backend/
├── services/
│   └── ragService.py          # Main RAG service implementation
├── scripts/
│   └── run_rag.py             # Bridge script for Node.js integration
├── controllers/
│   └── ragController.js       # Express controller for RAG endpoints
├── routes/
│   └── ragRoutes.js           # API routes for medical queries
├── requirements.txt           # Python dependencies
└── test_rag.js               # Test script for RAG functionality
```

## API Endpoints

### POST /api/rag/ask
Ask a medical question to the RAG system.

**Request Body:**
```json
{
  "query": "What is the best treatment for psoriasis?"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "query": "What is the best treatment for psoriasis?",
    "answer": "Causes:\n- Autoimmune condition...\n\nTreatments:\n- Topical corticosteroids...\n\nFollow-up:\n- Regular dermatologist visits...\n\nSummary:\nPsoriasis treatment involves...",
    "rankedResults": [...],
    "selectedDomain": "dermatology",
    "timestamp": "2024-01-15T10:30:00.000Z"
  }
}
```

### GET /api/rag/health
Check if the medical RAG service is operational.

**Response:**
```json
{
  "success": true,
  "message": "Medical RAG service is operational",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## Setup Instructions

### 1. Install Python Dependencies
```bash
cd Backend
pip install -r requirements.txt
```

### 2. Test the Integration
```bash
# Test the RAG service directly
node test_rag.js

# Or test individual components
python scripts/run_rag.py "What is a headache?"
```

### 3. Start the Backend Server
```bash
npm start
# or
npm run dev
```

## Medical Datasets

The system uses three medical datasets:

1. **Neurology Dataset**: 1,452 Q&A pairs from synthetic neurology dataset
2. **Cardiology Dataset**: 14,885 Q&A pairs from cardiology chatbot data
3. **Dermatology Dataset**: 1,460 Q&A pairs from dermatology fine-tuning dataset

## Domain Routing

The system automatically routes queries to appropriate medical domains based on keyword matching:

- **Cardiology**: Heart disease, cardiovascular, ECG, etc.
- **Dermatology**: Skin conditions, acne, psoriasis, etc.
- **General**: Neurological conditions, general medical queries

## Models Used

1. **Sentence Transformer**: `sentence-transformers/all-MiniLM-L6-v2`
2. **HyDE Model**: `microsoft/BioGPT`
3. **Reranker Model**: `google/flan-t5-large`

## Performance Considerations

- **Initialization Time**: ~2-3 minutes for first load (model downloading and indexing)
- **Query Processing**: ~10-30 seconds per query
- **Memory Usage**: ~4-6GB RAM for all models
- **Timeout**: 5 minutes for query processing

## Error Handling

The system includes comprehensive error handling:
- Input validation and sanitization
- Process timeout protection
- Graceful fallback for model failures
- Detailed error logging

## Security Considerations

- Query sanitization to prevent command injection
- Process isolation for Python execution
- Input validation and length limits
- Error message sanitization

## Troubleshooting

### Common Issues

1. **Python not found**: Ensure Python is installed and in PATH
2. **Model download fails**: Check internet connection and Hugging Face access
3. **Memory errors**: Ensure sufficient RAM (8GB+ recommended)
4. **Timeout errors**: Increase timeout or optimize query complexity

### Debug Mode

Enable debug logging by setting environment variable:
```bash
DEBUG=rag node server.js
```

## Future Enhancements

- [ ] Caching for frequently asked questions
- [ ] Batch processing for multiple queries
- [ ] Model optimization for faster inference
- [ ] Additional medical domains (oncology, pediatrics, etc.)
- [ ] Real-time model updates
- [ ] Advanced filtering and search capabilities
