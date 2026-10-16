@echo off
echo ===================================================
echo   Starting ZeroWasteByte Full-Stack Application
echo ===================================================
echo [1/2] Checking Python Virtual Environment...
if not exist ".venv\Scripts\python.exe" (
    echo Setting up virtual environment...
    python -m venv .venv
    .venv\Scripts\pip install -r requirements.txt
)
echo [2/2] Launching FastAPI Backend with MongoDB...
echo ---------------------------------------------------
echo  Web Application: http://localhost:8000
echo  API Documentation: http://localhost:8000/docs
echo ---------------------------------------------------
.venv\Scripts\python.exe server.py
pause
