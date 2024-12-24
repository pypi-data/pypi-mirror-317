from setuptools import setup, find_packages

setup(
    name='my_packagefetian',  # 包的名称，要保证唯一性，最好在PyPI上还没被使用过
    version='0.1.0',  # 包的版本号，每次更新功能后可以适当递增版本号
    author='fetian20',  # 你的名字或者组织名称
    author_email='your_email@example.com',  # 联系邮箱
    description='A simple example package',  # 对包的简短描述
    packages=find_packages(),  # 自动查找项目中的所有包（通过识别包含 __init__.py 的目录）
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # 分类器，用于描述包支持的Python版本、许可证类型等信息，方便用户筛选查找
    python_requires='>=3.9',  # 声明支持的最低Python版本要求
)
