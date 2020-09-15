#!/bin/bash
git pull
echo "version = '$(git describe --abbrev=7 --always)'" > app/version.py
/bin/bash setup.sh