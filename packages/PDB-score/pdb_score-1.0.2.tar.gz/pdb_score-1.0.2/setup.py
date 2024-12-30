from setuptools import setup, find_packages

setup(
    name="PDB_score",
    version="1.0.2",
    author="SiriNatsume",
    author_email="SiriNatsume@outlook.com",
    description="A tool to massively calculate protein scores using PDB files.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SiriNatsume/PDB-score",  # 如果有 GitHub 仓库
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",  # 数值计算
        "biopython",  # 蛋白质结构分析
    ],
    entry_points={
        "console_scripts": [
            "psc=PDB_score.main:main",  # 设置命令行入口
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license = "MIT",
    python_requires=">=3.6",
)