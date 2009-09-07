from deployable import *

# For testing only! Not necessary if extracting to the current directory is A-OK by you.
TARGET_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'complex_deploy')


def whoosh_post(filename):
    print "Doing something to the file '%s'..." % filename


install_list = [
    Shell(command='mkdir foo', allow_fail=True),
    Tarball(url='http://pypi.python.org/packages/source/W/Whoosh/Whoosh-0.3.0b24.zip', filename='whoosh.zip', name='download_whoosh', post_process=whoosh_post),
    Git(url='git://github.com/toastdriven/django-haystack.git', revision='b44afc6c'),
    Svn(url='http://code.djangoproject.com/svn/django/trunk/django', revision='11364'),
    GitSvn(url='http://pysolr.googlecode.com/svn/trunk/', checkout_as='pysolr', revision='26'),
    Hg(url='http://bitbucket.org/ubernostrum/django-profiles/', revision='24'),
]


deploy(install_list, target=TARGET_DIRECTORY, local_cache=None)
# deploy(install_list, target=TARGET_DIRECTORY, local_cache='/tmp/sample_deploy_local_cache')
