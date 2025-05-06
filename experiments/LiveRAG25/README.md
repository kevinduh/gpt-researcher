# LiveRAG 2025 Challenge

To replicate our experiments for the LiveRAG 2025 Challenge, first install this repo following the [instructions](../../README.md).

Then, we set up two servers and point to them in `experiments/config.local.Falcon3-10B-Instruct.json`:
- Retriever: PLAID search service for the document collection
- Generation LLM: Falcon3-10B Instruct LLM, served by llama.cpp

We also set up services to together.ai for:
- Query reformulation (STRATEGIC_LLM): Qwen/Qwen2.5-7B-Instruct-Turbo
- Passage filtering for compressed context (EMBEDDING): m2-bert-80M-8k-retrieval

Our `.env` looks like:

```(bash)
TOGETHER_API_KEY=<your_key>
LANGCHAIN_TRACING_V2=false
```

Finally, we run: 

```(bash)
cd repo/root/dir
python experiments/LiveRAG25/run_all2.py experiments/config.local.Falcon3-10B-Instruct.json input.jsonl output.jsonl
```
