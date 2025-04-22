from gpt_researcher import GPTResearcher
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()
import logging
import sys

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
    print(f"===== context start =====\n{context}\n===== context end =====")

    report = await researcher.write_report()
    print(f"+++ log start +++\n{custom_logs_handler.logs}\n+++ log end +++")
    return report

if __name__ == "__main__":
    #query = "I need a report on China's ban on the import of lumber from Australia, which started in 2020.  I am particularly interested in the reasons for the ban, including both the stated reasons and any available speculation or information about unstated reasons for the ban"
    query = "I enjoy having drinks with friends but hate leaving my dog at home. Are there any establishments in Cleveland that welcome dogs while serving drinks?"

    #report_type = "SCALE25_report"
    report_type = "LiveRAG25_report"

    config_file = sys.argv[1]
    report = asyncio.run(get_report(query, report_type, config_file))
    print(f"----- {report_type} start ----\n{report}\n------ report end ----")
