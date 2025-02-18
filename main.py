from azure_report_tool.azure_extractor import AzureConnector
from azure_report_tool.report_generator import ReportGenerator
import datetime
import os
current_date = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
date_60_days_ago = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=60)).strftime("%Y-%m-%dT%H:%M:%SZ")
date_3_days_ago = (datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")

client_secret = os.getenv("CLIENT_SECRET")
llm_api_key = os.getenv("LLM_API_KEY")

test = AzureConnector(
    tenant_id="b0f5bbda-5dc8-4ac8-8621-fb81b23db439",
    client_id="0b240cb1-61d1-4fb5-bb53-b8190263bbdf",
    client_secret=client_secret,
    subscription_id="87eb1361-d59d-47b3-a050-3fb90ffebd63",
    time_from=date_60_days_ago,
    time_to=date_3_days_ago
)
# Authenticate with Azure
test.authenticate()
# Fetch Subscription Data
data_from = test.get_subscription_cost_data_from()

report = ReportGenerator(
    data=data_from,
    output_dir="output/report.md",
    llm_model="gpt-4o-mini-2024-07-18",
    llm_api_key=llm_api_key
)
# Generate Report
out_report = report.generate_report()