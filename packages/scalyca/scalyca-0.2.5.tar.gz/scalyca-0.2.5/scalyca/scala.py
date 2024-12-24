import abc
import argparse
import datetime
import logging

from . import colour as c
from . import exceptions
from . import logger

log = logger.setup_log('root', timefmt='%H:%M:%S')


class Scala(metaclass=abc.ABCMeta):
    """
        Scala: Simple Console Application with Logging and Argparse
    """
    _description = "Simple Configurable Application with Logging and Argparse"
    _prog = "Scala"
    _version = "undefined"

    def __init__(self, **kwargs):
        """ Optionally override the application name and description """
        self._ok = False
        self._started = datetime.datetime.now(datetime.UTC)
        self._description = kwargs.get('description', self._description)
        self._prog = kwargs.get('prog', self._prog)
        self._success_message = kwargs.get('success_message', f"{c.script(self._prog)} finished")
        self._abort_message = kwargs.get('error_message', f"{c.script(self._prog)} aborted during runtime")

        self._argparser = argparse.ArgumentParser(
            prog=self._prog,
            description=self._description
        )

    def _initialize(self):
        log.info(f"{c.script(self._prog)} (version {self._version}) starting")
        self._add_default_arguments()
        self.add_arguments()
        self.args = self._argparser.parse_args()

        self._configure()
        self._override_configuration()
        self.initialize()

    def add_argument(self, *args, **kwargs):
        """ Just a public wrapper so that we do not have to access _argparser directly """
        self._argparser.add_argument(*args, **kwargs)

    def add_arguments(self):
        """ Override this in your Scala derivative to add custom arguments """

    def _add_default_arguments(self):
        """ Add default arguments that are present in every instance of Scala """
        self.add_argument('-l', '--logfile', type=argparse.FileType('w'), help="Write log to file")
        self.add_argument('-d', '--debug', action='store_true', help="Turn on verbose logging")

    def initialize(self):
        """ Custom initialization routines. Might remain empty. """

    def _configure(self):
        pass

    @abc.abstractmethod
    def main(self):
        """
        The main entry point of the program.
        Provide an implementation in your derivative of Scala.
        """

    def finalize(self):
        """ Override this in you Scala derivative to add custom finalization """

    def _override_configuration(self):
        self.override_configuration()
        log.setLevel(logging.DEBUG if self.args.debug else logging.INFO)
        log.debug(f"{c.script(self._prog)} debug mode on")

        if self.args.logfile:
            log.addHandler(logging.FileHandler(self.args.logfile.name))
            log.debug(f"Added log output {c.path(self.args.logfile.name)}")

    def override_configuration(self):
        """ Custom override hook for overriding the configuration """

    def run(self):
        try:
            self._initialize()
            self.main()
            self._ok = True
        except exceptions.PrerequisiteError as e:
            log.error(f"Terminating due to missing prerequisites: {e}")
            self._ok = False
        except exceptions.ConfigurationError as e:
            log.error(f"Terminating due to a configuration error: {e}")
            self._ok = False
        except KeyboardInterrupt:
            log.error(f"Interrupted by user")
            self._ok = False
        finally:
            self._finalize()
            run_time = datetime.datetime.now(datetime.UTC) - self._started
            if self._ok:
                log.info(f"{self._success_message} in {run_time}")
            else:
                log.critical(f"{self._abort_message} after {run_time}")

    def _finalize(self):
        self.finalize()
