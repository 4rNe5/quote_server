from fastapi import FastAPI, HTTPException
from typing import List, Optional
import random
from pydantic import BaseModel
import uvicorn
from quote_list import quote_list

class Quote(BaseModel):
    author: str
    authorProfile: str
    message: str

class QuoteResponse(BaseModel):
    quote: Quote
    total_quotes: int

# 명언 데이터 가공
quotes_data = [
    Quote(
        author=quote["author"],
        authorProfile=quote["authorProfile"],
        message=quote["message"]
    )
    for quote in quote_list
]

app = FastAPI(
    title="Quote API",
    description="위대한 사상가들의 인생 명언을 제공하는 API",
    version="0.1.1"
)

@app.get("/", response_model=QuoteResponse)
async def get_random_quote():
    # 무작위로 하나의 명언을 반환
    quote = random.choice(quotes_data)
    return QuoteResponse(quote=quote, total_quotes=len(quotes_data))

@app.get("/quotes", response_model=List[Quote])
async def get_all_quotes():
    # 모든 명언을 반환
    return quotes_data

@app.get("/quotes/author/{author}", response_model=List[Quote])
async def get_quotes_by_author(author: str):
    # 특정 저자의 명언을 반환
    author_quotes = [q for q in quotes_data if q.author.lower() == author.lower()]
    if not author_quotes:
        raise HTTPException(status_code=404, detail=f"저자 '{author}'의 명언을 찾을 수 없습니다")
    return author_quotes

@app.get("/quotes/search", response_model=List[Quote])
async def search_quotes(keyword: str):
    # 명언 내용이나 저자 이름에서 키워드를 검색.
    keyword = keyword.lower()
    matching_quotes = [
        q for q in quotes_data
        if keyword in q.message.lower() or
           keyword in q.author.lower() or
           keyword in q.authorProfile.lower()
    ]
    if not matching_quotes:
        raise HTTPException(status_code=404, detail=f"키워드 '{keyword}'를 포함한 명언을 찾을 수 없습니다")
    return matching_quotes

@app.get("/authors", response_model=List[str])
async def get_authors():
    # 모든 저자 목록 반환
    return sorted(list(set(q.author for q in quotes_data)))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)