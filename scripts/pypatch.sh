PYVENV_DIR=${PYVENV_DIR:-"$HOME/pyvenv"}
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd ${SCRIPT_DIR}/..
REM ${PYVENV_DIR}/bin/python3 src/utils/pypatch.py _ichimoku_cloud.py /home/gilles/pyvenv/lib/python3.11/site-packages/tti/indicators/_ichimoku_cloud.py patch/_ichimoku_cloud.patch
REM ${PYVENV_DIR}/bin/python3 src/utils/pypatch.py data_preprocessing.py /home/gilles/pyvenv/lib/python3.11/site-packages/tti/utils/data_preprocessing.py patch/data_preprocessing.patch

${PYVENV_DIR}/bin/python3 src/utils/pypatch.py patch/_ichimoku_cloud.patch ${PYVENV_DIR}/lib/python3.11/site-packages/tti/indicators/_ichimoku_cloud.py
${PYVENV_DIR}/bin/python3 src/utils/pypatch.py patch/data_preprocessing.patch ${PYVENV_DIR}/lib/python3.11/site-packages/tti/utils/data_preprocessing.py
