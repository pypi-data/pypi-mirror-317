from setuptools import setup, find_packages

setup(
    name="heuristic-client",  # Unique name for your package
    version="0.1.0",
    description="A Python client for connecting your llm to the world",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nitya Singh",
    author_email="nityasingh030301@gmail.com",
    url="https://heuristic-mu.vercel.app",  # Optional GitHub URL
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
