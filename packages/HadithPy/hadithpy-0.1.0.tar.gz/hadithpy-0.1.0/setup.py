from setuptools import setup, find_packages

setup(
    name="HadithPy",
    version="0.1.0",
    description="A simple and advanced library for searching and managing Hadiths (Prophet sayings)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Ahmed Negm",
    author_email="a7mednegm.x@gmail.com",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: Arabic",
    ],
    python_requires='>=3.6',
)