#!/bin/bash
PREFIX=/opt/e4biblesaver/
PY=e4biblesaver.py
LIB=e4biblelib.so
SYMLINK=/usr/bin/e4biblesaver
BIBLE=bible.txt

sudo rm -rf $PREFIX
sudo rm -f $SYMLINK
sudo install -d $PREFIX
cd pyext-e4biblelib
echo \"$PREFIX$BIBLE\">src/bible.h
cargo build --release && cp target/release/libe4biblelib.so ../e4biblelib.so
sudo install $BIBLE $PREFIX
cd ..
sudo install $PY $PREFIX
sudo install $LIB $PREFIX
sudo ln -s $PREFIX$PY $SYMLINK
