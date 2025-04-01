from fastapi import APIRouter

router = APIRouter()

@router.get("/info")
async def get_static_info():
    return {
        "locations": [
            {
                "address": "ул. Примерная, 1",
                "working_hours": "09:00 - 22:00",
                "phone": "+7 (999) 123-45-67"
            },
            {
                "address": "пр. Тестовый, 10",
                "working_hours": "08:00 - 23:00",
                "phone": "+7 (999) 765-43-21"
            }
        ],
        "company_info": {
            "name": "Coffee Shop",
            "description": "Сеть кофеен на вынос",
            "email": "info@coffeeshop.com"
        },
        "delivery_info": {
            "min_order": 500,
            "delivery_fee": 200,
            "free_delivery_threshold": 1500
        }
    }

@router.get("/static")
async def get_static():
    return {"message": "Static files endpoint"} 