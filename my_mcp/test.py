import uuid


def get_mac_address():
    """获取 MAC 地址"""
    # 获取节点的 MAC 地址（48位正整数）
    mac = uuid.getnode()
    print(mac)
    # mac是MAC 地址的十进制整数形式，格式化为标准的 MAC 地址格式（如：00:1A:2B:3C:4D:5E）
    mac_hex = ':'.join(('{:012x}'.format(mac))[i:i + 2] for i in range(0, 12, 2))
    return mac_hex


# 使用
mac = get_mac_address()
print(f"MAC 地址: {mac}")
# uuid.getnode() 只返回“一个” MAC 地址，而你的电脑有 3 个网卡，它只挑了其中一个。
# 它挑的规则是“随机”或“第一个能用的”，并不是“全部”。