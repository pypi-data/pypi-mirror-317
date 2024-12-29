from setuptools import setup, find_packages

setup(
    name="aihcx",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click>=8.0",  # 使用较新版本的 Click
        "requests>=2.0.0",
        "tabulate>=0.8.0",
        "click-completion>=0.5.2",
        "pyyaml>=5.1",
        "bce-python-sdk-next>=100.9.19.19"
    ],
    entry_points={
        "console_scripts": [
            "aihcx=aihcx.cli:cli",
        ],
    },
    description="AI训练平台命令行工具",
    author="Baidu AIHC Team",
    python_requires=">=3.6",
    package_data={
        'aihcx': ['py.typed', '*.pyi'],
    },
)