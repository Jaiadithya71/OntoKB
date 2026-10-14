# URGENT: Production Fast Path Activation Hotfix

**Issue**: Fast path optimizations are not being activated. Queries still take 30-60s.

**Root Cause**: 
1. Fast path confidence threshold too high (12 → lowered to 5)
2. Procedural pattern too aggressive (blocks queries)
3. Evidence extraction still running for non-procedural queries

**Solution**: Set these environment variables IMMEDIATELY:

```bash
# FORCE fast path activation
export RAG_FAST_PATH_ENABLED=1

# DISABLE evidence extraction (use direct generation)
export RAG_EVIDENCE_EXTRACTION_ENABLED=0

# LOWER confidence threshold
export RAG_FAST_PATH_MIN_CONFIDENCE=0

# USE fast models
export RAG_USE_FAST_MODEL_FOR_FACTUAL=1
export RAG_LLM_REASONING_ENABLED_FOR_COMPLEX=0  # Disable reasoning
```

**Expected Results**:
- TTFT: 24s → 2-5s (5-10x faster)
- Total: 30-63s → 5-15s
- Direct generation without evidence extraction

**Deployment Steps**:

1. **Staging** (Test first):
```bash
cd /home/qabot/hrbot/api
export RAG_EVIDENCE_EXTRACTION_ENABLED=0
export RAG_FAST_PATH_MIN_CONFIDENCE=0
npm start
# Test queries: measure latency
```

2. **Production** (Once confirmed):
```bash
# Update environment in deployment/docker/kubernetes/systemd
export RAG_EVIDENCE_EXTRACTION_ENABLED=0
export RAG_FAST_PATH_MIN_CONFIDENCE=0
systemctl restart hrbot-api  # or equivalent
```

3. **Verify**:
- Simple query latency < 10s
- TTFT < 5s
- No evidence extraction logs

**If Problems Occur**:
- Revert: `RAG_EVIDENCE_EXTRACTION_ENABLED=1`
- Increase threshold: `RAG_FAST_PATH_MIN_CONFIDENCE=10`
- Enable reasoning: `RAG_LLM_REASONING_ENABLED_FOR_COMPLEX=1`

**Code Changes Made**:
- ✅ Lowered RAG_FAST_PATH_MIN_CONFIDENCE: 12 → 5
- ✅ Relaxed PROCEDURAL pattern (less aggressive)
- ✅ Removed query type restriction from fast path
- ✅ Fast path now activates for ALL non-procedural queries
