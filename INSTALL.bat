@echo off
python3 -m pip install --upgrade pip
pip install -r requirements.txt
pip install -q -U google-generativeai
start START.bat
exit