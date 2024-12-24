# setup.py

from setuptools import setup, find_packages

setup(
    name="sokoweb",
    version="0.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "cryptography>=43.0.3",
        "fastapi>=0.115.5",
        "uvicorn[standard]>=0.32.0",
        "python-jose>=3.3.0",
        "passlib==1.7.4",
        "bcrypt==3.2.0",
        "python-multipart>=0.0.17",
        "asgi_lifespan>=2.1.0",
        "aiohttp>=3.8.0",
        "SQLAlchemy>=1.4.0",
        "asyncpg>=0.25.0",
        "psycopg2-binary>=2.9.0",
        'email-validator',
        'pydantic[email]',
        'aiofiles'
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ]
    },
    entry_points={
        'console_scripts': [
            'sokoweb-up = sokoweb.cli:main',
        ],
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)