# __init__.py

import os

def get_dll_paths():
    # 获取当前文件所在的目录
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # DLL 目录
    dll_dir = os.path.join(base_dir, 'dll')

    # 初始化字典
    dll_paths = {}

    # 遍历 DLL 目录下的所有版本目录
    for version in os.listdir(dll_dir):
        version_dir = os.path.join(dll_dir, version)
        if os.path.isdir(version_dir):
            dll_file = os.path.join(version_dir, 'LibreHardwareMonitorLib.dll')
            if os.path.isfile(dll_file):
                dll_paths[version] = dll_file

    # 获取最新版本的路径
    if dll_paths:
        latest_version = sorted(dll_paths.keys())[-1]
        dll_paths['latest'] = dll_paths[latest_version]
        dll_paths['latest_version'] = latest_version

    # HidSharp.dll 目录
    HidSharp_dll_dir = os.path.join(dll_dir, "HidSharp.dll")
    dll_paths['HidSharp'] = HidSharp_dll_dir

    return dll_paths

# 只导出 dll 变量
dll = get_dll_paths()

# 清理命名空间，确保只有 dll 变量被导出
del os
del get_dll_paths
