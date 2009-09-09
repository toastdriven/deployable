deployable
==========

A simple system for repeatable deploys.


Why?
----

There are a number of deployment systems out there (such as Capistrano_,
`zc.buildout`_, pip_ requirements, etc.) but most are very complicated or are
language-specific. ``deployable`` aims to be language-agnostic, easy to use,
repeatable, flexible and fault-tolerant.

``deployable`` is ideal for setting up a single machine. Should you need
deployment on multiple machines, you might want to consider using ``deployable``
with Fabric_.

.. _Capistrano: http://www.capify.org/
.. _zc.buildout: http://pypi.python.org/pypi/zc.buildout/
.. _pip: http://pypi.python.org/pypi/pip
.. _Fabric: http://www.nongnu.org/fab/


Goals
-----

* Language-agnostic
* Repeatable
* Easy to use
* Easy to extend
* Work with many major version control systems
* Allow for cached deployment (pull sources to a single machine then
  redistribute to other servers)


Requirements
------------

* Requires Python 2.4+ w/ no other dependancies.
* No install required, just include the ``deployable.py`` file along with your
  source code.
* Only test on Unix systems, though it may work on Windows. (Reports/patches
  accepted!)


Usage
------

Simply create a Python file of with the name of your choice and fill it with::

    from deployable import *
    
    install_list = [
        Shell(command='mkdir foo'),
        Tarball(url='http://pypi.python.org/packages/source/W/Whoosh/Whoosh-0.3.0b24.zip'),
        Git(url='git://github.com/toastdriven/django-haystack.git'),
        Svn(url='http://code.djangoproject.com/svn/django/trunk/django'),
        GitSvn(url='http://pysolr.googlecode.com/svn/trunk/'),
        Hg(url='http://bitbucket.org/ubernostrum/django-profiles/'),
    ]
    
    deploy(install_list)

Then run the file (i.e. ``python deploy_me_please.py``). You'll get a log of
what's going on. For advanced usage, see the ``api_complex.py`` sample file
included with this distribution.


Supported
---------

Currently supported commands are:

* shell
* tarball
* Git
* Mercurial
* Subversion
* git-svn
