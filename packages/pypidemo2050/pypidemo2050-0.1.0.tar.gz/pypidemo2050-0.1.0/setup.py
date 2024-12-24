from setuptools import setup, find_packages

setup(
    name="pypidemo2050",                      # 项目名称
    version="0.1.0",                        # 项目版本
    author="Leo Wang",                     # 作者名
    author_email="your_email@example.com",  # 作者邮箱
    description="A sample Python module",  # 简短描述
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_project",  # 项目主页
    packages=find_packages(),               # 自动发现模块
    classifiers=[                           # 分类标签
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11.5',                # Python 版本要求
    install_requires=[                      # 项目依赖
        "poetry-core",
        "poetry.core.masonry.api"
    ],
)



