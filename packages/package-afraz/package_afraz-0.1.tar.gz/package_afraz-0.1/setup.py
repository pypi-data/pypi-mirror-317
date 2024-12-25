from setuptools import setup, find_packages

setup(
    name="package_afraz",  # The name of your package
    version="0.1",  # Initial version
    packages=find_packages(),  # Automatically find the packages
    install_requires=[],  # Any dependencies your package has
    author="Afraz Ahmed A",
    author_email="afraz@gmail.com",
    description="Afraz Ahmed A is a Python developer working with QCoDes. We will launch our package very soon.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Afraz/mypackage",  # Your package's repository URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
