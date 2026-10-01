@echo off
rem Double-click to install (first time) and start the MS Estonia site.
cd /d "%~dp0"

set PY=python
where python >nul 2>nul || set PY=py
where %PY% >nul 2>nul || (
  echo Python was not found. Install it from https://www.python.org and tick "Add python.exe to PATH".
  pause
  exit /b 1
)

if not exist env\Scripts\python.exe (
  echo Creating Python environment...
  %PY% -m venv env || (pause & exit /b 1)
)

echo Installing requirements...
env\Scripts\python.exe -m pip install -q -r requirements.txt || (pause & exit /b 1)

echo Starting site at http://localhost:8501  (close this window to stop)
env\Scripts\python.exe -m streamlit run app.py
pause
