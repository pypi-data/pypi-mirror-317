from setuptools import setup

setup(
    name="tkvariable",
    version="0.1.0",
    py_modules=["tkvariable"],
    author="Emkay",
    author_email="mkay.py@gmail.com",
    description="Efficient Tkinter variable management with dynamic creation and tracing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/code-with-emkay/tkvariable",  # Update with your GitHub repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
