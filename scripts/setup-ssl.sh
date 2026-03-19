#!/bin/bash
# SSL 证书申请脚本

echo "🚀 申请 Let's Encrypt SSL 证书 for clawmate.cloud"
echo "================================================"
echo ""

# 检查 DNS 是否生效
echo "⏳ 等待 DNS 生效..."
echo "当前 DNS 解析结果："
nslookup clawmate.cloud 8.8.8.8 2>/dev/null || echo "DNS 尚未完全生效，可能需要等待 10-60 分钟"
echo ""

# 申请证书（HTTP 验证）
echo "📜 正在申请 SSL 证书..."
certbot certonly --standalone \
  -d clawmate.cloud \
  -d www.clawmate.cloud \
  --agree-tos \
  --non-interactive \
  --email your-email@example.com \
  2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SSL 证书申请成功！"
    echo "证书位置："
    echo "  - /etc/letsencrypt/live/clawmate.cloud/fullchain.pem"
    echo "  - /etc/letsencrypt/live/clawmate.cloud/privkey.pem"
else
    echo ""
    echo "❌ 证书申请失败，可能原因："
    echo "  1. DNS 尚未完全生效（请等待 10-60 分钟）"
    echo "  2. 80 端口被占用"
    echo "  3. 防火墙阻止了访问"
fi
