from setuptools import setup, find_packages 

setup(
    name= "lensedGW", # 包名，发布后可用 pip 安装
    version= "1.0.1", # 版本号
    description="lensed waveform for point mass model",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/addone", # 你的项目地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entrypoints={
        "console_scripts": [
            "lensedGW=lensed_waveform.main:lensed_fd_waveform", # 将 `addone` 命令行映射到 `add_one` 函数
        ],
    },
)
