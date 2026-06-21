"D:\Mobile Tracker projects\mobile-tracking-system\mobile-tracking-system\agents\.venv\Scripts\python.exe" -m pip install --upgrade pip
"D:\Mobile Tracker projects\mobile-tracking-system\mobile-tracking-system\agents\.venv\Scripts\python.exe" -m pip install -r requirements.txt
"D:\Mobile Tracker projects\mobile-tracking-system\mobile-tracking-system\agents\.venv\Scripts\python.exe" -m pip list | findstr fastapi
"D:\Mobile Tracker projects\mobile-tracking-system\mobile-tracking-system\agents\.venv\Scripts\python.exe" -m pip list | findstr uvicorn
python agent_service.py
uvicorn agents.agent_service:app --host 0.0.0.0 --port 8001 --reload