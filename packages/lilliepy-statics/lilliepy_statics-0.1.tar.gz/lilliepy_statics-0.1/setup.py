from setuptools import setup

setup(
    name='lilliepy-statics',
    version='0.1',
    packages=['lilliepy_statics'],
    install_requires=[
        'reactpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    description='helps with static files related stuff in the lilliepy framework',
    keywords=[
        "lilliepy", "lilliepy-static", "reactpy", "lilliepy-statics"
    ],
    url='https://github.com/websitedeb/lilliepy-statics',
    author='Sarthak Ghoshal',
    author_email='sarthak22.ghoshal@gmail.com',
    license='MIT',
    python_requires='>=3.6',
)