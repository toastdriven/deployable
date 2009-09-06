"""
deployable - A simple system for repeatable deploys.

There are a number of deployment systems out there but most are very
complicated or are language-specific. ``deployable`` aims to be
language-agnostic, easy to use, repeatable, flexible and fault-tolerant.


* Requires Python 2.4+ w/ no other dependancies.
* Only test on *nix systems, though it may work on Windows. (Reports/patches
  accepted!)
"""
import logging
import os
import subprocess
import sys
from deployable.plugins import tarball


__author__ = 'Daniel Lindsley'
__version__ = (0, 0, 1)


# Default logger.
log = logging.getLogger('deployable')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log.setFormatter(formatter)


class DeployFailed(Exception):
    pass


class DeployCommand(object):
    """
    The base command from which other commands should extend.
    
    Subclasses must support at least what's mentioned in the API here.
    """
    def __init__(self, name=None, allow_fail=False, **kwargs):
        self.name = name
        self.allow_fail = allow_fail
    
    def run_command(self, log, successful_jobs):
        """
        The main command method that performs part of the deployment.
        
        Must be overridden in the subclass. Successful runs should return
        nothing, while failed runs should raise an exception.
        """
        raise NotImplementedError("You must subclass `DeployCommand` and implement the `run_command` method.")


def deploy(commands, target=None, local_cache=None, logger=None):
    """
    Runs one or more deploy commands for execution.
    
    Accepts:
        ``target``:
            A absolute or relative path where the targets should be installed.
            This is overridable on a per-command basis. If ``None``, the current
            directory is assumed.
        ``local_cache``:
            A absolute or relative path where the targets should be locally
            cached. This is useful if you want to set up a single server where
            all of your other servers point to fetch their dependancies (avoids
            failed deploys when random site on the internet is down).
        ``logger``:
            A Python ``logging`` class. If None, uses the default logger which
            dumps to STDOUT.
    """
    global log
    cache = None
    successful = {}
    failed = {}
    
    if logger is None:
        logger = log
    
    if target is None:
        target = os.path.join(os.path.dirname(__file__))
    else:
        target = create_target_directory(logger, target)
    
    if local_cache is not None:
        cache = create_cache_directory(logger, local_cache)
    
    for command in commands:
        if hasattr(command, 'run_command'):
            try:
                command.run_command(logger, successful)
                successful[command.name] = command
            except:
                failed.add[command.name] = command
                
                if not command.allow_fail:
                    rollback_deploy(successful)
                    logger.error("Deploy failed.")
                    raise DeployFailed("Command '%s' failed." % command.name)
    
    logger.info("Deploy completed successfully.")


def create_target_directory(logger, target_directory):
    if not os.path.exists(target_directory):
        logger.info("Deploy directory '%s' does not exist. Creating...")
        os.mkdir(target_directory)
    else:
        logger.info("Deploy directory '%s' already exists.")


def create_cache_directory(logger, cache_directory):
    if not os.path.exists(cache_directory):
        logger.info("Cache directory '%s' does not exist. Creating...")
        os.mkdir(cache_directory)
    else:
        logger.info("Cache directory '%s' already exists.")
