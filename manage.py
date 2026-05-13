#!/usr/bin/env python3
"""
AgroControl - Django-style manage.py
Loyihani ishga tushirish va boshqarish
"""
import sys
import uvicorn

def runserver():
    """Development server ishga tushirish"""
    print("AgroControl ishga tushirilmoqda...")
    print("=" * 60)
    print("Server tayyor!")
    print("URL: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Login: http://localhost:8000/login")
    print("\nTo'xtatish uchun: Ctrl+C\n")

    uvicorn.run(
        "config.urls:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

def main():
    """Asosiy funksiya"""
    if len(sys.argv) < 2:
        print("Foydalanish: python manage.py [command]")
        print("\nMavjud buyruqlar:")
        print("  runserver    - Development server ishga tushirish")
        print("  shell        - Python shell ochish")
        sys.exit(1)

    command = sys.argv[1]

    if command == "runserver":
        runserver()
    elif command == "shell":
        import code
        code.interact(local=locals())
    else:
        print(f"Noma'lum buyruq: {command}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServer to'xtatildi")
        sys.exit(0)
    except Exception as e:
        print(f"\nXatolik: {e}")
        sys.exit(1)
