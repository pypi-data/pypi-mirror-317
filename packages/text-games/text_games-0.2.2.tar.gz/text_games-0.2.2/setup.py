from setuptools import setup, find_packages

setup(
    name='text_games',  # The name of your package
    version='0.2.2',  # Updated version for the new release
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'pygame',  # Required for Snake game and other graphical interfaces
        'tk',      # Tkinter is generally included with Python, but specifying doesn't hurt
    ],
    author='Sriganth',  # Your name
    author_email='sriganthperiyannan@example.com',  # Your email
    description='A collection of text-based games in Python.',  # A short description of your project
    long_description=open('README.md').read(),  # Read the content of the README.md file for a long description
    long_description_content_type='text/markdown',  # Specify the format of the long description
    url='https://github.com/Sriganth-byte/Python_Text_Games',  # Your GitHub repository URL
    project_urls={  # Optional additional links
        'Bug Tracker': 'https://github.com/Sriganth-byte/Python_Text_Games/issues',
        'Source Code': 'https://github.com/Sriganth-byte/Python_Text_Games',
    },
    classifiers=[  # Classifiers to categorize your project on PyPI
        'Development Status :: 4 - Beta',  # Updated to "Beta" since this is an upgrade
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
    keywords='games text-based python snake hangman tic-tac-toe puzzles',  # Keywords for your package
    license='MIT',  # License type
)
