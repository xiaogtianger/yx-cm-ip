import urllib.request
import re
import random

# 配置目标 URL 和需要保留的国家/地区代码
URL = "http://zip.cm.edu.kg/all.txt"
TARGET_COUNTRIES = ["SG", "US", "JP", "KR", "HK"]
MAX_PER_COUNTRY = 20

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
    
    # 初始化一个字典，用于按国家分类存储匹配到的行
    country_groups = {country: [] for country in TARGET_COUNTRIES}

    print("正在分类和筛选 IP 数据...")
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            continue
        
        # 检查当前行属于哪一个指定国家
        for country in TARGET_COUNTRIES:
            if re.search(rf'\b{country}\b', line_strip, re.IGNORECASE):
                country_groups[country].append(line_strip)
                break

    filtered_lines = []
    
    # 对每个国家的数据进行随机抽样
    for country, items in country_groups.items():
        if len(items) > MAX_PER_COUNTRY:
            # 如果数量超过20个，随机抽取20个
            sampled_items = random.sample(items, MAX_PER_COUNTRY)
            print(f"[{country}] 发现 {len(items)} 条数据，已随机保留 {MAX_PER_COUNTRY} 条。")
        else:
            # 如果少于或等于20个，全部保留
            sampled_items = items
            print(f"[{country}] 发现 {len(items)} 条数据，已全部保留。")
            
        filtered_lines.extend(sampled_items)

    # 将最终结果写入本地文件
    output_file = "filtered_ips.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(filtered_lines) + "\n")
    
    print(f"过滤与随机抽样完成！共保存了 {len(filtered_lines)} 条记录到 {output_file}。")

if __name__ == "__main__":
    main()
