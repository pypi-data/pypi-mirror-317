from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyhurl',
    version='1.0.7',
    description='A set of useful functions that I use in projects.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Rongliang Hu',
    author_email='hurongliang@gmail.com',
    packages=find_packages(),
    install_requires=[
        "pymysql",
        "python-dotenv",
        "oss2",
        "openai",
        "ollama"
    ],
    license='MIT',
    url='https://github.com/hurongliang/pyhurl',
    python_requires='>=3.8',
)