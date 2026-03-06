import azure.functions as func
from azure.data.tables import TableServiceClient
from datetime import datetime, timezone
import requests
import os

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */30 * * * *", arg_name="mytimer", run_on_startup=False, use_monitor=True)
def crypto_timer(mytimer: func.TimerRequest) -> None:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(url, timeout=20)
    data = response.json()

    connection_string = os.environ["AzureWebJobsStorage"]
    service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = service.get_table_client(table_name="CryptoPrices")

    now = datetime.now(timezone.utc)
    timestamp = now.isoformat()

    entities = [
        {
            "PartitionKey": "BTC",
            "RowKey": timestamp,
            "symbol": "BTC",
            "price": float(data["bitcoin"]["usd"]),
            "createdAt": timestamp
        },
        {
            "PartitionKey": "ETH",
            "RowKey": timestamp + "-ETH",
            "symbol": "ETH",
            "price": float(data["ethereum"]["usd"]),
            "createdAt": timestamp
        }
    ]

    for entity in entities:
        table_client.upsert_entity(entity)