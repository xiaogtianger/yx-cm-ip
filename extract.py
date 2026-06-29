import urllib.request
import re

# 配置目标 URL 和需要保留的国家/地区代码
URL = "http://zip.cm.edu.kg/all.txt"
TARGET_COUNTRIES = {"SG", "US", "JP", "KR", "HK"}

def main():
    print(f"正在从 {URL} 获取数据...")
    try:
        # 发送请求获取文本内容
        req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"获取数据失败: {e}")
        return

    lines = content.splitlines()
    filtered_lines = []

    print("正在筛选指定国家/地区的 IP 数据...")
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        
        # 匹配逻辑：检查当前行是否包含指定的国家代码
        # 注：此处使用不区分大小写的全字/单词边界匹配，防止误伤（如某域名或备注恰好包含sg）
        # 如果原始文件格式为 "IP SG" 或 "SG,IP"，该正则均可有效过滤
        for country in TARGET_COUNTRIES:
            if re.search(rf'\b{country}\b', line_strip, re.IGNORECASE):
                filtered_lines.append(line_strip)
                break

    # 将结果写入本地文件
    output_file = "filtered_ips.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(filtered_lines) + "\n")
    
    print(f"过滤完成！共保存了 {len(filtered_lines)} 条记录到 {output_file}。")

if __name__ == "__main__":
    main()
