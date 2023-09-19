const WebSocket = require('ws');
let ws;
let wsIsAlive = false;
let isReconnecting = false;
let pingSent = false;
let connectionEstablished = false;
let connectionTimer;
let isConnecting = false;

function connectWebSocket() {
  if (isReconnecting) {
    return;
  }
  isReconnecting = true;

  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.terminate();
  }

  // Binance WebSocket connection for BTC/USDT spot market trades
  ws = new WebSocket('wss://stream.binance.com:9443/ws/ethusdt@trade');

  isConnecting = true;
  ws.on('open', () => {
    console.log('WebSocket connection opened.');
    wsIsAlive = true;
    isReconnecting = false;
    isConnecting = false;
    connectionEstablished = true;
    ws.ping();
  });

  ws.on('pong', () => {
    wsIsAlive = true;
    pingSent = false;
  });

  ws.on('message', (data) => {
    const jsonData = JSON.parse(data);
    console.log('Received data:', jsonData);
  });

  ws.on('close', () => {
    console.log('WebSocket connection closed');
    isReconnecting = false;

    if (!connectionEstablished) {
      console.log('WebSocket was closed before the connection was established');
      connectWebSocket();
    }

    connectionEstablished = false;
    clearTimeout(connectionTimer);
  });

  ws.on('error', (error) => {
    console.error('WebSocket encountered error: ', error);
    ws.close();
  });

  connectionTimer = setTimeout(() => {
    if (isConnecting) {
      console.log('WebSocket was closed before the connection was established');
      connectWebSocket();
    }
  }, 5000);
}

// Start the WebSocket connection
connectWebSocket();

setInterval(() => {
  if (wsIsAlive === false && !isReconnecting && !isConnecting) {
    console.log('Websocket connection lost. Reconnecting...');
    connectWebSocket();
  }

  wsIsAlive = false;

  if (ws.readyState === WebSocket.OPEN) {
    ws.ping();
    pingSent = true;
  }
}, 1000);
