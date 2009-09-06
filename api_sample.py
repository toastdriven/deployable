from deployable import *
from deployable.plugins import git, svn


TARGET_DIRECTORY = os.path.join('/Users/daniellindsley/Desktop/sample_deploy')


install_list = [
    tarball(url='http://pypi.python.org/packages/source/W/Whoosh/Whoosh-0.3.0b24.zip', postprocess=whoosh_post),
    # git(url='git://github.com/toastdriven/django-haystack.git', revision='b44afc6c'),
    # svn(url='http://code.djangoproject.com/svn/django/trunk/django'),
    # git_svn(url='http://code.djangoproject.com/svn/django/trunk/django'),
]


run_deploy(install_list, target=TARGET_DIRECTORY, cache_locally=True)
