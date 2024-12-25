from setuptools import setup, find_packages

setup(
    name="spestly",
    version="0.1.0",
    description="A Python package for generating images using the OdysseyXL models.",
    author="Aayan Mishra",
    author_email="aayan.mishra@proton.me",
    url="https://github.com/Aayan-Mishra/OdysseyXL",
    packages=find_packages(),
    install_requires=[
        "gradio-client",
        "Pillow",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
