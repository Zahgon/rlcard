

import copy
import datetime
import csv
import json
import logging
import os
import time
from typing import Dict

import git


def gather_metadata() -> Dict:
    pass


class FileWriter:
    def __init__(self,
                 xpid: str = None,
                 xp_args: dict = None,
                 rootdir: str = '~/palaas'):
        if not xpid:
            xpid = '{proc}_{unixtime}'.format(
                proc=os.getpid(), unixtime=int(time.time()))
        self.xpid = xpid
        self._tick = 0

        if xp_args is None:
            xp_args = {}
        self.metadata = gather_metadata()
        self.metadata['args'] = copy.deepcopy(xp_args)
        self.metadata['xpid'] = self.xpid

        formatter = logging.Formatter('%(message)s')
        self._logger = logging.getLogger('palaas/out')

        shandle = logging.StreamHandler()
        shandle.setFormatter(formatter)
        self._logger.addHandler(shandle)
        self._logger.setLevel(logging.INFO)

        rootdir = os.path.expandvars(os.path.expanduser(rootdir))
        self.basepath = os.path.join(rootdir, self.xpid)

        if not os.path.exists(self.basepath):
            self._logger.info('Creating log directory: %s', self.basepath)
            os.makedirs(self.basepath, exist_ok=True)
        else:
            self._logger.info('Found log directory: %s', self.basepath)


        self.paths = dict(
            msg='{base}/out.log'.format(base=self.basepath),
            logs='{base}/logs.csv'.format(base=self.basepath),
            fields='{base}/fields.csv'.format(base=self.basepath),
            meta='{base}/meta.json'.format(base=self.basepath),
        )

        self._logger.info('Saving arguments to %s', self.paths['meta'])
        if os.path.exists(self.paths['meta']):
            self._logger.warning('Path to meta file already exists. '
                                 'Not overriding meta.')
        else:
            self._save_metadata()

        self._logger.info('Saving messages to %s', self.paths['msg'])
        if os.path.exists(self.paths['msg']):
            self._logger.warning('Path to message file already exists. '
                                 'New data will be appended.')

        fhandle = logging.FileHandler(self.paths['msg'])
        fhandle.setFormatter(formatter)
        self._logger.addHandler(fhandle)

        self._logger.info('Saving logs data to %s', self.paths['logs'])
        self._logger.info('Saving logs\' fields to %s', self.paths['fields'])
        if os.path.exists(self.paths['logs']):
            self._logger.warning('Path to log file already exists. '
                                 'New data will be appended.')
            with open(self.paths['fields'], 'r') as csvfile:
                reader = csv.reader(csvfile)
                self.fieldnames = list(reader)[0]
        else:
            self.fieldnames = ['_tick', '_time']

    def log(self, to_log: Dict, tick: int = None,
            verbose: bool = False) -> None:
        pass

    def close(self, successful: bool = True) -> None:
        self.metadata['date_end'] = datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S.%f')
        self.metadata['successful'] = successful
        self._save_metadata()

    def _save_metadata(self) -> None:
        with open(self.paths['meta'], 'w') as jsonfile:
            json.dump(self.metadata, jsonfile, indent=4, sort_keys=True)
