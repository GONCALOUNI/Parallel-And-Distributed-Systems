@echo off
echo → Stopping services…
docker-compose down

if %ERRORLEVEL%==0 (
  echo Services stopped.
) else (
  echo Failed to stop services.
)
pause