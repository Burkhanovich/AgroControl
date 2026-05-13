# AgroControl - Dala Sug'orish Boshqaruv Tizimi

O'zbekiston fermerlariga mo'ljallangan zamonaviy dala ekinlarini sug'orish jarayonini masofadan boshqarish va kuzatish platformasi.

## 📋 Loyiha Haqida

**AgroControl** - bu real vaqt rejimida dala ekinlarini sug'orish jarayonini monitoring qilish, boshqarish va avtomatlashtirish uchun mo'ljallangan veb-platforma.

### Asosiy Imkoniyatlar

- 🗺️ Interaktiv dala xaritasi
- 📊 Real-vaqt sensor ma'lumotlari monitoring
- 💧 Masofadan sug'orish boshqaruvi
- 📅 Avtomatik sug'orish jadvallari
- 📈 Tahlil va hisobotlar
- 🔔 Telegram/SMS bildirishnomalar
- 🌐 O'zbek va Rus tillari

## 🚀 Ishga Tushirish

### 1. Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2. Dependencies O'rnatish
```bash
pip install -r requirements.txt
```

### 3. Environment Sozlash
```bash
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# .env faylini tahrirlang:
# - SECRET_KEY
# - JWT_SECRET_KEY
# - DATABASE_URL
# - INFLUXDB_TOKEN
```

### 4. Server Ishga Tushirish
```bash
python manage.py runserver
```

**URL:** http://localhost:8000

## 📁 Loyiha Strukturasi

```
AgroControl/
├── manage.py              # Django-style manage.py
├── requirements.txt       # Python dependencies
│
├── config/                # Project settings
│   ├── settings.py        # Asosiy sozlamalar
│   ├── database.py        # Database
│   ├── security.py        # JWT, Auth
│   └── urls.py            # Routerlar
│
├── apps/                  # Barcha applar
│   ├── authentication/    # Login, Register
│   ├── dashboard/         # Dashboard
│   ├── farms/             # Fermer xo'jaliklari
│   ├── zones/             # Dala zonalari
│   ├── sensors/           # Sensorlar
│   ├── irrigation/        # Sug'orish
│   ├── schedules/         # Jadvallar
│   └── notifications/     # Bildirishnomalar
│
├── templates/             # HTML templates
│   ├── base.html
│   ├── auth/
│   └── dashboard/
│
└── static/                # CSS, JS, images
    ├── css/
    ├── js/
    └── images/
```

## 🛠️ Texnologiyalar

- **Backend:** Python FastAPI
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Database:** PostgreSQL, InfluxDB, Redis
- **Auth:** JWT (access + refresh token)

## 📚 API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 Xavfsizlik

- JWT autentifikatsiya
- Password hashing (bcrypt)
- HTTPS qo'llab-quvvatlash
- CORS sozlamalari
- Input validatsiya

## 📞 Yordam

Muammolar yuzaga kelsa:
- GitHub Issues: [loyiha repository]
- Email: support@agrocontrol.uz

## 📄 Litsenziya

MIT License

---

**Ishlab chiqilgan:** 2026  
**Versiya:** 1.0.0
