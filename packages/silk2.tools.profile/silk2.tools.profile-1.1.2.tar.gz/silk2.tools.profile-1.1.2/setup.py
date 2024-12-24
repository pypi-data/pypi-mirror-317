'''
Setup file for SOPHON
'''

import os
import shutil
from distutils.core import setup, Extension
from setuptools import find_packages


if __name__ == "__main__":

    current_folder = os.path.dirname(os.path.abspath(__file__))
    dst_path=os.path.join(current_folder,"SILK2/Tools/profile")
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
    os.makedirs(dst_path,exist_ok=True)

    shutil.copy(os.path.join(current_folder,"__init__.py"), dst_path)
    shutil.copy(os.path.join(current_folder,"__main__.py"), dst_path)
    shutil.copy(os.path.join(current_folder,"log_profile.py"), dst_path)

    filehandle = open(os.path.join(current_folder,"../../git_version"),"r")
    git_version = filehandle.readline().rstrip("\n").rstrip("\r")

    # SILK2 python module
    PACKAGES = ['SILK2']
    module_name = "silk2.tools.profile"

    # wrap SILK2 python module
    setup(name=module_name,
        version=git_version,
        description='Profile using Performance logs.',
        author='zhiju.huang',
        author_email='zhiju.huang@sophgo.com',
        url='https://github.com/sophgo',
        license='BSD',
        long_description='''
            Analyze performance bottlenecks using Performance logs.
        ''',
        packages=PACKAGES,
        install_requires=[
            "numpy",
            "pyecharts",
            "bs4"
        ],
        classifiers=[
            "Programming Language :: Python :: 3",  # 支持的 Python 版本
            "License :: OSI Approved :: BSD License",  # 许可证分类（改为 BSD）
            "Operating System :: POSIX :: Linux",  # 兼容的操作系统
        ],
        python_requires=">=3.6", 
        include_package_data=True)

        

