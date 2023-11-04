PYVENV_DIR=${PYVENV_DIR:-"$HOME/pyvenv"}
export TMPDIR=${TMPDIR:-"/tmp"}
#export BOURSE_CONFIG_DIR=${BOURSE_CONFIG_DIR:-"${TMPDIR}/bconfig"}
${PYVENV_DIR}/bin/python3 src/bourse.py
