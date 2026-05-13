# OpenWeatherMap API Key Olish

AgroControl loyihasida ob-havo ma'lumotlarini ko'rish uchun OpenWeatherMap API key kerak.

## 1. Ro'yxatdan o'tish

1. https://openweathermap.org/ saytiga kiring
2. **Sign Up** tugmasini bosing
3. Email, username va parol kiriting
4. Emailingizni tasdiqlang

## 2. API Key Olish

1. https://home.openweathermap.org/api_keys ga kiring
2. **Create Key** tugmasini bosing
3. Key nomini kiriting (masalan: "AgroControl")
4. API key ko'rinadi (masalan: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

## 3. API Key ni Loyihaga Qo'shish

`.env` faylini oching va quyidagini qo'shing:

```env
OPENWEATHER_API_KEY=sizning-api-key-ingiz
```

Masalan:
```env
OPENWEATHER_API_KEY=YOUR_API_KEY_HERE
```

## 4. Serverni Qayta Ishga Tushirish

```bash
python manage.py runserver
```

## 5. Ob-havo Sahifasini Ochish

http://localhost:8000/weather

---

## Eslatma

- **Bepul rejada:** 60 ta so'rov/daqiqa, 1,000,000 so'rov/oy
- API key faollashuvi 10-15 daqiqa vaqt olishi mumkin
- Agar xatolik bo'lsa, API key faolligini tekshiring

## Test Qilish

```bash
curl "https://api.openweathermap.org/data/2.5/weather?lat=41.2995&lon=69.2401&appid=SIZNING_API_KEY&units=metric"
```

Agar javob kelsa, API key ishlayapti!
