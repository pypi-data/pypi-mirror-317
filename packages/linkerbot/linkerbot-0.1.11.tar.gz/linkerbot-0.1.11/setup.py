from setuptools import setup, find_packages

setup(
    name="linkerbot",
    version="0.1.11",
    author="LinkerBot",
    author_email="2424028621@example.com",
    description="灵心巧手相关的SDK",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/linkerbot-sdk",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'tqdm>=4.65.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
