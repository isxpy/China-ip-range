import requests
import os
import math

# 下载APNIC的IP数据库文件并保存为apnic.txt
url = "http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
response = requests.get(url)

with open('apnic.txt', 'wb') as f:
    f.write(response.content)

# 筛选数据并写入cnip.txt
with open('apnic.txt', 'r') as infile, open('cnip.txt', 'w') as outfile:
    for line in infile:
        if line.startswith('apnic|CN|ipv4'):
            outfile.write(line)

# ip_data是从cnip.txt读取的数据
with open('cnip.txt', 'r') as file:
    ip_data = file.read().splitlines()

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

cidr_blocks = []
for entry in ip_data:
    parts = entry.split('|')
    network_address = parts[3]
    ip_count = int(parts[4])

    # 检查是否为2的幂次方
    if is_power_of_two(ip_count):
        prefix_length = 32 - int(math.log2(ip_count))
        cidr_block = f"{network_address}/{prefix_length}"
        cidr_blocks.append(cidr_block)
    else:
        print(f"无法直接转换IP数量 {ip_count} 到精确的CIDR掩码，需要进一步处理或估算")

# 如果需要将结果保存到文件cnip-cidr.txt中
with open('cnip-cidr.txt', 'w') as output_file:
    for block in cidr_blocks:
        output_file.write(f"{block}\n")

# 清理：如果不需要原始的apnic.txt文件，可以删除
# os.remove('apnic.txt')
# 清理：如果不需要原始的cnip.txt文件，可以删除
    os.remove('cnip.txt')