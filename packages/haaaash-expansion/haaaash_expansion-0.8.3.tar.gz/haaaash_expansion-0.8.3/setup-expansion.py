from setuptools import setup, find_packages

filepath = 'README.md'

setup(
    name='haaaash-expansion',
    version='0.8.3',
    author='Gudupao',
    author_email='official@gudupao.top',
    description='hash 批量计算器 高级版',
    long_description=open(filepath, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'PySide6>=6.5.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    
    ],
    entry_points={
        'console_scripts': [
            'haaaash=haaaash.__main__:main',
        ],
    },
)