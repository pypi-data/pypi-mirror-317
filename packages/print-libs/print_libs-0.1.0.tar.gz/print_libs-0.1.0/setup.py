from setuptools import setup, find_packages

# 读取 requirements.txt 文件
# def read_requirements():
#     with open('requirements.txt') as f:
#         return f.read().splitlines()

setup(
    name='print_libs',                   # 工具库的名称
    version='0.1.0',                       # 版本号
    description='用于修饰输出',     # 简短描述
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Z X H',                    # 作者
    author_email='your_email@example.com', # 作者邮箱
    url='https://github.com/your_user/your_project', # 项目主页地址
    packages=find_packages(),              # 自动发现包
    include_package_data=True,             # 包含静态文件
    # install_requires=read_requirements(),  # 从 requirements.txt 加载依赖
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',               # Python 版本要求
    # entry_points={
    #     'console_scripts': [
    #         'your_command=your_package.module1:main_function' # 定义命令行工具
    #     ]
    # },
)



## 运行setuf.py 为项目构建whl
# python setup.py sdist bdist_wheel
## twine upload dist/* 上传到PIP PYPI 需要注册账号

## 本地安装
# pip install 本地目录指向构建的whl




