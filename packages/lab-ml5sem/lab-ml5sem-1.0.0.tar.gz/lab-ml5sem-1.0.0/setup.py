from setuptools import setup, find_packages

setup(
    name='lab-ml5sem',
    version='1.0.0',
    description='A package for data visualization and machine learning helper functions.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Rohit Iyengar',
    author_email='rohitiyengar8@gmail.com',
    url='https://github.com/Rohitlyengar/lab_ml',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'seaborn',
        'numpy',
        'matplotlib',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    license='MIT',
    keywords='machine-learning data-visualization helpers',
    project_urls={
        'Source': 'https://github.com/Rohitlyengar/lab_ml',
        'Bug Tracker': 'https://github.com/Rohitlyengar/lab_ml/issues',
    },
)
