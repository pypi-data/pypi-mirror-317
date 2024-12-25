from setuptools import setup

if __name__ == "__main__":
    setup(
        name="URAdime",
        version="0.2.1",
        packages=["URAdime"],
        install_requires=[
            "pysam",
            "pandas",
            "biopython",
            "python-Levenshtein",
            "tqdm",
            "numpy",
        ],
        entry_points={
            'console_scripts': [
                'uradime=URAdime.URAdime:main',
            ],
        },
    ) 