@echo off
echo Installing required Python packages...

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install required packages
pip install mysql-connector-python
pip install python-dotenv
pip install cryptography
pip install tkcalendar
pip install python-docx
pip install customtkinter
pip install pillow
pip install matplotlib

echo Installation complete!
pause