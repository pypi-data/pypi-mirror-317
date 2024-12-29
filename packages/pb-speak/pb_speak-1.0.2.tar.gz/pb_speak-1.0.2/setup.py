from setuptools import setup, find_packages

setup(
    name="pb_speak",  # Package name
    version="1.0.2",  # Initial version
    description="A customizable text-to-speech Python library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Priyanshu Bhatt",
    author_email="priyanshubhatt80@gmail.com",  # Replace with your email
    url="https://github.com/FalconX80/pb_speak",  # Replace with your GitHub URL
    license="MIT",
    packages=find_packages(),
    install_requires=["pyttsx3"],  # Add any dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
