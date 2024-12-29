from setuptools import setup, find_packages

setup(
    name="easy_geotool",
    version="0.1.2",
    author="JeasunLok",
    author_email="luojsh7@mail2.sysu.edu.cn",
    description="An easy geospatial data processing tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JeasunLok/easy_geotool",
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  # 自动查找所有子包
    python_requires=">=3.9",
    install_requires=open("requirements.txt").read().splitlines(),  # 从 requirements.txt 读取依赖
)
