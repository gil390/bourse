IF "%PYVENV_DIR%"=="" (set PYVENV_DIR=%USERPROFILE%\pyvenv)
python3 -m venv %PYVENV_DIR%
%PYVENV_DIR%\Scripts\python.exe -m pip install --upgrade pip
%PYVENV_DIR%\Scripts\pip3.exe install matplotlib
%PYVENV_DIR%\Scripts\pip3.exe install pandas
%PYVENV_DIR%\Scripts\pip3.exe install yfinance
%PYVENV_DIR%\Scripts\pip3.exe install tti
%PYVENV_DIR%\Scripts\pip3.exe install tkscrolledframe
%PYVENV_DIR%\Scripts\pip3.exe install diff-match-patch