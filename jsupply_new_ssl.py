#!/opt/alt/python38/bin/python3.8
import argparse
import json
import os
import re
import subprocess
import sys


CACHE_FILE = "/var/cache/imunify360-webshield/ssl.cache"


KEY_PATT = re.compile(r"""(?s)(-----BEGIN.+?KEY-----.+-----END.+?KEY-----)""")
CERT_PATT = re.compile(r"""(?s)(-----BEGIN CERTIFICATE-----.+?-----END CERTIFICATE-----)""")

def process(args, ret=False):
    data = {'domain': args.domain}
    path = getattr(args, "bundle", None)
    if not path:
        return
    with open(path) as f:
        raw = f.read()
    k = KEY_PATT.search(raw)
    if k:
        data['key'] = k[1]
    c = CERT_PATT.findall(raw)
    if c:
        data['certificate'] = c[0]
    if len(c) > 1:
        data['chain'] = '\n'.join(c[1:])
    if ret:
        return json.dumps([data])
    json.dump([data], sys.stdout)


def compose(args, ret=False):
    data = {'domain': args.domain}
    for item in 'key', 'certificate', 'chain':
        item_path = getattr(args, item, None)
        if not item_path:
            continue
        with open(item_path) as f:
            data[item] = f.read()
    if ret:
        return json.dumps([data])
    json.dump([data], sys.stdout)


def add_to_cache(data):
    p = subprocess.Popen(["im360-ssl-cache", "-a", "-"], stdin=subprocess.PIPE)
    p.communicate(data.encode('ascii'))
    return p.returncode
    

def remove_from_cache(domain):
    try:
        subprocess.run(["im360-ssl-cache", "-R", domain], check=True)
    except subprocess.CalledProcessError:
        return 1
    else:
        return 0


def purge_cache():
    try:
        with open(CACHE_FILE, "w"): pass
    except Exception:
        return 1
    return 0


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument('-d', '--domain', help="domain")
    args.add_argument('-k', '--key', help="Key path")
    args.add_argument('-c', '--certificate', help="Certificate path")
    args.add_argument('-C', '--chain', help="Chain path")
    args.add_argument('-B', '--bundle', help="Path to bundle file (key, cert and chain in one file)")
    args.add_argument('-a', '--add', help="add the specified certificate data to ssl-cache", action="store_true")
    args.add_argument('-r', '--remove', help="remove data for the given domain from ssl-cache", action="store_true")
    args.add_argument('-p', '--purge', help="remove all domains from ssl-cache", action="store_true")
    return args.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if not any(vars(args).values()):
        sys.exit()

    if (args.add or args.remove or args.purge) and os.geteuid() != 0:
        raise SystemExit("Root privileges are required to modify ssl-cache")

    if args.purge:
        sys.exit(purge_cache())

    if args.domain is None:
        raise SystemExit("Domain name is required. Please set it with '-d' option")
        
    if args.remove:
        sys.exit(remove_from_cache(args.domain))

    if args.bundle is not None:
        if args.add:
            sys.exit(add_to_cache(process(args, ret=True)))
        process(args)
    else:
        if args.add:
            sys.exit(add_to_cache(compose(args, ret=True)))
        compose(args)

