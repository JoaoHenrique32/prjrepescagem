from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# URLs das APIs (primária e de backup)
API_PRIMARY = "https://api.openweathermap.org/data/2.5/weather"
API_BACKUP = "https://api.weatherapi.com/v1/current.json"

# Suas chaves de API
API_KEY_PRIMARY = "sua_chave_primaria"
API_KEY_BACKUP = "sua_chave_de_backup"

@app.get("/weather")
async def get_weather(city: str):
    try:
        # Tentar a API primária
        async with httpx.AsyncClient() as client:
            response = await client.get(
                API_PRIMARY,
                params={"q": city, "appid": API_KEY_PRIMARY, "units": "metric"}
            )
            if response.status_code == 200:
                return response.json()

        # Se falhar, tentar a API de backup
        async with httpx.AsyncClient() as client:
            response = await client.get(
                API_BACKUP,
                params={"q": city, "key": API_KEY_BACKUP}
            )
            if response.status_code == 200:
                return response.json()

        # Lançar erro se ambas falharem
        raise HTTPException(status_code=502, detail="Falha ao obter dados de ambas as APIs")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
