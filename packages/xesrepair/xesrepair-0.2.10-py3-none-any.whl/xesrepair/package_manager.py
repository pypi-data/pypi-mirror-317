import subprocess
from xesrepair.common import PYTHONW_EXE, USER_LIB_PATH

# 安装库,可以在库名后边用==a.b.c来指定版本，第二个参数mirror可以指定源
# 阿里源：https://mirrors.aliyun.com/pypi/simple/
# 清华源：https://pypi.tuna.tsinghua.edu.cn/simple
# 豆瓣源：https://pypi.douban.com/simple/
# pypi官方源：https://pypi.org/simple
# 学而思私有源：https://codepypi.xueersi.com/simple
def install_package(package_name, mirror=''):
    # 使用pip安装包
    
    cmd = [PYTHONW_EXE, "-m", "pip", "install", "-t", USER_LIB_PATH, "--no-cache-dir", '--no-warn-script-location', "--upgrade", package_name]
    if mirror != '' and mirror is not None:
        cmd.append("-i")
        cmd.append(mirror)
    print(" ".join(cmd))
    subprocess.check_call(cmd)

# 卸载库
def uninstall_package(package_name):
    cmd = [PYTHONW_EXE, "-m", "pip", "uninstall", "-y", package_name]
    subprocess.check_call(cmd)
    
# 查看库版本
def show_package(package_name):
    cmd = [PYTHONW_EXE, "-m", "pip", "show", package_name]
    subprocess.check_call(cmd)
    
if __name__ == "__main__":
    # 安装库
    # install_package("ursina==5.2.0", mirror="https://codepypi.xueersi.com/simple")
    # 卸载库
    # uninstall_package("ursina")
    # 查看库版本
    # show_package("ursina")
    pass

