from setuptools import setup, find_packages

setup(
    name='notebookllm',
    version='0.1.0',
    packages=find_packages(),
    py_modules=['cli'],
    install_requires=[
       'nbformat',
       'jupyter_client',
    ],
   entry_points={
        "console_scripts": [
            "notebookllm = cli:main",
        ],
    },
)
