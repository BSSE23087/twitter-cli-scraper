from setuptools import setup, find_packages

setup(
    name='twitter-cli-scraper',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver-manager',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'twitter-scraper=scraper.twitter_scraper:main',
        ],
    },
    author='Muhammad Abdullah',
    author_email='muhammadabdullah07014@gmail.com',
    description='A CLI tool for scraping Twitter trends and tweets.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bsse23087/twitter-cli-scraper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
