from fastapi import APIRouter, HTTPException

from app.state import latest_price

router = APIRouter(prefix="/price")


@router.get("")
async def get_all_prices():
    try:
        return latest_price
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch all prices: {str(e)}"
        )


@router.get("/{symbol}")
async def get_price(symbol: str):
    try:
        result = latest_price.get(symbol.upper())

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"Symbol '{symbol}' not found"
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching price for {symbol}: {str(e)}"
        )