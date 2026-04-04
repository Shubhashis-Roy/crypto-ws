# Crypto Price WebSocket Project

## Features

- Real-time crypto price streaming (BTC/USDT, ETH/USDT, BNB/USDT)
- WebSocket broadcasting to multiple clients
- Async architecture using FastAPI
- Dockerized setup
- Deployed on Render

---

## Architecture

```
Binance WebSocket → Listener → Async Queue → Consumer → WebSocket Server → Clients
```

---

## Hosted Deployment (Render)

**Base URL:**
https://crypto-ws-c4kn.onrender.com/

### Test WebSocket (Production)

Open browser → DevTools → Console:

```javascript
const ws = new WebSocket("wss://crypto-ws-c4kn.onrender.com/ws");

ws.onmessage = (event) => {
  console.log(JSON.parse(event.data));
};
```

You should see live crypto price updates in real-time.

---

## Run Locally (Without Docker)

### 1. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Server

```bash
uvicorn app.main:app --reload
```

### 4. Test WebSocket

Open browser console and run:

```javascript
const ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.onmessage = (event) => {
  console.log(JSON.parse(event.data));
};
```

---

## Run with Docker

### Build Image

```bash
docker build -t fastapi-app .
```

### Run Container

```bash
docker run -p 8000:8000 fastapi-app
```

---

## API

```id="k9d2sx"
GET /price
```

Returns latest prices for all symbols (JSON)

```id="v3m8qp"
GET /price/{symbol}
```

Example:

```id="y7n4bc"
GET /price/ETHUSDT
```

Returns latest price data for the given symbol only

---

## Notes

- Uses asyncio for concurrency
- Handles Binance WebSocket reconnections
- Supports multiple trading pairs
- Designed for real-time streaming

---

## Tech Stack

- FastAPI
- WebSockets (asyncio)
- Docker
- Render

---

## Author

Shubhashis Roy
shubhashisroy360@gmail.com
