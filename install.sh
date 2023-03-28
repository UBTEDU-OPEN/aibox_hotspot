#!/bin/bash

cat << EOF
/*
 * Install oneAI
 */
EOF

ROOT_PATH=$(cd "$(dirname "$0")";pwd)

pushd $ROOT_PATH &> /dev/null

PROJECT_NAME="hotspot"

HOTSPOT_EXE_PATH="/usr/local/UBTTools/hotspot/"
HOTSPOT_EXE_NAME="hotspot.py"
HOTSPOT_CONF_DIR="/home/oneai/.config/hotspot"
pwd

echo "1.Clean up"
rm -rf build dist $HOTSPOT_EXE_PATH$HOTSPOT_EXE_NAME

echo "2.copy "$HOTSPOT_EXE_NAME "and conf"
#目录不存在创建
if [ ! -d ${HOTSPOT_EXE_PATH} ];then
    mkdir -p -m=755 $HOTSPOT_EXE_PATH
fi
cp ./hotspot/$HOTSPOT_EXE_NAME $HOTSPOT_EXE_PATH
chmod 755 $HOTSPOT_EXE_PATH$HOTSPOT_EXE_NAME

#配置
if [ ! -d ${HOTSPOT_CONF_DIR} ];then
    mkdir -p -m=755 $HOTSPOT_CONF_DIR
fi
cp -rfp hotspot/common/config/locale $HOTSPOT_CONF_DIR
cp -pf hotspot/common/config/hotspot.ini $HOTSPOT_CONF_DIR

echo "3.Installing "$PROJECT_NAME
python3 setup.py install

echo "4.done"

popd &> /dev/null

