from gpt_researcher import GPTResearcher
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()
import logging
import sys
import json
import os
import time

class CustomLogsHandler:
    """A custom Logs handler class to handle JSON data."""
    def __init__(self):
        self.logs = []  # Initialize logs to store data

    async def send_json(self, data: Dict[str, Any]) -> None:
        """Send JSON data and log it."""
        if data['type'] == 'logs':
            self.logs.append(data)  # Append data to logs


def extract_titles_passages(context):
    passages = []
    for item in context.replace('\n',' ').split('Source:'):
        fields = item.split('Content:')
        if len(fields) == 2:
            title = fields[0].strip().split('Title: ')[1]
            passage = fields[1].strip()
            passages.append({'doc_IDs':[title], 'passage':passage})
    return passages


async def get_report(query: str, report_type: str, config_file: str) -> str:

    custom_logs_handler = CustomLogsHandler()
    researcher = GPTResearcher(query, report_type, websocket=custom_logs_handler, config_path=config_file)

    context = await researcher.conduct_research()
    passages = extract_titles_passages(context)
    report = await researcher.write_report()
    return report, custom_logs_handler.logs, passages, context


if __name__ == "__main__":

    report_type = "LiveRAG25_report"

    config_file = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    ddir = os.path.dirname(os.path.realpath(__file__))

    data = []
    with open(input_file) as F:
        for line in F:
            data.append(json.loads(line))

    with open(output_file,'w') as OUT:
        loop = asyncio.get_event_loop()
        for i, d in enumerate(data[:2]):
            print(f"\n============{i}:{d['id']}==============")
            query = d["question"]
            start_time = time.time()
            report, logs, passages, context = loop.run_until_complete(get_report(query, report_type, config_file))
            
            elapsed_time = time.time() - start_time
            print(f"----- {report_type} start ----\n{report}\n------ report end ----")
            print(f"\n========== {elapsed_time} seconds=========")

            d['passages'] = passages
            total_words = 200
            d['final_prompt'] = f"""
Information: "{context}"
---
Using the above information, answer the following query or task: "{query}" in one or two sentences.
Use at most {total_words} words.
"""
            d['answer'] = report

            print(json.dumps(d))
            OUT.write(json.dumps(d)+'\n')
