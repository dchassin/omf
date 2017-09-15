#!/bin/sh
# Command to start up the OMF web server locally. Works on Unix, macOS.
script_dir=$(dirname $0)
cd $script_dir/omf
python $script_dir/omf/web.py
read -n1 -r -p "Server stopped. Press space to continue..." key