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
        
import json

@app.route(route="latest", auth_level=func.AuthLevel.ANONYMOUS)
def latest(req: func.HttpRequest) -> func.HttpResponse:
    connection_string = os.environ["AzureWebJobsStorage"]
    service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = service.get_table_client(table_name="CryptoPrices")

    btc_entities = list(table_client.query_entities("PartitionKey eq 'BTC'"))[-10:]
    eth_entities = list(table_client.query_entities("PartitionKey eq 'ETH'"))[-10:]

    def build_summary(items):
        if not items:
            return {"last_price": None, "trend": "brak danych", "count": 0}
        prices = [float(x["price"]) for x in items]
        trend = "bez zmian"
        if len(prices) >= 2:
            if prices[-1] > prices[-2]:
                trend = "wzrost"
            elif prices[-1] < prices[-2]:
                trend = "spadek"
        return {
            "last_price": prices[-1],
            "avg_price": round(sum(prices) / len(prices), 2),
            "trend": trend,
            "count": len(prices),
            "items": [
                {
                    "symbol": x["symbol"],
                    "price": x["price"],
                    "createdAt": x["createdAt"]
                }
                for x in items
            ]
        }

    result = {
        "BTC": build_summary(btc_entities),
        "ETH": build_summary(eth_entities)
    }

    return func.HttpResponse(
        json.dumps(result, ensure_ascii=False),
        mimetype="application/json",
        status_code=200
    )