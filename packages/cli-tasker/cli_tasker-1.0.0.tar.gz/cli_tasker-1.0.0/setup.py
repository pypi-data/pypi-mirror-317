from setuptools import setup, find_packages

setup(
    name="cli-tasker",                 # 包名
    version="1.0.0",                     # 版本號
    author="呂佳晏",                      # 作者名
    author_email="jojojo22845@gmail.com", # 作者 Email
    description="A simple CLI task tracker",
    long_description=open("README.md").read(),  # 從 README.md 中提取說明
    long_description_content_type="text/markdown",
    url="https://github.com/luyan0422/cli-tasker",  # GitHub 項目地址
    packages=find_packages(),            # 自動查找所有子包
    include_package_data=True,           # 包括非 Python 文件（如 JSON）
    install_requires=["tabulate"],       # 依賴項列表
    entry_points={
        "console_scripts": [
            "cli-tasker=cli_tasker.cli:main",  # 將命令行工具綁定到 cli.py 的 main 函數
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",             # 兼容的 Python 版本
)
