#!/bin/bash

pushd .
cd /usr/lib/cgi-bin/tilecache-2.10
sudo su www-data -c "./tilecache_seed.py za -b 16,-35,33,-21 1 12"
popd
