from setuptools import setup, find_packages # type: ignore

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

setup(
        name="libfilter",
        version="1.32",
        author="kuba201",
        description='Signal/Audio Processing framework made with pure python',
        long_description=readme,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        url="https://github.com/KubaPro010/libfilter",
        install_requires=[],
        project_urls={
            'Source': 'https://github.com/KubaPro010/libfilter',
        },
        keywords=['fm', 'processor', 'pcm', 'signal'],
        classifiers= [
            "Intended Audience :: Education",
            "Intended Audience :: Telecommunications Industry",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.10",
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: GNU General Public License (GPL)",
        ]
)