from setuptools import setup, find_packages

setup(
    name="wallet-pysdk",                 # 包的名称
    version="1.0.1",                   # 版本号
    author="JZ浩",                # 作者
    author_email="walletcloud88@gmail.com",  # 作者邮箱
    description="open api",  # 简短描述
    long_description=open("README.md").read(),  # 从 README 文件中读取长描述
    long_description_content_type="text/markdown",  # 长描述内容类型
    url="https://github.com/walletcloud88/pysdk",  # 项目主页
    packages=find_packages(),          # 自动发现所有子包
    classifiers=[                      # 分类信息
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',           # 支持的最低 Python 版本
    install_requires=[                 # 依赖包列表
        "pycryptodome>=3.21.0",
        "requests>=2.32.3",
    ],
)
