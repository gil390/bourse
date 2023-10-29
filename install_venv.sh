PYVENV_DIR=${PYVENV_DIR:-"$HOME/pyvenv"}
[ ! -d ${PYVENV_DIR} ] && python -m venv ${PYVENV_DIR}
${PYVENV_DIR}/bin/python3 -m pip install --upgrade pip
${PYVENV_DIR}/bin/pip install matplotlib
${PYVENV_DIR}/bin/pip install pandas
${PYVENV_DIR}/bin/pip install yfinance
${PYVENV_DIR}/bin/pip install tti
${PYVENV_DIR}/bin/pip install tkscrolledframe
