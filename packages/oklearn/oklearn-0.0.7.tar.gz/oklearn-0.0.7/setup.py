from setuptools import setup

setup(
    name='oklearn',
    version='0.0.7',
    description='machine learning library for the python programming language',
    url='',
    author='',
    author_email='',
    license='MIT',
    packages=['oklearn'],
    install_requires=['pandas', 'numpy', 'imbalanced-learn', 'scikit-learn', 'matplotlib',
                      'xgboost', 'lightgbm'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'
    ],
)