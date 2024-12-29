from typing_extensions import Literal, overload, TypeVar
from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel, ValidationError
import orjson
from .user import UserMixin
from .util import binance_timestamp
from .types import OrderStatus, Error, ErrorRoot, Order, ListStatusType, ListOrderStatus

T = TypeVar('T')
M = TypeVar('M', bound=BaseModel)

ReplaceMode = Literal['STOP_ON_FAILURE', 'ALLOW_FAILURE']

class Fill(BaseModel):
  price: str
  qty: str
  commission: str
  commissionAsset: str

class OrderResponse(BaseModel):
  orderId: int
  status: OrderStatus
  price: str
  fills: list[Fill] = []
  code: Literal[None] = None

class PartialOrder(BaseModel):
  symbol: str
  orderId: int

class ListOrderResponse(BaseModel):
  orderListId: int
  listStatusType: ListStatusType
  listOrderStatus: ListOrderStatus
  code: Literal[None] = None
  orders: list[PartialOrder]

class CancelOrderResponse(BaseModel):
  code: Literal[None] = None

def validate_response(r: str, Model: type[M]) -> M | Error:
  obj = orjson.loads(r)
  try:
    if 'code' in obj:
      return ErrorRoot.model_validate(obj).root
    return Model.model_validate(obj)
  except ValidationError as e:
    print('Error validating:', obj)
    raise e

@dataclass
class Spot(UserMixin):
  api_key: str
  api_secret: str
  base: str = 'https://api.binance.com'

  @overload
  async def query_order(self, symbol: str, orderId: int, recvWindow: int = 5000, *, unsafe: Literal[False] = False) -> OrderResponse | Error:
    ...
  @overload
  async def query_order(self, symbol: str, orderId: int, recvWindow: int = 5000, *, unsafe: Literal[True]) -> OrderResponse:
    ...
  @UserMixin.with_client
  async def query_order(self, symbol: str, orderId: int, recvWindow: int = 5000, *, unsafe: bool = False) -> OrderResponse | Error:
    query = self.signed_query({
      'symbol': symbol,
      'orderId': orderId,
      'timestamp': binance_timestamp(datetime.now()),
      'recvWindow': recvWindow,
    })
    r = await self.client.get(
      f'{self.base}/api/v3/order?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    val = validate_response(r.text, OrderResponse)
    if unsafe and val.code is not None:
      raise RuntimeError(f'Error fetching order: {val.code}, {val.msg}')
    return val
  
  @UserMixin.with_client
  async def query_order_list(self, orderListId: int, recvWindow: int = 5000) -> ListOrderResponse | Error:
    query = self.signed_query({
      'orderListId': orderListId,
      'timestamp': binance_timestamp(datetime.now()),
      'recvWindow': recvWindow,
    })
    r = await self.client.get(
      f'{self.base}/api/v3/orderList?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return validate_response(r.text, ListOrderResponse)

  @overload
  async def spot_order(self, pair: str, order: Order, *, unsafe: Literal[False] = False) -> OrderResponse | Error:
    ...
  @overload
  async def spot_order(self, pair: str, order: Order, *, unsafe: Literal[True]) -> OrderResponse:
    ...
  @UserMixin.with_client
  async def spot_order(self, pair: str, order: Order, *, unsafe: bool = False) -> OrderResponse | Error:
    query = self.signed_query({
      'symbol': pair,
      'timestamp': binance_timestamp(datetime.now()),
      'newOrderRespType': 'FULL',
      **order,
    })
    r = await self.client.post(
      f'{self.base}/api/v3/order?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    val = validate_response(r.text, OrderResponse)
    if unsafe and val.code is not None:
      raise RuntimeError(f'Error creating order: {val.code}, {val.msg}')
    return val
  

  @overload
  async def oto_order(self, pair: str, *, working: Order, pending: Order, unsafe: Literal[False] = False) -> ListOrderResponse | Error:
    ...
  @overload
  async def oto_order(self, pair: str, *, working: Order, pending: Order, unsafe: Literal[True]) -> ListOrderResponse:
    ...
  @overload
  async def oto_order(self, pair: str, *, working: Order, pending: Order, unsafe: Literal[False] = False) -> ListOrderResponse | Error:
    ...
  @UserMixin.with_client
  async def oto_order(self, pair: str, *, working: Order, pending: Order, unsafe: bool = False) -> ListOrderResponse | Error:

    def cap_first(s: str):
      return s[0].upper() + s[1:]

    def rename(order: Order, prefix: str) -> dict:
      return {prefix + cap_first(key): value for key, value in order.items()}
    
    query = self.signed_query({
      'symbol': pair,
      'timestamp': binance_timestamp(datetime.now()),
      'newOrderRespType': 'FULL',
      **rename(working, 'working'),
      **rename(pending, 'pending'),
    })
    r = await self.client.post(
      f'{self.base}/api/v3/orderList/oto?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    val = validate_response(r.text, ListOrderResponse)
    if unsafe and val.code is not None:
      raise RuntimeError(f'Error creating OTO order: {val.code}, {val.msg}')
    return val


  @UserMixin.with_client
  async def replace_order(self, pair: str, orderId: int, order: Order) -> OrderResponse | Error:

    query = self.signed_query({
      'symbol': pair,
      'cancelOrderId': orderId,
      'newOrderRespType': 'FULL',
      'timestamp': binance_timestamp(datetime.now()),
      **order,
    })

    r = await self.client.post(
      f'{self.base}/api/v3/order/cancelReplace?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return validate_response(r.text, OrderResponse)
  
  @overload
  async def cancel_order(self, symbol: str, orderId: int, recvWindow: int = 5000, *, unsafe: Literal[False] = False) -> dict | Error:
    ...
  @overload
  async def cancel_order(self, symbol: str, orderId: int, recvWindow: int = 5000, *, unsafe: Literal[True]) -> dict:
    ...
  @UserMixin.with_client
  async def cancel_order(self, symbol: str, orderId: int, recvWindow: int = 5000, *, unsafe: bool = False) -> dict | Error:
    query = self.signed_query({
      'symbol': symbol,
      'orderId': orderId,
      'timestamp': binance_timestamp(datetime.now()),
      'recvWindow': recvWindow,
    })

    r = await self.client.delete(
      f'{self.base}/api/v3/order?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    val = validate_response(r.text, CancelOrderResponse)
    if unsafe and val.code is not None:
      raise RuntimeError(f'Error canceling order: {val.code}, {val.msg}')
    return val

  @overload
  async def cancel_order_list(self, symbol: str, orderListId: int, recvWindow: int = 5000, *, unsafe: Literal[False] = False) -> ListOrderResponse | Error:
    ...
  @overload
  async def cancel_order_list(self, symbol: str, orderListId: int, recvWindow: int = 5000, *, unsafe: Literal[True]) -> ListOrderResponse:
    ...
  @UserMixin.with_client
  async def cancel_order_list(self, symbol: str, orderListId: int, recvWindow: int = 5000, *, unsafe: bool = False) -> ListOrderResponse | Error:
    query = self.signed_query({
      'symbol': symbol,
      'orderListId': orderListId,
      'timestamp': binance_timestamp(datetime.now()),
      'recvWindow': recvWindow,
    })

    r = await self.client.delete(
      f'{self.base}/api/v3/orderList?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    val = validate_response(r.text, CancelOrderResponse)
    if unsafe and val.code is not None:
      raise RuntimeError(f'Error canceling order: {val.code}, {val.msg}')