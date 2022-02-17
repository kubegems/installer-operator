# -*- coding: utf-8 -*-

import os
import yaml

fs = os.listdir("./")

for f in fs:
    if os.path.isfile(f) and f.endswith(".yaml"):
        with open(f) as fd:
            content = fd.read()
            sections = yaml.safe_load_all(content)
            for section in sections:
                print('kubectl delete {0} {1}'.format(section['kind'], section['metadata']['name']))
