VENV_DIR="/home/gilles/Téléchargements/venv"
[ ! -d ${VENV_DIR} ] && python -m venv ${VENV_DIR}
${VENV_DIR}/bin/python3 -m pip install --upgrade pip
${VENV_DIR}/bin/pip install matplotlib
${VENV_DIR}/bin/pip install pandas
${VENV_DIR}/bin/pip install yfinance
${VENV_DIR}/bin/pip install tti
