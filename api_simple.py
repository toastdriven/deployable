from deployable import *


# For testing only! Not necessary if extracting to the current directory is A-OK by you.
TARGET_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'simple_deploy')


install_list = [
    Shell(command='mkdir foo'),
    Tarball(url='http://pypi.python.org/packages/source/W/Whoosh/Whoosh-0.3.0b24.zip'),
    Git(url='git://github.com/toastdriven/django-haystack.git'),
    Svn(url='http://code.djangoproject.com/svn/django/trunk/django'),
    GitSvn(url='http://pysolr.googlecode.com/svn/trunk/'),
    Hg(url='http://bitbucket.org/ubernostrum/django-profiles/'),
]

deploy(install_list, target=TARGET_DIRECTORY)
