import os
import platform
import subprocess


def run(args=None):
    """调用工具的入口，兼容 MacOS 和 Windows 多平台多架构"""
    binary_name = "deploy"  # 默认的二进制文件名称

    # 获取操作系统和架构信息
    system = platform.system().lower()  # 操作系统名称 (windows, darwin, linux)
    arch = platform.machine().lower()   # CPU 架构 (x86_64, arm64, etc.)

    # 根据操作系统和架构拼接二进制文件名
    if system == "windows":
        binary_name += f"_windows_{arch}.exe"
    elif system == "darwin":  # MacOS 的系统名是 darwin
        binary_name += f"_macos_{arch}"
    elif system == "linux":
        binary_name += f"_linux_{arch}"
    else:
        raise OSError(f"Unsupported operating system: {system}")

    # 获取二进制文件路径
    binary_path = os.path.join(os.path.dirname(__file__), binary_name)

    # 检查二进制文件是否存在
    if not os.path.exists(binary_path):
        raise FileNotFoundError(f"Binary file not found: {binary_path}")

    # 构建并运行命令
    command = [binary_path] + (args or [])
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True  # 自动抛出非零退出码异常
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed with error: {
                           e.stderr.strip()}") from e
