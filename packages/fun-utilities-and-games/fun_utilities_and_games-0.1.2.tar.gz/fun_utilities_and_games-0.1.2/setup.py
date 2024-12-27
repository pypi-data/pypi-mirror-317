from setuptools import setup, find_packages

setup(
    name='fun_utilities_and_games',  # The new name of your package
    version='0.1.2',  # First version of the package
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'pygame',  # Required for Snake game and other graphical interfaces
        'tk',      # Tkinter is generally included with Python, but specifying doesn't hurt
    ],
    author='Sriganth',  # Your name
    author_email='sriganthperiyannan@example.com',  # Your email
    description='A collection of fun utilities and text-based games in Python.',  # Updated description
    long_description=open('README.md').read(),  # Read the content of the README.md file for a long description
    long_description_content_type='text/markdown',  # Specify the format of the long description
    url='https://github.com/Sriganth-byte/fun_utilities_and_games',  # Your updated GitHub repository URL
    project_urls={  # Optional additional links
        'Bug Tracker': 'https://github.com/Sriganth-byte/fun_utilities_and_games/issues',
        'Source Code': 'https://github.com/Sriganth-byte/fun_utilities_and_games',
    },
    classifiers=[  # Classifiers to categorize your project on PyPI
        'Development Status :: 1 - Planning',  # Changed to "Planning" for the first version
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'License :: OSI Approved :: MIT License',  # Adjust the license if you're using a different one
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    python_requires='>=3.7',  # Specify the minimum Python version required
    keywords='games utilities text-based python snake hangman tic-tac-toe puzzles',  # Keywords for your package
    license='MIT',  # License type
)
