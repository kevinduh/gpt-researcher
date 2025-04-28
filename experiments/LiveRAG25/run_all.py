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


async def get_report(query: str, report_type: str, config_file: str) -> str:

    custom_logs_handler = CustomLogsHandler()
    researcher = GPTResearcher(query, report_type, websocket=custom_logs_handler, config_path=config_file)

    context = await researcher.conduct_research()
    titles = [t for t in context.split('\n') if t.startswith("Title:")]
    report = await researcher.write_report()
    return report, custom_logs_handler.logs, titles


if __name__ == "__main__":

    report_type = "LiveRAG25_report"

    config_file = sys.argv[1]
    output_file = sys.argv[2]
    ddir = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(ddir,"data_morgana_examples.json")) as F:
        data = json.load(F)

    loop = asyncio.get_event_loop()
#    for i, id in enumerate(list(data.keys())[:4]):
    for i, id in enumerate(list(data.keys())):
        print(f"\n============{i}:{id}==============")
        query = data[id]["Question"]
        start_time = time.time()
        report, logs, titles = loop.run_until_complete(get_report(query, report_type, config_file))
 
        elapsed_time = time.time() - start_time
        data[id]["Generation"] = report
        data[id]["Logs"] = logs
        data[id]["Titles"] = titles
        data[id]["Timing"] = str(elapsed_time)
        print(f"----- {report_type} start ----\n{report}\n------ report end ----")


    with open(output_file,'w') as F:
        json.dump(data, F, indent=4)