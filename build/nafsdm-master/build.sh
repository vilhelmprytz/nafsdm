#!/bin/bash

$BUILD_PATH="build/nafsdm-master"

cd ../..

mkdir $BUILD_PATH/home
mkdir -p $BUILD_PATH/usr/bin

cp -R nafsdm-master $BUILD_PATH/home
cp systemconfigs/nafsdm-manager $BUILD_PATH/usr/bin/
cp systemconfigs/nafsdmctl $BUILD_PATH/usr/bin
cp systemconfigs/nafsdm-webinterface.service $BUILD_PATH/home/master-nafsdm/webinterface/nafsdm-webinterface.service
cp LICENSE $BUILD_PATH/home/master-nafsdm
cp CHANGELOG.md $BUILD_PATH/home/master-nafsdm/changelog.txt

cd build

/usr/bin/env dpkg-deb --build nafsdm-master
