from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='decor8ai',
    version='0.3.1',
    author='Akhilesh Joshi',
    author_email='akhilesh@immex.tech',
    description='Decor8 AI SDK for virtual staging, interior design generation, landscaping, remodeling, wall/cabinet color changes, sky replacement, and sketch-to-3D rendering.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/immex-tech/decor8ai-sdk',
    project_urls={
        'Homepage': 'https://www.decor8.ai',
        'Documentation': 'https://api-docs.decor8.ai',
        'Bug Tracker': 'https://github.com/immex-tech/decor8ai-sdk/issues',
    },
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
    ],
    keywords='decor8ai virtual-staging interior-design ai real-estate landscaping remodeling 3d-render',
    python_requires='>=3.10',
    install_requires=[
        'requests>=2.25.0',
    ],
)
