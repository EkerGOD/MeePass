import os
import re


def verify_dir_path(path):
    """
    判断输入的文件夹路径是否合法，是否包含非法字符
    @param path: 绝对路径
    @return:
    """
    # 将路径中连续的 \ 和 / 替换为一个 \
    path = re.sub(r'[\\/]+', r'\\', path)
    # 判断是否为盘符根目录
    ret = re.match(r'^[a-zA-Z]:[\\/]*?$', path)
    if ret:
        return True, path
    # 判断是否为绝对路径
    if not os.path.isabs(path):
        return False
    # 分离出盘符并判断盘符是否存在
    drive, rest = os.path.splitdrive(path)
    if not os.path.isdir(drive):
        return False
    # 判断路径是否包含非法字符
    ret = re.findall(r'[:*?"<>|]', rest)
    if not ret:
        return True
    else:
        return False