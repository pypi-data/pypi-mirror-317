from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='AILink', 
    version='0.0.7', 
    packages=find_packages(),
    py_modules=['ailink'],
    include_package_data=True,
    url='https://github.com/cador/AILink',
    author='Haolin You',
    author_email='cador.ai@aliyun.com', 
    description='A creative idea involves wrapping the OpenAI library to facilitate seamless connections with domestic large models. This project emerged precisely because large model interfaces are compatible with OpenAI, making it easier to utilize large models compared to traditional methods.', 
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.10',
    install_requires=[
        'openai>=1.58.1',
        'httpx[socks]>=0.28.1'
    ],
)
