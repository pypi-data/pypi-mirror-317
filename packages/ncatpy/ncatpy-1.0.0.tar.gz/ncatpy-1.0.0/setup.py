import setuptools
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="ncatpy",
    version="1.0.0",
    author="木子",
    author_email="2793415370@qq.com",
    description="基于Napcat.QQ开发的pythonsdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liyihao1110/NcatBot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        'websockets',
        'requests',
        'aiohttp',
        'PyYAML',
        'httpx',
    ]
)