from setuptools import setup, find_packages

setup(
    name='text_games',  # The name of your package
    version='0.1.0',  # The initial version of your project
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[  # List of dependencies your project needs to run
        # Add dependencies here, e.g., 'numpy', 'requests'
    ],
    author='Sriganth',  # Your name
    author_email='sriganthperiyannan@example.com',  # Your email
    description='A collection of text-based games in Python.',  # A short description of your project
    long_description=open('README.md').read(),  # Read the content of the README.md file for a long description
    long_description_content_type='text/markdown',  # Specify the format of the long description
    url='https://github.com/Sriganth-byte/Python_Text_Games',  # Your GitHub repository URL
    classifiers=[  # Classifiers to categorize your project on PyPI
        'Development Status :: 3 - Alpha',  # Change to "Beta" or "Production/Stable" when appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Adjust the license if you're using a different one
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    python_requires='>=3.7',  # Specify the minimum Python version required
)
