# CREW AI WORKFLOW
from crewai import Agent, Task, LLM, Crew
import os

class ReportGenerator:
    def __init__(self, data: list, output_dir: str, llm_model: str, llm_api_key: str):
        self.data = data
        self.output_dir = output_dir
        self.llm_model = llm_model
        if llm_api_key is not None and llm_model.startswith("gpt"):
            os.environ["OPENAI_API_KEY"] = llm_api_key
        else:
            print("Please ensure you provide an OpenAI API key and valid GPT Model.")
            
    def generate_report(self):
        """Generate Report using LLM Model"""
        # Initialize LLM
        llm = LLM(model=self.llm_model)
        # Initialize Agent
        report_agent = Agent(
            role = "Cloud Cost Analyst",
            goal = "Analyze given Azure Billing info and Generate a Report to provide insights and actionable advice.",
            backstory = "You are an expert in Cloud Costs and have long experience in optimizing cloud costs for various organizations.",
            llm = llm
        )
        # Define Task
        report_task = Task(
            description = f'''Generate a detailed report based on the given Azure Billing data defined here:
            {self.data}
            The data is given as a CSV format with the column names first followed by data. Identify trends, anomalies, and provide actionable advice to optimize costs.''',
            expected_output = "A detailed report in an organized format that includes various types of reports such as insights, trends, anomalies, and recommendations.",
            name = "Report Task",
            output_file = self.output_dir,
            agent = report_agent
        )
        # Initialize Crew
        crew = Crew(
            agents = [report_agent],
            tasks = [report_task],
            verbose = True
        )
        output = crew.kickoff()
        return output
        