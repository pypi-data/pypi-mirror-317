"""
" ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ████████╗██████╗  ██████╗ ███╗   ██╗
" ██║  ██║██║   ██║████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
" ███████║██║   ██║██╔████╔██║███████║   ██║   ██████╔╝██║   ██║██╔██╗ ██║
" ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║   ██║██║╚██╗██║
" ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║
" ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"
"                   Copyright (C) 2023 Humatron, Inc.
"                          All rights reserved.
"""

from setuptools import setup


def readme() -> str:
    with open('README.md', 'r') as f:
        return f.read()


# noinspection HttpUrlsUsage
setup(
    name='humatron-python-sdk',
    version='1.3.11',
    author='Humatron',
    author_email='worker_support@humatron.ai',
    description='SDK library for Humatron developers',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='http://humatron.ai/build/python_worker_sdk',
    packages=[
        'humatron',
        'humatron/worker',
        'humatron/worker/rest',
        'humatron/worker/rest/flask',
        'humatron/channels',
        'humatron/channels/rest'
    ],
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='Humatron python',
    python_requires='>=3.11'
)
