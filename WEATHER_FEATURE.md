# AgroControl - Ob-havo Bo'limi

## ✅ Qo'shilgan Funksiyalar

### 1. Real Ob-havo Ma'lumotlari
- **OpenWeatherMap API** integratsiyasi
- Joriy ob-havo (harorat, namlik, shamol, bosim)
- 7 kunlik prognoz
- O'zbek tilida tavsiflar

### 2. Ko'rsatiladigan Ma'lumotlar

**Joriy ob-havo:**
- Harorat (°C)
- His qilinadigan harorat
- Namlik (%)
- Shamol tezligi (m/s)
- Atmosfera bosimi (hPa)
- Ob-havo tavsifi
- Ob-havo ikonkasi

**7 kunlik prognoz:**
- Hafta kuni nomi (o'zbek tilida)
- Sana
- Maksimal/minimal harorat
- Namlik
- Shamol tezligi
- Yog'ingarchilik ehtimoli (%)
- Ob-havo tavsifi va ikonka

### 3. Texnik Xususiyatlar

**Backend:**
- `apps/weather/service.py` - OpenWeatherMap API bilan ishlash
- `apps/weather/views.py` - FastAPI endpoints
- `apps/weather/schemas.py` - Pydantic models
- Async HTTP so'rovlar (httpx)
- Error handling va logging

**Frontend:**
- `templates/weather/index.html` - Responsive dizayn
- Real-time ma'lumotlar yuklash
- Loading va error states
- Tailwind CSS styling
- Gradient background
- Weather icons

**API Endpoint:**
```
GET /api/weather?lat=41.2995&lon=69.2401
```

**Parametrlar:**
- `lat` - Kenglik (latitude) - default: 41.2995 (Toshkent)
- `lon` - Uzunlik (longitude) - default: 69.2401 (Toshkent)

**Authentication:**
- JWT token talab qilinadi
- `get_current_user` dependency

### 4. Fayllar Tuzilmasi

```
apps/weather/
├── __init__.py
├── service.py      # OpenWeatherMap API service
├── views.py        # FastAPI routes
└── schemas.py      # Pydantic models

templates/weather/
└── index.html      # Frontend sahifa

config/
├── settings.py     # OPENWEATHER_API_KEY qo'shildi
└── urls.py         # Weather router qo'shildi
```

### 5. Sozlash

**1. API Key Olish:**
- https://openweathermap.org/ da ro'yxatdan o'ting
- API key oling (bepul: 60 so'rov/daqiqa)

**2. .env faylga qo'shing:**
```env
OPENWEATHER_API_KEY=sizning-api-key-ingiz
```

**3. Serverni ishga tushiring:**
```bash
python manage.py runserver
```

**4. Sahifani oching:**
```
http://localhost:8000/weather
```

### 6. Xususiyatlar

✅ Real-time ma'lumotlar  
✅ 7 kunlik prognoz  
✅ O'zbek tilida  
✅ Responsive dizayn  
✅ Error handling  
✅ Loading states  
✅ Authentication  
✅ Toshkent koordinatalari (default)  
✅ Har qanday joylashuv uchun (lat/lon parametrlari)  

### 7. API Limitlar

**Bepul reja:**
- 60 so'rov/daqiqa
- 1,000,000 so'rov/oy
- 5 kunlik tarix
- 7 kunlik prognoz

### 8. Kelajakda Qo'shilishi Mumkin

- Fermer xo'jaligi joylashuvini saqlash
- Bir nechta joylashuv uchun ob-havo
- Bildirishnomalar (yomg'ir, sovuq)
- Grafik va diagrammalar
- Tarixiy ma'lumotlar
- Ekin uchun tavsiyalar

---

**Yaratilgan:** 2026-05-13  
**Status:** ✅ Tayyor va ishlamoqda
