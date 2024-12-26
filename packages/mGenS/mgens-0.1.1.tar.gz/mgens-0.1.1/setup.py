from setuptools import setup, find_packages

setup(
    name='mGenS',  # Replace with your package name
    version='0.1.1',  # Initial version
    author='Hathaway Zhang',  # Your name
    author_email='hathawayzhang@gmail.com',  # Your email
    description='Support functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hathaaaway/mgen',  # URL to your package's repository
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Update based on your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify your Python version requirement
)


# from distutils.core import setup

# setup(
#   name = 'mgen',         # How you named your package folder (MyLib)
#   packages = ['mgen'],   # Chose the same as "name"
#   version = '0.1',      # Start with a small number and increase it with every change you make
#   license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
#   description = 'Master generator for dashboards',   # Give a short description about your library
#   author = 'Hathaway Zhang',                   # Type in your name
#   author_email = 'hathawayzhang@gmail.com',      # Type in your E-Mail
#   url = 'https://github.com/hathaaaway/reponame',   # Provide either the link to your github or to your website
#   download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
#   keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
#   install_requires=[            # I get to this in a second
#           'validators',
#           'beautifulsoup4',
#       ],
#   classifiers=[
#     'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

#     'Intended Audience :: Developers',      # Define that your audience are developers
#     'Topic :: Software Development :: Build Tools',

#     'License :: OSI Approved :: MIT License',   # Again, pick a license

#     'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
#     'Programming Language :: Python :: 3.4',
#     'Programming Language :: Python :: 3.5',
#     'Programming Language :: Python :: 3.6',
#   ],
# )