#!/usr/bin/env python3
"""镜像同步健康巡检：mirror_updated 超过 25h 的仓列 WARN（同步周期 8h，两轮未到即异常）。
用法：python3 scripts/check-mirror-health.py"""
import json, subprocess, sys, time, os
from datetime import datetime

TOKEN_FILE = os.path.expanduser('~/.config/forgejo/token')
TABLE = os.path.join(os.path.dirname(__file__), '..', 'data', 'source-mirrors.json')
doc = json.load(open(TABLE))
orgs = sorted({e['upstream'].split('github.com/')[1].split('/')[0] for e in doc['fonts'] if e['feicode_mirror']})
token = open(TOKEN_FILE).readline().strip()
now = time.time()
warns = []
checked = 0
for org in orgs:
    r = subprocess.run(['curl','-s','--max-time','20',
        f'https://feicode.com/api/v1/orgs/{org}/repos?limit=50',
        '-H', f'Authorization: token {token}'], capture_output=True, text=True)
    try:
        repos = json.loads(r.stdout)
    except Exception:
        continue
    if not isinstance(repos, list):
        continue
    for repo in repos:
        mu = repo.get('mirror_updated') or ''
        if not mu:
            continue
        try:
            ts = datetime.fromisoformat(mu.replace('Z', '+00:00')).timestamp()
        except Exception:
            continue
        checked += 1
        age_h = (now - ts) / 3600
        if age_h > 25:
            warns.append((repo['full_name'], round(age_h, 1)))
if warns:
    print(f'MIRROR-WARN {len(warns)}/{checked} 仓同步滞后 >25h（同步失败或上游代理断连，处置见 MIRROR-SOP §2/§3）:')
    for n, h in sorted(warns, key=lambda x: -x[1]):
        print(f'  {n}: 上次同步 {h}h 前')
    sys.exit(1)
print(f'MIRROR-OK {checked} 仓全部正常')
