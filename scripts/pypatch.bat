IF "%PYVENV_DIR%"=="" (set PYVENV_DIR=%USERPROFILE%\pyvenv)
IF "%TEMP%"=="" (set TMPDIR=%USERPROFILE%\AppData\Local\Temp) ELSE (set TMPDIR=%TEMP%)
SET SCRIPTPATH=%~dp0
REM echo %SCRIPTPATH:~0,-1%

%PYVENV_DIR%\Scripts\python.exe src\utils\pypatch.py patch\_ichimoku_cloud.patch %PYVENV_DIR%\Lib\site-packages\tti\indicators\_ichimoku_cloud.py
%PYVENV_DIR%\Scripts\python.exe src\utils\pypatch.py patch\data_preprocessing.patch %PYVENV_DIR%\Lib\site-packages\tti\utils\data_preprocessing.py
