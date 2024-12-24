from setuptools import setup, find_packages

setup(
    name="psswrdgen",
    version="1.0.0",
    author="almos05",
    author_email="tenderboylive3@gmail.com",
    description="A simple password generator library.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/almos05/lb_python/tree/main/lb_4/password_generator",
    packages=find_packages(where='password_generator'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[]
)