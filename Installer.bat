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

pyinstaller --noconfirm --clean --onefile --windowed --icon=logo.png --add-data "Back_End\.env.secret;Back_End" --add-data "Front_End\Pic\logo.png;Front_End\Pic" --additional-hooks-dir=. --collect-all mysql.connector --hidden-import mysql.connector.plugins --hidden-import mysql.connector.plugins.mysql_native_password --hidden-import mysql.connector.plugins.caching_sha2_password --hidden-import mysql.connector.plugins.authentication --hidden-import mysql.connector.authentication --collect-all cryptography --hidden-import cryptography BHMS.py

echo Installation complete!
pause