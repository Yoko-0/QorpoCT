from datetime import datetime
from fastapi import FastAPI, Response, status

from QorpoApp.dataBase.models import CurrenciesTable
from QorpoApp.utils.currencyApi import get_price_currency

app = FastAPI()


@app.get("/price/history")  # example /price/history?page=2
async def get_price_history(response: Response, page: int = 1) -> dict:
    all_records = await CurrenciesTable.get_all()
    splited_records = [all_records[i:i + 10] for i in range(0, len(all_records), 10)]

    if len(splited_records) < page:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": f"There is no '{page}' page, current pages count is {len(splited_records)}"}

    cur_page = splited_records[page - 1]
    history = [
        {
            "currency": record.currency,
            "date_": record.date_,
            "price": record.price,
        }
        for record in cur_page
    ]
    return {"history": history}


@app.get("/price/{currency}")  # example /price/btc
async def get_price(currency: str, response: Response) -> dict:
    currency = currency.upper()
    price = await get_price_currency(currency)

    if price is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": f"Unknown currency {currency}"}

    await CurrenciesTable.create(
        currency=currency,
        date_=int(datetime.now().timestamp()),
        price=price,
    )

    return {
        "price": price,
        "pair": f"{currency}/USDT"
    }


@app.delete("/price/history")  # example /price/history
async def delete_price() -> dict:
    await CurrenciesTable.delete_all()
    return {"response": "The entire history was successfully deleted"}
