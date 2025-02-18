from azure.identity import ClientSecretCredential
import requests
import datetime

class AzureConnector:
    def __init__(self, tenant_id, client_id, client_secret, subscription_id, time_from: str, time_to: str):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.subscription_id = subscription_id
        self.time_from = time_from
        self.time_to = time_to
        self.credential = None

    def authenticate(self):
        """Authenticate with Azure using service principal credentials."""
        self.credential = ClientSecretCredential(
            self.tenant_id, self.client_id, self.client_secret
        )
        #self.client = ResourceManagementClient(self.credential, self.subscription_id)
        print("Authenticated successfully")

    def get_subscription_cost_data_from(self):
        """Fetch Subscription Data"""
        token = self.credential.get_token("https://management.azure.com/.default").token
        url = f"https://management.azure.com/subscriptions/{self.subscription_id}/providers/Microsoft.CostManagement/query?api-version=2023-03-01"
        # Get current date in ISO format
        current_date = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        # Query payload (adjust timeframe as needed)
        payload = {
            "type": "ActualCost",
            "timeframe": "Custom",
            "timePeriod": {
                "from": self.time_from,
                "to": current_date
            },
            "dataset": {
                "granularity": "Daily",
                "aggregation": {
                    "totalCost": {
                        "name": "PreTaxCost",
                        "function": "Sum"
                    }
                }
            }
        }
        # Header to define token and content type
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # Make API request
        response = requests.post(url, json=payload, headers=headers)
        
        # Package export data to List for CSV format
        if response.status_code == 200:
            columns = [col["name"] for col in response.json()["properties"]["columns"]]
            rows = response.json()["properties"]["rows"]
            # Reformat dates in rows
            for row in rows:
                row[1] = datetime.datetime.strptime(str(row[1]), "%Y%m%d").strftime("%Y-%m-%d")
            return [columns] + rows
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        
    def get_subscription_cost_data_from_to(self):
        """Fetch Subscription Data"""
        token = self.credential.get_token("https://management.azure.com/.default").token
        url = f"https://management.azure.com/subscriptions/{self.subscription_id}/providers/Microsoft.CostManagement/query?api-version=2023-03-01"
        # Query payload (adjust timeframe as needed)
        payload = {
            "type": "ActualCost",
            "timeframe": "Custom",
            "timePeriod": {
                "from": self.time_from,
                "to": self.time_to
            },
            "dataset": {
                "granularity": "Daily",
                "aggregation": {
                    "totalCost": {
                        "name": "PreTaxCost",
                        "function": "Sum"
                    }
                }
            }
        }
        # Header to define token and content type
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # Make API request
        response = requests.post(url, json=payload, headers=headers)
        
        # Package export data to List for CSV format
        if response.status_code == 200:
            columns = [col["name"] for col in response.json()["properties"]["columns"]]
            rows = response.json()["properties"]["rows"]
            # Reformat dates in rows
            for row in rows:
                row[1] = datetime.datetime.strptime(str(row[1]), "%Y%m%d").strftime("%Y-%m-%d")
            return [columns] + rows
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None