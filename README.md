# SCALE25gen GPT-Researcher

This project implements report generation using GPT Researcher ([web](https://gptr.dev), [doc](https://docs.gptr.dev), [discord](https://discord.gg/QgZXvJAccX)). 

## Quickstart 

First, install the code in your conda environment (`scale25gptr`):

```bash
git clone https://github.com/kevinduh/gpt-researcher.git
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

The [Tavily](https://tavily.com) key is needed for web search. The [Langchain](https://www.langchain.com) key is needed for Langsmith logging, which is optional but highly recommended. Both have free tiers. The OpenAI key is needed for LLM calls.

Finally, we run a "single" GPT-researcher agent with the example script below. This essentially calls `gpt_researcher.py/agent.py`. As a RAG system, first it calls `conduct_research()` to gather context (relevant documents), then it calls `write_report()` generate the report:

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
* In [2], the Planner decides on the system prompt to use in subsequent calls by asking a LLM (SMART_LLM setting, defaults to openai:gpt-4o-2024-11-20), see `gpt_researcher/actions/agent_creator.py` 
* In [3-4], the Planner searches the web and use it to decide new query reformulations, see `gpt_researcher/prompts.py:generate_search_queries_prompt`. Here it uses the STRATEGIC_LLM setting for the LLM call (defaults to openai:o3-mini). For defaults, see `gpt_researcher/config/variables/default.py`
* Starting with [5], the Researchers will issue new search queries and then compress the returned documents [6]. The retrieval is currently web search by Tavily. After documents are returned, they are filtered or compressed based on word embedding similarity to the query (this requires an embedding model, e.g. openai:text-embedding-3-small). This is to reduce the ultimate context length for RAG.
* [7] shows the final assembled context from multiple search results, and [8] calls GENERATION_LLM to generate the report. For the final prompt, see `gpt_researcher/prompts.py:generate_report_prompt()`.

<div align="center">
<img align="center" height="600" src="https://github.com/assafelovic/gpt-researcher/assets/13554167/4ac896fd-63ab-4b77-9688-ff62aafcc527">
</div>

## Multi-Agent Framework

While the RAG system demonstrated in `tests/test-report.py` is a good start, we are more interested in a multi-agent setup that gives more fine-grained control over the generation process. For this, we will use the code in `multi_agents/`, which uses [LangGraph](https://academy.langchain.com/courses/intro-to-langgraph). The implementation in `gpt_researcher/`) is treated as just one out of many agents, as shown in this conceptual flowchart:

<div align="center">
<img align="center" height="600" src="https://github.com/user-attachments/assets/ef561295-05f4-40a8-a57d-8178be687b18">
</div>
<br clear="all"/>

To try out the multi-agent code, try running:

```bash
python multi_agents/main.py
```

This reads multi_agent/tasks.json and creates the report in `output/run_*`.


## Modifications for SCALE25gen 

The folder `experiments/` contains settings that facilitate specific experiments. 
The `config.*.json` files specify configurations such as which LLM to use. 
The subfolders within `experiments/` contain example scripts that are specific to certain datasets. 

For example: 

```bash
# runs LiveRAG experiment using default OpenAI service
python experiments/LiveRAG25/run1.py experiments/config.openai.default.json

# runs LiveRAG experiment using a local server with Falcon as the generation LLM
python experiments/LiveRAG25/run1.py experiments/config.local.Falcon3-10B-Instruct.json
```

