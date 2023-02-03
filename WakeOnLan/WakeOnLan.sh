#!/bin/bash
# Wake on LAN
if [ -n "$1" ]
then
                val=$1
fi
echo ""
echo "Wake on LAN is running..."
echo "Selected MAC-ADDRESS: ${val}"
echo ""
sudo wakeonlan ${val}
echo "The computer is now starting up!"
#mac 00-C0-9F-C7-06-D7