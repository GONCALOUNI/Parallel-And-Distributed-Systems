@echo off
echo → Starting services with Docker Compose…
docker-compose up --build -d

if %ERRORLEVEL%==0 (
  echo Services started.
) else (
  echo Failed to start services.
)
pause