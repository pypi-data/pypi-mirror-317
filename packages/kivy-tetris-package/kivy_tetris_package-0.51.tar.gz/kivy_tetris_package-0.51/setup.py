from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()
f.close()

setup(
    name="kivy_tetris_package",
    version="0.51",
    author="Daniel Kříž",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    description="Tetris game written in Kivy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "kivy",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'kivy_tetris_package = kivy_tetris_package.main:main'
        ]
    },
    package_data={
        '': ['kivy_tetris_package/*'],
    },
)
