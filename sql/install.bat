py -m venv .env
.\.env\Scripts\activate
py -m pip install -r requirements.txt

rem if using a local pip archive
rem py -m pip install --no-index --find-links=/local/dir/ requests
