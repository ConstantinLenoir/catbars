import setuptools

with open("README.rst", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="catbars",
    version="1.0.0",
    author="Constantin Yves Lenoir",
    author_email="constantinlenoir@gmail.com",
    description="A plotting library for making horizontal bar charts.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/ConstantinLenoir/catbars",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['matplotlib', 'numpy'],
    python_requires='>=3.8',
)
