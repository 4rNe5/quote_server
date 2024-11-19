from pydantic import BaseModel

class Quote(BaseModel):
    author: str
    authorProfile: str
    message: str
class QuoteResponse(BaseModel):
    quote: Quote
    total_quotes: int