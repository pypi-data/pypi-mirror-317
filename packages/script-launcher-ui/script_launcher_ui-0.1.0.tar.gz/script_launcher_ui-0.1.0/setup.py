from setuptools import setup, find_packages

setup(
    name='script_launcher_ui',
    version='0.1.0',
    description='A simple script launcher UI for configuration selection',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(include=['script_launcher_ui', 'script_launcher_ui.*']),
    install_requires=[
        'PyQt6',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)
