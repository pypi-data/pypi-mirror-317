from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='york_patched',
    url='https://github.com/Vipulpatel12/york_patched',
    author='Vipul Patel',
    author_email='vipul108patel.vp@gmail.com',
    # Needed to actually package something
    packages=['patchwork'],
    # Needed for dependencies
    install_requires=['numpy'],

    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
    classifiers=[                        # Metadata about the package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
