from dataclasses import dataclass
from binance import Spot, Public, UserStream, User

@dataclass
class Binance(UserStream, Public, Spot, User):
  
  @classmethod
  def env(cls):
    import os
    from dotenv import load_dotenv
    load_dotenv()
    errs = []
    if (api_key := os.getenv('API_KEY')) is None:
      errs.append('API_KEY is not set')
    if (api_secret := os.getenv('API_SECRET')) is None:
      errs.append('API_SECRET is not set')
    if errs:
      raise RuntimeError(', '.join(errs))
    return cls(api_key, api_secret) # type: ignore