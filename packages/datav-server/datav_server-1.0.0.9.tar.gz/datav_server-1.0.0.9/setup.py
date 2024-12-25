from setuptools import setup, find_packages

setup(
    name='datav_server',
    version='1.0.0.9',
    description='datav爬取数据通用组件服务端',
    author='python之父·博思之光·杨瑞',
    packages=find_packages(),
    install_requires=[
        'sqlparse',
        'Flask==2.2.5',
        'PyMySQL==1.0.2'
    ],
)