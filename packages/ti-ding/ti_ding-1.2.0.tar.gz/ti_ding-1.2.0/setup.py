from setuptools import setup, find_packages

setup(
    name="ti-ding",
    version="1.2.0",
    description="A CLI tool to notify you with sound when a terminal process completes.",
    author="Anand Chourasia",
    author_email="anandchourasia007@gmail.com",
    packages=find_packages(),
    package_data={
        'src.sound_effects': ['*.mp3'],
    },
    include_package_data=True,
    install_requires=[
        "playsound == 1.2.2",
        "plyer"
    ],
    entry_points={
        "console_scripts": [
            "notify=src.cli:run_command_with_notification",
        ],
    },
    python_requires=">=3.7",
)
