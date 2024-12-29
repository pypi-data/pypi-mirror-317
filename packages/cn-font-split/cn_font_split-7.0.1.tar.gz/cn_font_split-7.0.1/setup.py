from setuptools import setup, find_packages

setup(
    name='cn-font-split',
    version='7.0.1',  # Use 'b' for beta
    description='A revolutionary font subsetter that supports CJK and any characters!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KonghaYao/cn-font-split/tree/ts/packages/subsets',
    author='KonghaYao',
    author_email='dongzhongzhidong@qq.com',
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='font converter performance wasm woff2 ttf otf opentype-fonts font-subsetter font-subset cjk',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Adjust as necessary
    install_requires=[  # Include your dependencies here
        'google===3.0.0',
        'protobuf==5.29.2'
    ],
    entry_points={
        'console_scripts': [
            'cn-font-split-py=cn_font_split.cli:main',  # Assuming you have a CLI entry point
        ],
    },
    project_urls={
        'Homepage': 'https://chinese-font.netlify.app/',
        'Source': 'https://github.com/KonghaYao/cn-font-split/tree/ts/packages/subsets',
    },
)