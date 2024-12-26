from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ecsm-tool",
    version="0.0.2",
    license="MIT",
    description="ECSM TOOLS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="liuyang.z",
    author_email="chalks_arrival.0i@icloud.com",
    keywords=["ECSM", "TOOLS", "API"],
    packages=find_packages(),
    install_requires=[
        'requests>=2.32.3',
        'tqdm>=4.67.1',
    ],
    entry_points={
        "console_scripts": [
            "ecsm-tool = ecsm_tool.main:main",
        ],
    },
)
