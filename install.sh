#########################################################################
# File Name: install.sh
# Author: Cixi.Geng
# mail: cixi.geng@unisoc.com
# Created Time: 2020年11月10日 星期二 13时42分48秒
#########################################################################
#!/bin/bash

GCOV_BIN="$PWD"

cp lcovrc ~/.lcovrc
echo "export GCOV_BIN=\"${GCOV_BIN}\"" >> ~/.bashrc
echo "export PATH=\${GCOV_BIN}:\$PATH" >> ~/.bashrc
source ~/.bashrc
