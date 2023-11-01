IF "%PYVENV_DIR%"=="" (set PYVENV_DIR=%USERPROFILE%\pyvenv)
IF "%TEMP%"=="" (set TMPDIR=%USERPROFILE%\AppData\Local\Temp) ELSE (set TMPDIR=%TEMP%)
%PYVENV_DIR%\Scripts\python.exe src/bourse.py
