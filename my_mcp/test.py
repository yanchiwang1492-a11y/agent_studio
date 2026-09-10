import uuid


def get_mac_address():
    """获取 MAC 地址"""
    # 获取节点的 MAC 地址（48位正整数）
    mac = uuid.getnode()
    # 格式化为标准的 MAC 地址格式（如：00:1A:2B:3C:4D:5E）
    mac_hex = ':'.join(('{:012x}'.format(mac))[i:i + 2] for i in range(0, 12, 2))
    return mac_hex


# 使用
mac = get_mac_address()
print(f"MAC 地址: {mac}")