"""
setup.py
"""
from pathlib import Path
from setuptools import setup, find_packages

def read(file_path):
    """Read and return the contents of a file."""
    return Path(file_path).read_text(encoding='utf-8')

setup(
    name='starlyng_smart_reboot',
    version='0.2.4',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'python-dotenv',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-mock==3.14.0',
            'pylint==3.2.2',
            'twine',
            'wheel',
        ],
    },
    entry_points={
        'console_scripts': [
            'smart_reboot = smart_reboot.__main__:main',
        ],
    },
    author='Justin Sherwood',
    author_email='justin@sherwood.fm',
    description='Manage servers by rebooting using BCM in case of crashes.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/starlyngapp/smart-reboot',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Systems Administration',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
    license='MIT',
    keywords='server management bcm smart reboot',
)
