# Binance

## Installation

```bash
pip install binance-python
```

## Usage

### Public API

```python
from binance import Public

client = Public()
await client.candles('BTCUSDT', interval='1m', limit=4)
# [Candle(open_time=datetime(...), close_time=datetime(...), open=Decimal('93970.04000000'), ...), ...]
```

### Private API

```python
from binance import Binance

client = Binance(API_KEY, API_SECRET)
# or client = Binance.env() to load `API_KEY` and `API_SECRET` from environment variables or a .env file

await client.spot_order('BTCUSDT', {
  'price', 10000, ... # let the type hints guide you
})
```

### Context Manager

To run multiple requests concurrently, I'd recommend using the client as a context manager:

```python
from binance import Binance

client = Binance(API_KEY, API_SECRET)

async with client:
  await client.spot_order('BTCUSDT', {
    'price', 10000, ...
  })
  await client.spot_order('ETHUSDT', {
    'price', 2000, ...
  })
```