#!/usr/bin/env python3

from collections import defaultdict
import glob
import re
import sys

pattern = re.compile('(.*)_v([0-9]+).*\\.JPG')

grouped_pictures = defaultdict(list)

for fn in sys.argv[1:]:
    m = pattern.match(fn)
    if m:
        grouped_pictures[m.groups()[0]].append((fn, int(m.groups()[1])))

latest_versions = tuple(max(v, key=lambda x: x[1]) for v in grouped_pictures.values())

for lv in latest_versions:
    print(lv[0])


