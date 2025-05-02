from setuptools import setup, find_packages

setup(
    name="miku-bot",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "flask",
        "gunicorn",
        "praw",
        "python-telegram-bot==13.15",
        "requests",
        "telegram",
        "pillow",
        "APScheduler"
    ],
    python_requires=">=3.8",
)