from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements = fr.read().splitlines()

setup(
    name='ReDATA_README_Tool',
    version='0.3.1',
    packages=['readme_tool'],
    url='https://github.com/UAL-ODIS/ReDATA_README_Tool',
    license='MIT License',
    author='Chun Ly',
    author_email='astro.chun@gmail.com',
    description='A Python web UI built on FastAPI to gather metadata to construct a README',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
