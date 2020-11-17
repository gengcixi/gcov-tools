#########################################################################
# File Name: install.sh
# Author: Cixi.Geng
# mail: cixi.geng@unisoc.com
# Created Time: 2020年11月10日 星期二 13时42分48秒
#########################################################################
#!/bin/bash

GCOV_BIN="$PWD/fakeroot/usr/bin"

SET_PARA1="export GCOV_BIN=\"${GCOV_BIN}\""
grep "$SET_PARA1" ~/.bashrc && sed -i "/export GCOV_BIN=/d" ~/.bashrc || echo $SET_PARA1 >> ~/.bashrc
SET_PARA2="export PATH=\${GCOV_BIN}:\$PATH"
grep "$SET_PARA2" ~/.bashrc && sed -i "/export PATH=\${GCOV_BIN}/d" ~/.bashrc || echo $SET_PARA2 >> ~/.bashrc

#echo "export GCOV_BIN=\"${GCOV_BIN}\"" >> ~/.bashrc
#echo "export PATH=\${GCOV_BIN}:\$PATH" >> ~/.bashrc
source ~/.bashrc
cp lcovrc ~/.lcovrc
generate_deb_package()
{
	cd fakeroot
	md5sum `find usr -type f` > DEBIAN/md5sums
	cd ..
	if [ -f *.deb ];then
		rm *.deb
	fi
	dpkg -b fakeroot lcov-kernel.deb
}

