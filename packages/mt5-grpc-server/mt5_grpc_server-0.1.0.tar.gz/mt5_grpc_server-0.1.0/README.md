# MT5 gRPC Server

A high-performance gRPC server implementation for MetaTrader 5, enabling remote trading operations and market data access.

## Overview
This module provides a gRPC server that interfaces with MetaTrader 5 terminal, allowing remote access to trading operations, market data, and account management through a standardized gRPC API.

## Installation

```bash
pip install mt5-grpc-server
```

## Features

- **Account Operations**
  - Account info retrieval
  - Balance and equity monitoring
  - Trading history access

- **Trading Operations**
  - Order placement and modification
  - Position management
  - Order validation and calculations

- **Market Data**
  - Real-time price data
  - Symbol information
  - Market depth (DOM)


## Usage

### Starting the Server

Example with secure connection:
```bash
mt5-grpc-server --host 127.0.0.1 --port 50052 --secure --cert-file server.crt --private-key-file server.key
```

Or without secure connection:
```bash
# Default port is 50051 and host is 0.0.0.0
mt5-grpc-server 
```


### Command-line Options

The server supports the following command-line options:

- `--host HOST`: Host address to bind the server to (default: "0.0.0.0")
- `--port PORT`: Port number to listen on (default: 50051)
- `--secure`: Enable secure connection with SSL/TLS
- `--cert-file FILE`: Path to the SSL certificate file (required if --secure is used)
- `--private-key-file FILE`: Path to the private key file (required if --secure is used)
