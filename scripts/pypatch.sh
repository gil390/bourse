PYVENV_DIR=${PYVENV_DIR:-"$HOME/pyvenv"}
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd ${SCRIPT_DIR}/..
${PYVENV_DIR}/bin/python3 ${SCRIPT_DIR}/diffpatch.py P ${PYVENV_DIR}/lib/python3.11/site-packages/tti/indicators/_ichimoku_cloud.py patch/_ichimoku_cloud.patch ${PYVENV_DIR}/lib/python3.11/site-packages/tti/indicators/_ichimoku_cloud.py -f
${PYVENV_DIR}/bin/python3 ${SCRIPT_DIR}/diffpatch.py P ${PYVENV_DIR}/lib/python3.11/site-packages/tti/utils/data_preprocessing.py patch/data_preprocessing.patch ${PYVENV_DIR}/lib/python3.11/site-packages/tti/utils/data_preprocessing.py -f
