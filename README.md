# Crypto Monitor (Azure)

## Overview

This project is a simple cryptocurrency monitoring system built using Microsoft Azure.  
The application periodically retrieves cryptocurrency prices from a public API, stores the data in Azure Table Storage, and exposes the results through an HTTP API.

The collected data can also be visualized in a web browser using a chart.

The goal of the project is to demonstrate how multiple Azure services can work together in a serverless cloud architecture.

---

## Architecture

The application works in the following workflow:

Timer Trigger (Azure Function)  
→ Fetch cryptocurrency prices from external API  
→ Store data in Azure Table Storage  
→ HTTP Trigger exposes the data through API  
→ Web page visualizes the data using Chart.js

---

## Azure Services Used

The project uses the following Azure services:

- **Azure Functions** – serverless compute service
- **Timer Trigger** – periodically fetches cryptocurrency prices
- **HTTP Trigger** – exposes stored data through a REST API
- **Azure Storage Account (Table Storage)** – stores cryptocurrency price records

---

## Technologies

- Microsoft Azure
- Azure Functions (Python)
- Azure Table Storage
- REST API
- HTML / JavaScript
- Chart.js

---

## Example API Response

```json
{
  "BTC": {
    "last_price": 68216.0,
    "avg_price": 68203.0,
    "trend": "increase",
    "count": 5
  },
  "ETH": {
    "last_price": 1986.14,
    "avg_price": 1985.53,
    "trend": "increase",
    "count": 5
  }
}
```
---
## Visualization

A simple web page retrieves data from the Azure Function API and visualizes cryptocurrency prices using Chart.js.

## Author

Jan Weis
GitHub: https://github.com/Weisjan
