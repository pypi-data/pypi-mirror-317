from setuptools import setup


with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name='nashx',
    version='0.2',
    packages=['nashx'],
    entry_points={
        'console_scripts': [
            'nashx = nashx.hasher:main'
        ]
    },
    install_requires=[],
    long_description=description,
    long_description_content_type="text/markdown",
    author='Naman Agnihotri',
    author_email='namanagnihotri280@gmail.com',
    url='https://github.com/Naman7214/NASHX.git',
)
