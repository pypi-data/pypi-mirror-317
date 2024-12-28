from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi (if you don‘t need delete it)
# here = os.path.abspath(os.path.dirname(__file__))
# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

# you need to change all these
VERSION = '0.1.5'
DESCRIPTION = 'some Common functions '
LONG_DESCRIPTION = 'using for self...'

setup(
    name="Yusir",
    version="0.1.5",
    author="clever Yusir",
    author_email="linxing_1@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[]
    # keywords=['python', 'menu', 'dumb_menu','windows','mac','linux'],
    # classifiers=[
    #     "Development Status :: 1 - Planning",
    #     "Intended Audience :: Developers",
    #     "Programming Language :: Python :: 3",
    #     "Operating System :: Unix",
    #     "Operating System :: MacOS :: MacOS X",
    #     "Operating System :: Microsoft :: Windows",
    # ]
    , dependencies=[
        'pyautogui',
        'opencv-python'
    ]
)
