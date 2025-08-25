import requests
from datetime import datetime, timezone
from dateutil import tz

OPEN_METEO_GEOCODING = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Céu limpo",
    1: "Principalmente limpo",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Névoa",
    48: "Névoa gelada",
    51: "Garoa fraca",
    53: "Garoa moderada",
    55: "Garoa intensa",
    56: "Garoa gelada fraca",
    57: "Garoa gelada intensa",
    61: "Chuva fraca",
    63: "Chuva moderada",
    65: "Chuva forte",
    66: "Chuva gelada fraca",
    67: "Chuva gelada forte",
    71: "Neve fraca",
    73: "Neve moderada",
    75: "Neve forte",
    77: "Grãos de neve",
    80: "Aguaceiros fracos",
    81: "Aguaceiros moderados",
    82: "Aguaceiros fortes",
    85: "Aguaceiros de neve fracos",
    86: "Aguaceiros de neve fortes",
    95: "Tempestade",
    96: "Tempestade com granizo fraca",
    99: "Tempestade com granizo forte",
}

def descrever_codigo(codigo: int) -> str:
    return WEATHER_CODES.get(codigo, f"Código {codigo}")

def geocodificar_cidade(nome_cidade: str, count: int = 1, lang: str = "pt"):
    params = {
        "name": nome_cidade,
        "count": count,
        "language": lang,
        "format": "json",
    }
    r = requests.get(OPEN_METEO_GEOCODING, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    return data.get("results", [])

def obter_previsao(latitude: float, longitude: float, dias: int = 3, tz_auto: bool = True):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,weathercode",
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "forecast_days": dias,
        "timezone": "auto" if tz_auto else "UTC",
    }
    r = requests.get(OPEN_METEO_FORECAST, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

def extrair_atual(hourly: dict, timezone_str: str):
    """
    Pega a hora mais próxima do 'agora' na timezone da API e devolve um snapshot.
    """
    times = hourly["time"]
    temps = hourly["temperature_2m"]
    hums  = hourly["relative_humidity_2m"]
    precs = hourly["precipitation"]
    codes = hourly["weathercode"]

    now_idx = None
    now_local = datetime.now(timezone.utc).astimezone(tz.gettz(timezone_str))

    for i, t in enumerate(times):
        t = datetime.fromisoformat(t.replace("Z", "+00:00")).astimezone(tz.gettz(timezone_str))
        if t <= now_local:
            now_idx = i
        else:
            break

    if now_idx is None:
        now_idx = 0  # Nenhum horário no passado? Pega o primeiro.

    return {
        "time": times[now_idx],
        "temperature": temps[now_idx],
        "humidity": hums[now_idx],
        "precipitation": precs[now_idx],
        "weathercode": codes[now_idx],
        "description": descrever_codigo(codes[now_idx]),
    }

def montar_resumo_diario(daily: dict):
    dias = []
    for i, dia in enumerate(daily["time"]):
        dias.append({
            "date": dia,
            "wcode": daily["weathercode"][i],
            "wdesc": descrever_codigo(daily["weathercode"][i]),
            "tmax": daily["temperature_2m_max"][i],
            "tmin": daily["temperature_2m_min"][i],
            "rain": daily["precipitation_sum"][i],
        })
    return dias