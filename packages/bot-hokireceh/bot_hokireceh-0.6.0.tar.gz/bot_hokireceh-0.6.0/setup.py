from setuptools import setup, find_packages

setup(
    name='bot-hokireceh',
    version='0.6.0',
    description='Bot Telegram untuk komunitas Hoki Receh',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='HokiReceh',
    author_email='ads.hokireceh@gmail.com',
    url='https://codeberg.org/pemulungrupiah/bot-hokireceh',
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot==21.6',
        'aiohttp==3.10.0',
        'python-dotenv==0.21.0',
        'requests==2.26.0',
        'googletrans==4.0.0-rc1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
