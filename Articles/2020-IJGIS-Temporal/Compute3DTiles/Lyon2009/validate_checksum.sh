#!/bin/bash

if [ `command -v md5sum` ]; then
  md5_checksum=`tar c ${1}/Result/tileset_ouput_dir | md5sum`
elif [ `command -v md5` ]; then
  md5_checksum=`tar c ${1}/Result/tileset_ouput_dir | md5`
fi

echo $md5_checksum

if [ "$md5_checksum" == "feb8542ab49697b8fc04c56e1b3f996e" ]; then
  echo "Md5 checksum of computed tileset ok."
else
  echo "WARNING: md5 checksum of computed tileset does not match the reference one."
fi
