#########################################################################
# File Name: install.sh
# Author: Cixi.Geng
# mail: cixi.geng@unisoc.com
# Created Time: 2020年11月10日 星期二 13时42分48秒
#########################################################################
#!/bin/bash

GCOV_BIN="$PWD/fakeroot/usr/bin"

SET_PARA1="export GCOV_BIN=\"${GCOV_BIN}\""
grep "$SET_PARA1" ${HOME}/.bashrc && sed -i "/export GCOV_BIN=/d" ${HOME}/.bashrc
echo $SET_PARA1 >> ${HOME}/.bashrc

SET_PARA2="export PATH=\${GCOV_BIN}:\$PATH"
grep "$SET_PARA2" ${HOME}/.bashrc && sed -i "/export PATH=\${GCOV_BIN}/d" ${HOME}/.bashrc
echo $SET_PARA2 >> ${HOME}/.bashrc

source ${HOME}/.bashrc
cp lcovrc ${HOME}/.lcovrc

generate_deb_package()
{
	cd fakeroot
	md5sum `find usr -type f` > DEBIAN/md5sums
	cd ..
	if [ -f lcov-kernel.deb ];then
		rm lcov-kernel.deb
	fi
	dpkg -b fakeroot lcov-kernel.deb
}

