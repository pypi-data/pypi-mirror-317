from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r', encoding="utf8") as f:
        return f.read()
setup(
    name='math_formulas',
    version='1.0.0',
    author='Yugay A.V.',
    author_email='knifecalledlust33@gmail.com',
    description='',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages('.'),
    install_requires=[''],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='example, math',
    project_urls={
    },
    python_requires='>=3.7'
)