from setuptools import setup, find_packages

setup(
    name="chatbot-gpt2",  # Your package name (must be unique on PyPI)
    version="0.1.0",    # Initial version
    author="Rahul Kumar Bharti",
    author_email="rahul_kbharti2002@gmail.com",
    description="Chatbot package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",  # Project URL
    packages=find_packages(),  # Automatically find package directories
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose an appropriate license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # List dependencies, e.g., "numpy>=1.18.0"
    ],
)
