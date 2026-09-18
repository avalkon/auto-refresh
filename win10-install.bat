python -m venv %AppData%\auto-refresh.venv
mkdir %AppData%\auto-refresh.venv\sounds
copy %0\..\sounds\sound1.mp3 %AppData%\auto-refresh.venv\sounds
xcopy %0\..\images %AppData%\auto-refresh.venv\images /E/H/C/I
copy %0\..\LICENSE %AppData%\auto-refresh.venv
copy %0\..\README.md %AppData%\auto-refresh.venv
copy %0\..\auto-refresh-0.2.70.py %AppData%\auto-refresh.venv
copy %0\..\config.ini %AppData%\auto-refresh.venv
copy %0\..\requirements.txt %AppData%\auto-refresh.venv
copy %0\..\win10-run.bat %AppData%\auto-refresh.venv
copy %0\..\win10-uninstall.bat %AppData%\auto-refresh.venv
call %AppData%\auto-refresh.venv\Scripts\activate.bat
python -m pip install -r %AppData%\auto-refresh.venv\requirements.txt
call %AppData%\auto-refresh.venv\Scripts\deactivate.bat
