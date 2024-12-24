import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="stensor",
    version="0.2.0",
    author="ligan",
    author_email="623301032@qq.com",
    description="building deep learning framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/ligan15/stensor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)