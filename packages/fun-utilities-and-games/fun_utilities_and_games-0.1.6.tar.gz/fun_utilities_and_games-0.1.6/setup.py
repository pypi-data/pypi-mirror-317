from setuptools import setup, find_packages

setup(
    name='fun_utilities_and_games',
    version='0.1.6',  
    packages=find_packages(), 
    install_requires=['pygame', 'tk', ],
    author='Sriganth',
    author_email='sriganthperiyannan@example.com',
    description='A collection of fun utilities and text-based games in Python.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', 
    url='https://github.com/Sriganth-byte/fun_utilities_and_games',  
    project_urls={  
        'Bug Tracker': 'https://github.com/Sriganth-byte/fun_utilities_and_games/issues',
        'Source Code': 'https://github.com/Sriganth-byte/fun_utilities_and_games',
    },
    classifiers=[  
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    python_requires='>=3.7', 
    keywords='games utilities text-based python snake hangman tic-tac-toe puzzles',  
    license='MIT',
)
