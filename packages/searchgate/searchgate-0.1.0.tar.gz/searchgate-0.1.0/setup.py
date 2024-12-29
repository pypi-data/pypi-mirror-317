from setuptools import setup, find_packages

setup(
    name='searchgate', 
    version='0.1.0',
    description='A simple package to perform searches using different search engines.',  # 简短描述
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Irid',  # 作者名
    author_email='irid.zzy@gmail.com',  # 作者邮箱
    url='https://github.com/iridesc/searchgate',  # 项目主页
    packages=find_packages(),  # 自动发现所有包和子包
    install_requires=[
        'requests',  # 依赖项
        'bs4'
    ],
    license='MIT',
    classifiers=[
    ],
)
