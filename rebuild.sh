#!/bin/sh
set -e
cd "$(dirname "$0")"
cp template_v1.html template.html
for n in 2 3 4 5 6 7 8 9 10 11 12; do python3 v${n}_patch.py >/dev/null; done
python3 assemble.py template.html seed.json ../app/index.html
sed -i 's/unity-v[0-9]*"/unity-v12"/' ../app/sw.js
grep -o 'const VERSION = "[0-9.]*"' ../app/index.html; grep -o 'unity-v[0-9]*' ../app/sw.js
