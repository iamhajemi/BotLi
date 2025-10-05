@echo off
echo 🤖 BotLi Otomatik Güncelleme Aracı
echo ====================================

REM Python'un yüklü olup olmadığını kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı. Lütfen Python'u yükleyin.
    pause
    exit /b 1
)

REM Git'in yüklü olup olmadığını kontrol et
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git bulunamadı. Lütfen Git'i yükleyin.
    pause
    exit /b 1
)

REM Güncelleme scriptini çalıştır
python update_botli.py

REM Hata durumunda bekle
if errorlevel 1 (
    echo.
    echo ❌ Güncelleme başarısız oldu.
    pause
    exit /b 1
)

echo.
echo ✅ Güncelleme tamamlandı!
echo BotLi'yi başlatmak için: python user_interface.py
pause
