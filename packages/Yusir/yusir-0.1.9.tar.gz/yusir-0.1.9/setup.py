from setuptools import setup, find_packages

VERSION = '0.1.9'
DESCRIPTION = 'some Common functions '
LONG_DESCRIPTION = 'using for self...'

setup(
    name="Yusir",
    version="0.1.9",
    author="clever Yusir",
    author_email="linxing_1@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[]
    , dependencies=[
        'pyautogui',
        'opencv-python'
    ]
)
