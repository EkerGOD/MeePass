import math


def calculate_entropy_from_zxcvbn(zxcvbn_result):
    """
    根据 zxcvbn 的返回结果计算密码的熵。

    参数:
        zxcvbn_result (dict): zxcvbn 的返回结果。

    返回:
        int: 密码的熵（bits）。
    """
    # 获取猜测次数
    guesses = zxcvbn_result.get("guesses", 1)  # 默认值为 1，避免 log(0)
    # 计算熵
    entropy = math.log2(float(guesses))
    # 四舍五入到最近整数
    return int(entropy + 0.5)