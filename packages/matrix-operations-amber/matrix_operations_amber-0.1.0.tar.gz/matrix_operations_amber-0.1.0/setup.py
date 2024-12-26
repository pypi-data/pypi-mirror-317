from setuptools import setup, find_packages

# 读取README.md文件作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # 包的名称
    name='matrix_operations_amber',

    # 包的版本
    version='0.1.0',

    # 作者
    author='Amber Hou',

    # 作者的联系邮箱
    author_email='1471147972@qq.com',

    # 包的描述
    description='A simple package for matrix operations',

    # 包的长描述，从README.md读取
    long_description=long_description,

    # 长描述的格式，这里指定为markdown
    long_description_content_type='text/markdown',

    # 包的Python版本兼容性
    python_requires='>=3.6',

    # 包含的包和子包
    packages=find_packages(),

    # 包的分类
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],

)