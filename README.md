# SCALE25gen GPT-Researcherr

This project implements report generation using GPT Researcher ([web](https://gptr.dev), [doc](https://docs.gptr.dev), [discord](https://discord.gg/QgZXvJAccX)). 

## Quickstart

First, install the code in your conda environment (`scale25gptr`):

```bash
git clone //github.com/kevinduh/gpt-researcher.git
cd gpt-researcher
conda env create -f conda_env.yaml
conda activate scale25gptr
pip install -e .
```

Next, set up `.env` file in the root directory. This contains API keys (which should be kept secret). Here is an example:

```bash
OPENAI_API_KEY=<your_key>
TAVILY_API_KEY=<your_key>
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=<your_key>
```

The Tavily key is needed for web search. The Langc using a "single" GPT-researcher agent. This essentially calls `gpt_researcher.py/agent.py`. As a RAG system, first it calls `conduct_research()` to gather context (relevant documents), then it calls `write_report()` generate the report:

```bash
python tests/test-report.py

(example output snippet) 
[1] Starting the research task for 'I need a report on China's ban on the import of lumber from Australia, which started in 2020.  I am particularly interested in the reasons for the ban, including both the stated reasons and any available speculation or information about unstated reasons for the ban'...
[2] Geopolitics Agent
[3] Browsing the web to learn more about the task
[4] I will conduct my research based on the following queries: ['China 2020 ban on Australian timber imports: report on official reasons (pests, quarantine issues) and underlying trade dispute factors', "Analysis of China's 2020 import ban on Australian lumber:...
[5] Running research for 'China 2020 ban on Australian timber imports: report on official reasons (pests, quarantine issues) and underlying trade dispute factors'...
[6] Getting relevant content based on query...
[7] ... Context ...
[8] Writing report for ...
```

Let's explain what went on with the following conceptual flowchart, cross-referencing with the example output snippet: 
* The user's query is shown in [1] 
* In [2], the Planner decides on the "agent" system prompt using a LLM call (SMART_LLM setting, defaults to openai:gpt-4o-2024-11-20), see `gpt_researcher/actions/agent_creator.py` 
* In [3-4], the Planner searches the web and use it to decide new query reformulations, see `gpt_researcher/prompts.py:generate_search_queries_prompt`. Here it uses the STRATEGIC_LLM setting (defaults to openai:o3-mini). For defaults, see `gpt_researcher/config/variables/default.py`
* Starting with [5], the Researchers will issue new search queries and then compress the returned documents [6]. The compression is currently implemented as an Embedding based filter (if similarity of a retrieved document chunk embedding is not close to the query embedding, then it is deleted). This is to reduce the ultimate context length for RAG.
* [7] shows the final assembled context from multiple search results, and [8] calls SMART_LLM to generate the report. For the final prompt, see `gpt_researcher/prompts.py:generate_report_prompt()`.

<div align="center">
<img align="center" height="600" src="https://github.com/assafelovic/gpt-researcher/assets/13554167/4ac896fd-63ab-4b77-9688-ff62aafcc527">
</div>


