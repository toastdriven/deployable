from deployable import *


TARGET_DIRECTORY = os.path.join('/Users/daniellindsley/Desktop/sample_deploy')


install_list = [
    Shell(command='mkdir foo', allow_fail=True),
    Tarball(url='http://pypi.python.org/packages/source/W/Whoosh/Whoosh-0.3.0b24.zip', name='download_whoosh'),
    # Tarball(url='http://pypi.python.org/packages/source/W/Whoosh/Whoosh-0.3.0b24.zip', post_process=whoosh_post),
    # Git(url='git://github.com/toastdriven/django-haystack.git', revision='b44afc6c'),
    # Svn(url='http://code.djangoproject.com/svn/django/trunk/django'),
    # GitSvn(url='http://code.djangoproject.com/svn/django/trunk/django'),
]


deploy(install_list, target=TARGET_DIRECTORY, local_cache=None)
# deploy(install_list, target=TARGET_DIRECTORY, local_cache='/tmp/sample_deploy_local_cache')
