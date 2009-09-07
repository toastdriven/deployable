from deployable import *


TARGET_DIRECTORY = os.path.join('/Users/daniellindsley/Desktop/sample_deploy')


install_list = [
    Tarball(url='http://pypi.python.org/packages/source/W/Whoosh/Whoosh-0.3.0b24.zip', post_process=whoosh_post),
    # Git(url='git://github.com/toastdriven/django-haystack.git', revision='b44afc6c'),
    # Svn(url='http://code.djangoproject.com/svn/django/trunk/django'),
    # GitSvn(url='http://code.djangoproject.com/svn/django/trunk/django'),
]


run_deploy(install_list, target=TARGET_DIRECTORY, cache_locally=True)
