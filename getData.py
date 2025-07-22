import requests
import time
import csv
from datetime import datetime

API_KEY = "dee67626ae3aece5307ba760b1c75042"

districts = {
    "Quan1": (10.77707, 106.69533),
    "Quan3": (10.78356, 106.68394),
    "Quan5": (10.75575, 106.66943),
    "BinhThanh": (10.81112, 106.70871),
    "GoVap": (10.84081, 106.66943)
}

def fetch_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def save_to_csv(data):
    filename = "weather_data.csv"
    file_exists = False
    try:
        open(filename, "r")
        file_exists = True
    except:
        pass

    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "time", "province", "city", "temperature", "temp_min", "temp_max", "humidity", "feels_like",
                "visibility", "precipitation", "cloudcover", "wind_speed", "wind_gust",
                "wind_direction", "pressure", "is_day", "weather_code", "weather_main", "weather_description"
            ])
        for row in data:
            writer.writerow(row)

while True:
    current_data = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for name, (lat, lon) in districts.items():
        weather = fetch_weather(lat, lon)

        # Lấy dữ liệu từ JSON
        temp = weather["main"]["temp"]
        temp_min = weather["main"]["temp_min"]
        temp_max = weather["main"]["temp_max"]
        humidity = weather["main"]["humidity"]
        feels_like = weather["main"]["feels_like"]
        visibility = weather.get("visibility", 0.0)
        precipitation = weather.get("rain", {}).get("1h", 0.0)
        cloudcover = weather["clouds"]["all"]
        wind_speed = weather["wind"]["speed"]
        wind_gust = weather["wind"].get("gust", 0.0)
        wind_deg = weather["wind"].get("deg", 0.0)
        pressure = weather["main"]["pressure"]
        is_day = 1 if weather["weather"][0]["icon"].endswith("d") else 0
        weather_code = weather["weather"][0]["id"]
        main = weather["weather"][0]["main"]
        desc = weather["weather"][0]["description"]

        current_data.append([
            now, f"TPHCM-{name}", name, temp, temp_min, temp_max, humidity, feels_like, visibility,
            precipitation, cloudcover, wind_speed, wind_gust, wind_deg, pressure,
            is_day, weather_code, main, desc
        ])

    save_to_csv(current_data)
    print(f"{now}: Đã lưu dữ liệu thời tiết cho {len(districts)} quận.")
    time.sleep(60)  # Lặp lại mỗi phút
