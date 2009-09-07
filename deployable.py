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


__author__ = 'Daniel Lindsley'
__version__ = (0, 0, 1)
__license__ = 'BSD'


# Default logger.
log = logging.getLogger('deployable')
log.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %g:%M:%S')
stream.setFormatter(formatter)
log.addHandler(stream)


class DeployFailed(Exception):
    pass


class CommandFailed(Exception):
    pass


class DeployCommand(object):
    """
    The base command from which other commands should extend.
    
    Subclasses must support at least what's mentioned in the API here.
    """
    def __init__(self, name=None, allow_fail=False, log=None, post_process=None, **kwargs):
        self.name = name
        self.allow_fail = allow_fail
        self.log = log
        self.post_process = post_process
    
    def run_command(self):
        """
        The main command method that performs part of the deployment.
        
        Must be overridden in the subclass. Successful runs should return
        nothing, while failed runs should raise an exception.
        """
        raise NotImplementedError("You must subclass `DeployCommand` and implement the `run_command` method.")
    
    # def rollback(self):
    #     raise NotImplementedError("You must subclass `DeployCommand` and implement the `rollback` method.")
    
    def shell_command(self, command, log_output=False):
        command = command.split()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = process.communicate()
        return (process.returncode == 0, stdout, stderr)


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
        os.chdir(target)
        
    
    if local_cache is not None:
        cache = create_cache_directory(logger, local_cache)
    
    for command in commands:
        if not command.log:
            command.log = logger
        
        if hasattr(command, 'run_command'):
            try:
                command.run_command()
                successful[command.name] = command
            except Exception, e:
                failed[command.name] = command
                
                if command.allow_fail:
                    logger.error("Command failed. Moving on...")
                else:
                    logger.error("Command failed. Aborting...")
                    
                    if isinstance(e, CommandFailed):
                        raise e
                    else:
                        raise DeployFailed("Command '%s' failed - %s." % (command.name, e))
    
    logger.info("Deploy completed successfully.")


def create_target_directory(logger, target_directory):
    if not os.path.exists(target_directory):
        logger.info("Deploy directory '%s' does not exist. Creating...")
        os.mkdir(target_directory)
    else:
        logger.info("Deploy directory '%s' already exists.")
    
    return target_directory


def create_cache_directory(logger, cache_directory):
    if not os.path.exists(cache_directory):
        logger.info("Cache directory '%s' does not exist. Creating...")
        os.mkdir(cache_directory)
    else:
        logger.info("Cache directory '%s' already exists.")


# Built-in Commands

class Shell(DeployCommand):
    def __init__(self, command, **kwargs):
        super(Shell, self).__init__(**kwargs)
        self.command = command
        
        if not 'name' in kwargs:
            self.name = command
    
    def run_command(self):
        self.log.info("Running shell command '%s'..." % self.command)
        success, stdout, stderr = self.shell_command(self.command)
        
        if not success:
            raise CommandFailed("Shell command '%s' failed - %s." % (self.command, stderr))
        
        self.log.info("Shell command '%s' succeeded." % self.command)


class Tarball(DeployCommand):
    def __init__(self, url, target=None, **kwargs):
        super(Tarball, self).__init__(**kwargs)
        self.url = url
        self.target = target
        
        if not self.name:
            self.name = url
    
    def determine_curl_or_wget(self):
        curl = True
        
        returncode, stdout, stderr = self.shell_command('whereis curl')
        
        if not stdout:
            returncode, stdout, stderr = self.shell_command('whereis wget')
            curl = False
            
            if not stdout:
                raise CommandFailed("Neither `curl` nor `wget` could be found on this system. Aborting download of '%s'." % self.url)
        
        return curl
    
    def download_tarball(self, curl=True):
        if curl:
            if self.target:
                command = 'curl -o %s %s' % (self.target, self.url)
            else:
                command = 'curl -O %s' % self.url
        else:
            if self.target:
                command = 'wget -O %s %s' % (self.target, self.url)
            else:
                command = 'wget %s' % self.url
        
        self.log.info("Downloading tarball via '%s'..." % command)
        success, stdout, stderr = self.shell_command(command)
        
        if not success:
            raise CommandFailed("Download '%s' failed - %s." % (command, stderr))
        
        self.log.info("Tarball download '%s' succeeded." % command)
    
    def extract_tarball(self):
        # Determine the type for extraction.
        if self.target:
            filename = os.path.basename(self.target)
        else:
            filename = os.path.basename(self.url)
        
        extension = os.path.splitext(filename)[1]
        
        if 'gz' in extension:
            extract_command = 'tar xzf %s' % filename
        elif 'bz2' in extension:
            extract_command = 'tar xjf %s' % filename
        elif 'tar' in extension:
            extract_command = 'tar xjf %s' % filename
        elif 'zip' in extension:
            extract_command = 'unzip -f %s' % filename
        else:
            self.log.error("Unable to extract '%s' as it is an unknown type (%s). Please report this issue." % (filename, extension))
            raise CommandFailed("Extraction of tarball failed - %s." % stderr)
            
        
        self.log.info("Extracting tarball '%s'..." % filename)
        success, stdout, stderr = self.shell_command(extract_command)
        
        if not success:
            raise CommandFailed("Extraction of tarball '%s' failed - %s." % (extract_command, stderr))
        
        self.log.info("Tarball extraction '%s' succeeded." % extract_command)
        return filename
    
    def run_command(self):
        use_curl = self.determine_curl_or_wget()
        self.download_tarball(use_curl)
        filename = self.extract_tarball()
        self.log.info("Tarball '%s' succeeded." % self.name)
        
        if self.post_process is not None:
            self.log.info("Post-processing tarball '%s'..." % self.name)
            self.post_process(filename)
            self.log.info("Tarball '%s' post-processing succeeded." % self.name)



