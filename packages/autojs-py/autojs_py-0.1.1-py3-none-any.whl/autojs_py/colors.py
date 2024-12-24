def get_rgb(color):
    if isinstance(color, int):
        return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)
    elif isinstance(color, str):
        return get_rgb(Colors.parseColor(color))
    else:
        raise TypeError("Color must be an integer or a hex string.")
class Colors:
    BLACK = 0xFF000000  # 黑色
    DKGRAY = 0xFF444444  # 深灰色
    GRAY = 0xFF888888  # 灰色
    LTGRAY = 0xFFCCCCCC  # 亮灰色
    WHITE = 0xFFFFFFFF  # 白色
    RED = 0xFFFF0000  # 红色
    GREEN = 0xFF00FF00  # 绿色
    BLUE = 0xFF0000FF  # 蓝色
    YELLOW = 0xFFFFFF00  # 黄色
    CYAN = 0xFF00FFFF  # 青色
    MAGENTA = 0xFFFF00FF  # 品红色
    TRANSPARENT = 0x00000000  # 透明
    def __init__(self):
        pass
    @staticmethod
    def toStr(color):
        return '#%02x%02x%02x%02x' % (color[0], color[1], color[2], color[3])
    @staticmethod
    def red(color):
        """
        获取颜色的 R 通道值。

        参数:
        color (number | str): 颜色值，支持数字（0-16777215）或十六进制字符串（例如 '#ff0000'）。

        返回:
        int: 颜色的 R 通道值，范围在 0-255 之间。
        """
        if isinstance(color, int):
            # 从数字中提取 R 通道
            return (color >> 16) & 0xFF  # 提取高8位

        elif isinstance(color, str):
            # 从十六进制字符串中提取 R 通道
            if color.startswith('#'):
                color = color[1:]  # 去掉 '#'
            if len(color) == 6:
                return int(color[0:2], 16)  # 提取前两位并转换为整数
            else:
                raise ValueError("Invalid hex color format. Use '#' followed by 6 hex digits.")

        else:
            raise TypeError("Color must be an integer or a hex string.")

    @staticmethod
    def green(color):
        """
        获取颜色的 G 通道值。

        参数:
        color (number | str): 颜色值，支持数字（0-16777215）或十六进制字符串（例如 '#00ff00'）。

        返回:
        int: 颜色的 G 通道值，范围在 0-255 之间。
        """
        if isinstance(color, int):
            return (color >> 8) & 0xFF  # 提取中间8位（G通道）

        elif isinstance(color, str):
            if color.startswith('#'):
                color = color[1:]  # 去掉 '#'
            if len(color) == 6:
                return int(color[2:4], 16)  # 提取中间两位并转换为整数
            else:
                raise ValueError("Invalid hex color format. Use '#' followed by 6 hex digits.")

        else:
            raise TypeError("Color must be an integer or a hex string.")
    @staticmethod
    def blue(color):
        """
        获取颜色的 B 通道值。

        参数:
        color (number | str): 颜色值，支持数字（0-16777215）或十六进制字符串（例如 '#0000ff'）。

        返回:
        int: 颜色的 B 通道值，范围在 0-255 之间。
        """
        if isinstance(color, int):
            return color & 0xFF  # 提取低8位（B通道）

        elif isinstance(color, str):
            if color.startswith('#'):
                color = color[1:]  # 去掉 '#'
            if len(color) == 6:
                return int(color[4:6], 16)  # 提取最后两位并转换为整数
            else:
                raise ValueError("Invalid hex color format. Use '#' followed by 6 hex digits.")

        else:
            raise TypeError("Color must be an integer or a hex string.")

    @staticmethod
    def alpha(color):
        """
        获取颜色的 Alpha 通道值。

        参数:
        color (number | str): 颜色值，支持数字（0-16777215）或十六进制字符串（例如 '#ff0000'）。

        返回:
        int: 颜色的 Alpha 通道值，范围在 0-255 之间。
        """
        if isinstance(color, int):
            return (color >> 24) & 0xFF  # 提取高8位（Alpha通道）

        elif isinstance(color, str):
            if color.startswith('#'):
                color = color[1:]  # 去掉 '#'
            if len(color) == 8:  # 8位十六进制字符串
                return int(color[0:2], 16)  # 提取前两位并转换为整数
            else:
                return 255  # 默认不透明

        else:
            raise TypeError("Color must be an integer or a hex string.")

    @staticmethod
    def rgb(red, green, blue):
        """
        返回由 RGB 通道组成的整数颜色值，Alpha 通道为 255（不透明）。

        参数:
        red (number): 颜色的 R 通道的值
        green (number): 颜色的 G 通道的值
        blue (number): 颜色的 B 通道的值

        返回:
        int: 由 RGB 通道构成的整数颜色值。
        """
        return (255 << 24) | (red << 16) | (green << 8) | blue

    @staticmethod
    def argb(alpha, red, green, blue):
        """
        返回由 ARGB 通道组成的整数颜色值。

        参数:
        alpha (number): 颜色的 Alpha 通道的值
        red (number): 颜色的 R 通道的值
        green (number): 颜色的 G 通道的值
        blue (number): 颜色的 B 通道的值

        返回:
        int: 由 ARGB 通道构成的整数颜色值。
        """
        return (alpha << 24) | (red << 16) | (green << 8) | blue


    @staticmethod
    def parseColor(colorStr):
        """
        解析颜色字符串，并返回整数颜色值。

        参数:
        colorStr (str): 表示颜色的字符串，例如 "#112233"

        返回:
        int: 颜色的整数值。
        """
        if colorStr.startswith('#'):
            colorStr = colorStr[1:]  # 去掉 '#'
        if len(colorStr) == 6:
            return (255 << 24) | (int(colorStr[0:2], 16) << 16) | (int(colorStr[2:4], 16) << 8) | int(colorStr[4:6], 16)
        elif len(colorStr) == 8:
            return (int(colorStr[0:2], 16) << 24) | (int(colorStr[2:4], 16) << 16) | (
                        int(colorStr[4:6], 16) << 8) | int(colorStr[6:8], 16)
        else:
            raise ValueError("Invalid hex color format. Use '#' followed by 6 or 8 hex digits.")

    @staticmethod
    def isSimilar(color1, color2, threshold=4, algorithm="diff"):
        """
        判断两个颜色是否相似。

        参数:
        color1 (number | str): 颜色值1
        color2 (number | str): 颜色值2
        threshold (number): 相似度临界值，默认为4
        algorithm (str): 颜色匹配算法，默认为"diff"

        返回:
        bool: 是否相似。
        """

        r1, g1, b1 = get_rgb(color1)
        r2, g2, b2 = get_rgb(color2)

        if algorithm == "diff":
            return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2) < threshold
        elif algorithm == "rgb":
            return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5 <= threshold
        elif algorithm == "rgb+":
            # 这里可以实现 LAB Delta E 距离计算
            raise NotImplementedError("Algorithm 'rgb+' is not implemented.")
        elif algorithm == "hs":
            # 这里可以实现 HSV 欧拉距离匹配
            raise NotImplementedError("Algorithm 'hs' is not implemented.")
        else:
            raise ValueError("Invalid algorithm specified.")

    @staticmethod
    def equals(color1, color2):
        """
        判断两个颜色是否相等（忽略 Alpha 通道）。

        参数:
        color1 (number | str): 颜色值1
        color2 (number | str): 颜色值2

        返回:
        bool: 是否相等。
        """
        r1, g1, b1 = ((color1 >> 16) & 0xFF, (color1 >> 8) & 0xFF, color1 & 0xFF) if isinstance(color1,
                                                                                                int) else get_rgb(
            Colors.parseColor(color1))
        r2, g2, b2 = ((color2 >> 16) & 0xFF, (color2 >> 8) & 0xFF, color2 & 0xFF) if isinstance(color2,
                                                                                                int) else get_rgb(
            Colors.parseColor(color2))
        return r1 == r2 and g1 == g2 and b1 == b2

