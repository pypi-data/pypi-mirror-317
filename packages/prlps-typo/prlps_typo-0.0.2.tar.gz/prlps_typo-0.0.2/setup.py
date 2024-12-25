from setuptools import find_packages, setup

setup(
    name='prlps_typo',
    version='0.0.2',
    author='prolapser',
    packages=find_packages(),
    url='https://github.com/gniloyprolaps/prlps_typo',
    license='LICENSE.txt',
    description='исправление типографии в Markdown и HTML',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=['py_mini_racer', 'html2text', 'mistune', 'httpx'],
    package_data={
        'prlps_typo': ['typograf.js'],
    },
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)