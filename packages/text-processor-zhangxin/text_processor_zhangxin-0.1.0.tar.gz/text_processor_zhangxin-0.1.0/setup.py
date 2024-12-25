# setup.py
from setuptools import setup, find_packages

# 使用 utf-8 编码打开 README.md 文件
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='text_processor_zhangxin',
    version='0.1.0',
    description='A package for advanced text processing tasks by zhangxin',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Zhang Xin',
    author_email='2931344238@qq.com',
    url='https://github.com/your_username/text_processor_zhangxin',
    packages=find_packages(),  # 自动查找包目录
    install_requires=[],        # 如果有依赖库，列出在此
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',    # 支持的最低 Python 版本
)
