'''
python3 required
https://raw.githubusercontent.com/argoproj/argo-cd/v1.8.7/manifests/install.yaml

用法:
	mkdir argocd/$ARGOCD_VERSION
	cp ./argocd-split.py argocd/$ARGOCD_VERSION
	popd argocd/$ARGOCD_VERSION
	python3 argocd-split.py -s $SOURCEFILE
	popd
'''

import os
import yaml
import argparse
import requests


def get_args():
    p = argparse.ArgumentParser(usage=u'argocd yaml split tool')
    p.add_argument('--source', '-s', type=str, help="url or filename", required=True)
    return p.parse_args()


def get_content_from_url(url):
    try:
        return requests.get(url).text
    except Exception as e:
        print("failed to get yaml content")
        return ""

def get_content_from_file(filename):
    with open(filename, "r") as f:
        return f.read()

def load_content_sections(content):
    return yaml.safe_load_all(content)


def save_sections(sections):
    if not os.path.exists("crds"):
        os.mkdir("crds")
    
    for sec in sections:
        filename = '{kind}_{name}'.format(
            kind=sec['kind'].lower(),
            name=sec['metadata']['name'].lower()
        )
        if 'customresourcedefinition' == sec['kind'].lower():
            filename = "crds/{0}".format(filename)
        with open(filename + ".yaml", 'w') as f:
            f.write(yaml.safe_dump(sec))
        print(filename)

def main():
    args = get_args()
    if args.source.startswith('http'):
        content = get_content_from_url(args.source)
    else:
        content = get_content_from_file(args.source)
    sections = load_content_sections(content)
    save_sections(sections)


if __name__ == "__main__":
    main()
