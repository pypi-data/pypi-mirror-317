# setup.py

from setuptools import setup, find_packages

setup(
    name='pdf2test',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],  # 如果有依赖项，可以在这里添加
    author='fetian20',
    author_email='fetian20@qq.com',
    description='A simple package to demonstrate PDF to text conversion',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pdf2test',  # 替换为你的GitHub仓库链接
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
