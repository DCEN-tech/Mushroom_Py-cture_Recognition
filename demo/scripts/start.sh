#!/bin/bash

PROG_PATH=`dirname $0`

cd "${PROG_PATH}/../src" && streamlit \
   run app.py \
   --theme.base='dark'
