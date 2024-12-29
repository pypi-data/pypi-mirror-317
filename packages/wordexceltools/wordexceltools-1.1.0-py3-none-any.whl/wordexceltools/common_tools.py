# coding=utf-8
"""
@File   :common_tools.py
@Time   :2024/12/28 14:14 15:20
@Author :Sunmy
@Description: 通用工具类
"""

import os
from datetime import datetime

import chardet


def common_int_to_roman(number: int) -> str:
    """
    将整数转换为罗马数字。
    :param number: int, 要转换的正整数（范围 1-3999）。
    :return: str, 转换后的罗马数字表示。
    """
    try:
        # 罗马数字映射表
        roman_numerals = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]

        if number <= 0 or number >= 4000:
            raise ValueError("Number must be between 1 and 3999.")

        roman_result = []
        for value, symbol in roman_numerals:
            while number >= value:
                roman_result.append(symbol)
                number -= value

        return "".join(roman_result)
    except ValueError as ve:
        print(f"Invalid input in int_to_roman: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred in int_to_roman: {e}")


def common_count_files_in_folders(directory: str) -> dict:
    """
    统计目录下每个文件夹中包含的文件数量。
    :param directory: str, 要统计的目录路径。
    :return: dict, 文件夹路径为键，文件数量为值。
    """
    folder_counts = {}

    # 将目录路径转换为绝对路径
    directory = os.path.abspath(directory)

    # 遍历目录及其子目录
    for root, _, files in os.walk(directory):
        folder_counts[os.path.abspath(root)] = len(files)

    return folder_counts


def common_get_file_encoding(file_path: str) -> str:
    """
    检测文件的编码格式。
    :param file_path: str, 文件路径。
    :return: str, 检测到的文件编码格式。如果检测失败，返回 "unknown"。
    """
    try:
        # 打开文件并读取所有字节数据
        with open(file_path, "rb") as file:
            data = file.read()

        # 如果文件为空，返回 unknown
        if not data:
            print(f"Warning: The file '{file_path}' is empty.")
            return "unknown"

        # 使用 chardet 检测编码
        result = chardet.detect(data)
        encoding = result.get("encoding")

        # 如果未检测到编码，返回 unknown
        if not encoding:
            print(f"Warning: Encoding detection failed for file '{file_path}'.")
            return "unknown"

        return encoding

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
        return "unknown"
    except Exception as e:
        print(f"Error in get_file_encoding(file_path): {str(e)}")
        return "unknown"


def common_verify_folder_empty(folder_path: str) -> bool:
    """
    检查文件夹是否为空。
    :param folder_path: 文件夹路径。
    :return: 如果是空文件夹，返回 True；如果不是文件夹或非空，返回 False。
    """
    try:
        # 检查路径是否存在
        if not os.path.exists(folder_path):
            print(f"Error: The folder path '{folder_path}' does not exist.")
            return False

        # 检查路径是否为文件夹
        if not os.path.isdir(folder_path):
            print(f"Error: The path '{folder_path}' is not a valid directory.")
            return False

        # 检查文件夹内容是否为空
        return len(os.listdir(folder_path)) == 0

    except Exception as e:
        print(f"Error while validating folder: {str(e)}")
        return False


def common_get_files_path(folder_path, recursive=True, include_files=False):
    """
    遍历并输出所有文件夹或文件的路径。
    :param folder_path: 要遍历的文件夹路径。
    :param recursive: 是否递归遍历子目录，默认为True。
    :param include_files: 是否包含文件路径，默认为False，仅包含文件夹路径。
    :return: 路径列表，根据深度排序。
    """
    if not os.path.exists(folder_path):
        print(f"Error: The folder path '{folder_path}' does not exist.")
        return []

    path_list = []

    if recursive:
        # 递归遍历所有子目录和文件
        for root, dirs, files in os.walk(folder_path):
            # 如果需要包含文件
            if include_files:
                for file_name in files:
                    full_path = os.path.join(root, file_name)
                    abspath = os.path.abspath(full_path)
                    path_list.append(abspath)
            # 如果只需要包含文件夹
            else:
                for dir_name in dirs:
                    full_path = os.path.join(root, dir_name)
                    abspath = os.path.abspath(full_path)
                    path_list.append(abspath)
    else:
        # 仅遍历当前目录中的文件夹或文件
        if include_files:
            for file_name in os.listdir(folder_path):
                full_path = os.path.join(folder_path, file_name)
                if os.path.isfile(full_path):  # 确保是文件
                    abspath = os.path.abspath(full_path)
                    path_list.append(abspath)
        else:
            for dir_name in os.listdir(folder_path):
                full_path = os.path.join(folder_path, dir_name)
                if os.path.isdir(full_path):  # 确保是文件夹
                    abspath = os.path.abspath(full_path)
                    path_list.append(abspath)

    # 根据路径深度排序，深度越大的路径排在前面
    return sorted(path_list, key=lambda x: x.count(os.sep), reverse=True)


def common_verify_positive_integer(value):
    """
    验证输入是否为正整数。如果为空或无效，则返回0或None。
    :param value: 输入的值，可以是字符串或整数。
    :return: 返回正整数，如果输入无效则返回 None；如果为空，则返回0。
    """
    if isinstance(value, int):  # 如果已经是整数，直接返回
        if value >= 0:
            return value
        else:
            print("Error: Please enter a positive integer.")
            return None
    elif isinstance(value, str):  # 如果是字符串，继续验证
        value = value.strip()
        if value == "":  # 处理回车直接输入的情况
            return 0
        try:
            val = int(value)
            if val >= 0:
                return val
            else:
                print("Error: Please enter a positive integer.")
                return None
        except ValueError:
            print("Error: Please enter a valid integer.")
            return None
    else:
        print("Error: Invalid input type. Expected a string or integer.")
        return None


def common_verify_file_exist(path: str) -> bool:
    """
    检查文件是否存在且为文件。
    :param path: str, 文件路径。
    :return: bool, 如果文件存在且为文件，返回 True；否则返回 False。
    """
    return os.path.isfile(path)


def common_verify_folder_exist(path: str) -> bool:
    """
    检查文件夹是否存在且为目录，若不存在则创建。
    :param path: str, 文件夹路径。
    :return: bool, 如果文件夹存在或成功创建，返回 True；如果路径存在但不是目录，返回 False。
    """
    if os.path.isdir(path):
        return True  # 路径存在且是目录

    if os.path.exists(path) and not os.path.isdir(path):
        print(f"Error: The path '{path}' exists but is not a directory.")
        return False  # 路径存在但不是目录

    try:
        os.makedirs(path)  # 自动创建文件夹
        return True
    except OSError as e:
        print(f"Error: Failed to create directory '{path}'. Reason: {e}")
        return False


def common_copy_file(source: str, file_type: str, suffix: str = "") -> str:
    """
    根据源文件路径生成带时间戳和可选后缀的新文件路径。
    :param source: str, 源文件路径（可能是相对路径或绝对路径）。
    :param file_type: str, 新文件的扩展名。
    """
    # 获取绝对路径
    abs_file_path = os.path.abspath(source)

    # 分离目录和文件名
    dir_name, file_name = os.path.split(abs_file_path)

    # 去掉文件扩展名
    base_name, _ = os.path.splitext(file_name)

    # 获取当前时间
    time_stamp = common_now_time()

    # 添加后缀
    suffix_part = f"_{suffix}" if suffix else ""

    # 生成新的文件名
    new_file_name = f"{base_name}_{time_stamp}{suffix_part}.{file_type}"

    # 拼接成完整路径
    new_file_path = os.path.join(dir_name, new_file_name)

    # 检查文件是否存在
    if not os.path.exists(new_file_path):
        # 如果文件不存在，创建新文件
        with open(new_file_path, "w") as file:
            file.write("")  # 写入空内容

    return new_file_path


def common_verify_license_expiry(license_count, license_date, count: int) -> bool:
    """
    验证 license 次数还有 license 时间是否有效
    :param license_count: 许可证到期次数验证，common_verify_license_count的返回值。
    :param license_date: 许可证到期日期验证，common_verify_license_date的返回值。
    :param count: license 的可使用次数。
    :return: license的验证结果。如果操作失败，返回 False。
    """
    if license_count > count or license_date < 0:
        return False
    else:
        return True


def common_verify_license_date(license_time: str) -> int:
    """
    检查许可证是否过期，并返回剩余的天数。
    :param license_time: 许可证到期日期，格式为 'YYYYMMDD' 的字符串，例如 '20250430'。
    :return: 剩余的天数。如果许可证已过期，返回 -1；如果解析失败，返回 -2。
    """
    try:
        # 将传入的时间参数解析为日期时间对象
        license_date = datetime.strptime(license_time, "%Y%m%d")
        # 获取当前时间
        current_time = datetime.now()
        # 如果传入的时间早于或等于当前日期，则返回 -1 表示已过期
        if license_date <= current_time:
            return -1
        # 计算剩余天数并返回
        remaining_days = (license_date - current_time).days
        return remaining_days
    except ValueError as e:
        print(f"Error in get_license_date(): Invalid date format. {str(e)}")
        return -2
    except Exception as e:
        print(f"Error in get_license_date(): {str(e)}")
        return -2


def common_verify_license_count() -> int:
    """
    创建系统 license 存储文件，并返回文件中的记录数。
    :return: 文件中的记录数。如果操作失败，返回 -1。
    """
    try:
        # 获取当前系统用户的根目录
        home_dir = os.path.expanduser("~")
        # 构建隐藏目录的路径
        hidden_dir_path = os.path.join(home_dir, ".Tools")
        # 创建隐藏目录
        os.makedirs(hidden_dir_path, exist_ok=True)
        # 构建隐藏文件的路径和文件名
        hidden_file_path = os.path.join(hidden_dir_path, ".license")
        # 获取当前时间
        current_time = datetime.now()
        # 格式化时间为字符串
        use_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        # 创建或追加写入隐藏文件
        with open(hidden_file_path, "a+") as file:
            file.write(f"use time: {use_time}\n")
        # 读取隐藏文件并统计行数
        with open(hidden_file_path, "r") as file:
            lines = file.readlines()
            line_count = len(lines)
            return line_count
    except Exception as e:
        print(f"Error in get_license_count(): {str(e)}")
        return -1


def common_clean_text(text: str) -> str:
    """
    清理文本，去除多余的空格、零宽字符、换行符和回车符。
    :param text: 待清理的文本。
    :return: 清理后的文本。
    :raises ValueError: 如果输入不是字符串类型。
    """
    if not isinstance(text, str):
        raise ValueError("输入必须是字符串")
    return (
        text.strip()
        .replace(" ", "")
        .replace("\u200b", "")
        .replace("\n", "")
        .replace("\r", "")
    )


def common_now_time() -> str:
    """
    获取当前时间并格式化为字符串。
    :return: 格式化的当前时间字符串，格式为 'YYYYMMDD_HHMMSS'。
    """
    now = datetime.now()
    formatted_time = now.strftime("%Y%m%d_%H%M%S")
    return formatted_time


def common_remove_duplicates(lists) -> list:
    """
    列表数据去重转换为集合
    :param lists: 要转换的列表数据
    :return: 去除重复元素，且保持原始顺序的列表
    """
    return list(dict.fromkeys(lists))
