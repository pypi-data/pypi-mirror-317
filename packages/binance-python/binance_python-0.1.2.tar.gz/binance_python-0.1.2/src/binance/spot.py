from typing_extensions import Literal
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlencode
from decimal import Decimal
from pydantic import BaseModel
import orjson
from .client import ClientMixin
from .types import OrderStatus, Error, ErrorRoot, Order, ListStatusType, ListOrderStatus
from .util import sign, binance_timestamp


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

def validate_response(r: str) -> OrderResponse | Error:
  obj = orjson.loads(r)
  if 'code' in obj:
    return ErrorRoot.model_validate(obj).root
  return OrderResponse.model_validate(obj)

def validate_list_response(r: str) -> ListOrderResponse | Error:
  obj = orjson.loads(r)
  if 'code' in obj:
    return ErrorRoot.model_validate(obj).root
  return ListOrderResponse.model_validate(obj)

@dataclass
class Spot(ClientMixin):
  api_key: str
  api_secret: str
  base: str = 'https://api.binance.com'

  def sign(self, query_string: str) -> str:
    return sign(query_string, secret=self.api_secret)
  
  def signed_query(self, params: dict) -> str:
    return urlencode(params) + '&signature=' + self.sign(urlencode(params))

  @ClientMixin.with_client
  async def query_order(self, symbol: str, orderId: int, recvWindow: int = 5000) -> OrderResponse | Error:
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
    return validate_response(r.text)
  
  @ClientMixin.with_client
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
    return validate_list_response(r.text)

  @ClientMixin.with_client
  async def spot_order(self, pair: str, order: Order) -> OrderResponse | Error:
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
    return validate_response(r.text)
  

  @ClientMixin.with_client
  async def oto_order(self, pair: str, *, working: Order, pending: Order) -> ListOrderResponse | Error:

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
    return validate_list_response(r.text)


  @ClientMixin.with_client
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
    return validate_response(r.text)
  
  @ClientMixin.with_client
  async def cancel_order(self, symbol: str, orderId: str, recvWindow: int = 5000) -> OrderResponse | Error:
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
    return validate_response(r.text)

  @ClientMixin.with_client
  async def cancel_order_list(self, symbol: str, orderListId: int, recvWindow: int = 5000) -> ListOrderResponse | Error:
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
    return validate_list_response(r.text)