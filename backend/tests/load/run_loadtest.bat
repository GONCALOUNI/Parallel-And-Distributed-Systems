@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

IF "%BASE_URL%"=="" SET "BASE_URL=http://host.docker.internal:8000"
SET "OUT_DIR=%~dp0"
SET "OUT_FILE=k6-results.json"
SET "SCRIPT=/tests/loadtest.js"
SET "RESULT=%OUT_DIR%%OUT_FILE%"

IF EXIST "%RESULT%" (
  echo → removing stale file %OUT_FILE%
  DEL "%RESULT%"
)

echo Running load test against %BASE_URL%…

where docker >nul 2>&1
IF %ERRORLEVEL%==0 (
  echo → using Dockerized k6
  docker run --rm ^
    -v "%OUT_DIR%":/tests ^
    -e BASE_URL="%BASE_URL%" ^
    grafana/k6 run ^
      --vus 100 ^
      --duration 5m ^
      --out json=/tests/%OUT_FILE% ^
      "%SCRIPT%"
) ELSE (
  where k6 >nul 2>&1
  IF %ERRORLEVEL%==0 (
    echo → using local k6
    k6 run ^
      --vus 100 ^
      --duration 5m ^
      --out json="%RESULT%" ^
      --env BASE_URL="%BASE_URL%" ^
      "%OUT_DIR%loadtest.js"
  ) ELSE (
    echo Error: neither Docker nor k6 is installed. >&2
    exit /b 1
  )
)

echo Results written to %RESULT%
ENDLOCAL