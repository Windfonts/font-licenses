#!/bin/bash
# 镜像健康巡检包装：告警投 mailbox
OUT=$(python3 /Users/feibisi-studio/Projects/font-licenses/scripts/check-mirror-health.py 2>&1)
RC=$?
if [ $RC -ne 0 ]; then
  mkdir -p ~/office/joy/outbox
  TS=$(date +%Y%m%d-%H%M%S)
  cat > ~/office/joy/outbox/mirror-health-${TS}.json <<EOJ
{"to":"feibisi","type":"message","subject":"文风镜像同步告警","content":"$OUT（自动巡检，处置见 font-licenses MIRROR-SOP §2/§3）"}
EOJ
fi
echo "[$(date '+%F %T')] rc=$RC $OUT" >> /tmp/mirror-health.log
