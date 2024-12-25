from typing_extensions import Literal

Side = Literal['BUY', 'SELL']
TimeInForce = Literal['GTC', 'IOC', 'FOK']
OrderStatus = Literal['NEW', 'PARTIALLY_FILLED', 'FILLED', 'CANCELED', 'PENDING_CANCEL', 'REJECTED', 'EXPIRED']
OrderType = Literal['LIMIT', 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT', 'LIMIT_MAKER']

ListStatusType = Literal['EXEC_STARTED', 'ALL_DONE', 'REJECTED']
ListOrderStatus = Literal['EXECUTING', 'ALL_DONE', 'REJECTED']