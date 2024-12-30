from setuptools import setup, find_packages

setup(
    name='discord-lite',
    version='0.1.0',
    author='rainy58',
    author_email='yhg4908@kakao.com',
    description='A lightweight Discord bot API library.',
    long_description=open('README.md').read() if open('README.md', 'r').read() else '',
    long_description_content_type='text/markdown',
    project_urls={
        "Documentation": "https://github.com/yhg4908/discord-lite/wiki",
        "Issues": "https://github.com/yhg4908/discord-lite/issues",
        "Repository": "https://github.com/yhg4908/discord-lite",
    },
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.11.11",
        "websockets>=14.1"
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    python_requires='>=3.7',
    package_data={'': ['LICENSE', 'README.md', 'requirements.txt']},
    keywords='discord bot discordbot lite discord-lite lightweight http websockets api',
)
