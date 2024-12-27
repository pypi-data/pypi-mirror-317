from setuptools import setup, find_packages

# 读取README文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="midi-tempo-tools",  # 包名称
    version="0.1.0",  # 版本号
    author="Your Name",  # 作者名
    author_email="your.email@example.com",  # 作者邮箱
    description="A tool for handling MIDI file tempo operations",  # 简短描述
    long_description=long_description,  # 长描述（来自README.md）
    long_description_content_type="text/markdown",
    url="https://github.com/zhaoyu010/midiv",  # 项目URL

    # 包配置
    package_dir={"": "src"},  # 指定包的源目录
    packages=find_packages(where="src"),  # 自动发现所有包

    # 包含非Python文件
    package_data={
        "midi_tempo_tools": ["MidiTempoConverter.jar"],  # 包含JAR文件
    },
    include_package_data=True,

    # Python版本要求
    python_requires=">=3.6",

    # 依赖项
    install_requires=[
        "mido>=1.2.0",
    ],

    # 分类信息
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # 关键词
    keywords="midi, tempo, music, bpm",
)