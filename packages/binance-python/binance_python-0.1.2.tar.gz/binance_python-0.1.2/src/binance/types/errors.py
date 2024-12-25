from typing_extensions import Literal
from pydantic import BaseModel, RootModel, Field

class _BaseError(BaseModel):
  msg: str

class UnknownError(_BaseError):
  code: Literal[-1000]
  tag: Literal['UNKNOWN_ERROR'] = 'UNKNOWN_ERROR'

class InvalidMessage(_BaseError):
  code: Literal[-1013]
  tag: Literal['INVALID_MESSAGE'] = 'INVALID_MESSAGE'

class MissingParam(_BaseError):
  code: Literal[-1102]
  tag: Literal['MISSING_PARAM'] = 'MISSING_PARAM'

class UnreadParams(_BaseError):
  code: Literal[-1104]
  tag: Literal['UNREAD_PARAMS'] = 'UNREAD_PARAMS'

class OrderRejected(_BaseError):
  code: Literal[-2010]
  tag: Literal['ORDER_REJECTED'] = 'ORDER_REJECTED'

class CancelRejected(_BaseError):
  code: Literal[-2011]
  tag: Literal['CANCEL_REJECTED'] = 'CANCEL_REJECTED'

class RejectedKey(_BaseError):
  code: Literal[-2015]
  tag: Literal['REJECTED_KEY'] = 'REJECTED_KEY'

class OrderArchived(_BaseError):
  code: Literal[-2026]
  tag: Literal['ORDER_ARCHIVED'] = 'ORDER_ARCHIVED'

Error = UnknownError | OrderRejected | CancelRejected | InvalidMessage | OrderArchived | MissingParam | UnreadParams | RejectedKey

class ErrorRoot(RootModel):
  root: Error = Field(discriminator='code')