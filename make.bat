@echo off

if "%1" == "clean" (
  echo Clean watermark.exe and watermark.spec
  del watermark.exe watermark.spec
  echo Done
  goto end
)

pyinstaller --onefile -i icon.ico --distpath . src\watermark.py

:end
