#!/bin/bash
PYVENV_DIR=${PYVENV_DIR:-"$HOME/pyvenv"}
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Patches qui s appliquent sur tti 0.2.2
cd ${SCRIPT_DIR}/..
patch ${PYVENV_DIR}/lib/python3.11/site-packages/tti/indicators/_ichimoku_cloud.py < patch/_ichimoku_cloud.patch
patch ${PYVENV_DIR}/lib/python3.11/site-packages/tti/utils/data_preprocessing.py < patch/data_preprocessing.patch
