from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf - 8') as f:
    long_description = f.read()

setup(
    name='excel2vcf',
    version='1.0.2',
    description='Making vcard files from excel files.通过 excel 文件生成可导入手机的 vcard 文件',
    author='htiger',
    author_email='huangtg332052@163.com',
    long_description = long_description,
    long_description_content_type='text/markdown',
    platforms='any',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    package_data={"htiger": ["*.ini", "*.xlsx"]},
    install_requires=[
        'numpy>=1.24.4',
        'openpyxl>=3.1.5',
        'pandas>=2.0.3',
        'xlrd >= 2.0.1'
    ],
    entry_points={
        'console_scripts': [
          'excel2vcf = htiger.excel2vcf:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ]
)