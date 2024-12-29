from setuptools import setup, find_packages

setup(
    name="gomailer",
    version="1.0.1",
    packages=find_packages(),
    author="Go-Mailer Limited",
    author_email="info@go-mailer.com",
    description="The Go-Mailer Utility library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
