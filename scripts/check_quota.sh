#!/bin/bash
# MiniMax 截图生成监控脚本

cd /root/meetingmate-ai/scripts

echo "🖼️ MiniMax 截图生成器 - $(date)"
echo "===================================="

API_KEY="sk-cp-_smOHtq7w6qYyCQoQQIRl32Y5jiib_WhGpnUB_fsBRQDgjdSEQyD91o7lfk7loLHQ-zycd1heeXjRgzZ7psLv7Xm8_beIpwFoNrVkox0b9tqqvLfhEIdBnw"

# 测试额度是否恢复
echo "检测额度状态..."
resp=$(curl -s -X POST "https://api.minimaxi.com/v1/image_generation" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "image-01",
    "prompt": "test",
    "aspect_ratio": "1:1"
  }' 2>/dev/null)

status_code=$(echo "$resp" | grep -o '"status_code":[0-9]*' | cut -d':' -f2)

if [ "$status_code" = "0" ]; then
    echo "✅ 额度已恢复!"
    echo "开始生成5张产品截图..."
    python3 generate_screenshots.py
else
    msg=$(echo "$resp" | grep -o '"status_msg":"[^"]*"' | cut -d'"' -f4)
    echo "⏳ 额度未恢复: $msg"
    echo "下次检测: 10分钟后"
fi
