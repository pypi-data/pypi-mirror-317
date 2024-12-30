from setuptools import setup

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(
    name='fbchese',
    version='1.0.0',
    author='pozozal',
    author_email='12@mail4.uk',
    description='This is my first module',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://t.me/pozozal',
    packages=['package'], 
    install_requires=['requests>=2.21.0'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='example python',
    project_urls={
        'Documentation': 'https://t.me/pozozal'
    },
    python_requires='>=3.11' 
)
