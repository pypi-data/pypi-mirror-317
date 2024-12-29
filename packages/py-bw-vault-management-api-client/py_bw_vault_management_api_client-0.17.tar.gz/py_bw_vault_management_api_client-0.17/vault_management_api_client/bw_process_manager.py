import json
import logging
import os.path
import shlex
import subprocess
import time
import urllib


class BwProcess:
  def __init__(self, bw_cli_path):
    if not os.access(bw_cli_path, os.X_OK):
      raise ValueError(f'{bw_cli_path} does not exists or is not executable')
    self.__bw = bw_cli_path
    self.__bw_process = None

  def run(self, *args, parse_output=False, timeout=30):
    logging_args = list(args)
    try:
      i = logging_args.index('login')
      for i in range(i + 1, len(logging_args)):
        logging_args[i] = '...'
    except ValueError:
      pass
    logging.info('Running %s', shlex.join(logging_args))
    args = [self.__bw] + list(args)
    try:
      output = subprocess.check_output(args, timeout=timeout)
    except Exception as e:
      if isinstance(e, subprocess.CalledProcessError):
        logging.error('Failed to run %s. Exited with code %d', logging_args, e.returncode)
      else:
        logging.error('Failed to run %s. %s', logging_args, e)
      raise e
    if parse_output:
      return json.loads(output)

  def start_serve(self, username, password, host, port):
    status_output = self.run('status', parse_output=True)
    assert status_output['status'] == 'unauthenticated', f'Unexpected status: {status_output}'
    self.run('login', username, password)

    self.__bw_process = subprocess.Popen(
      [self.__bw, 'serve', '--hostname', host, '--port', str(port)],
      bufsize=0, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
    )
    logging.info('Started bw serve with pid %d', self.__bw_process.pid)

    for _ in range(0, 300):
      time.sleep(0.1)
      logging.info('Checking if bw serve is up')
      if self.__bw_process.poll() is not None:
        self.terminate_serve()
        outs, errs = self.__bw_process.communicate(timeout=15)
        raise AssertionError(
          f'bw serve (PID: {self.__bw_process.pid}) unexpectedly reports as terminated'
          f'exit code: {self.__bw_process.returncode}, stdout: {outs}, stderr: {errs}')
      try:
        urllib.request.urlopen(f'http://{host}:{port}/', timeout=1)
      except urllib.error.HTTPError:
        # url responds with a 404
        logging.info('bw serve up')
        break
      except urllib.error.URLError:
        pass
    else:
      self.terminate_serve()
      outs, errs = self.__bw_process.communicate(timeout=15)
      raise AssertionError(
        f'bw serve failed to start (PID: {self.__bw_process.pid}). '
        f'exit code: {self.__bw_process.returncode}, stdout: {outs}, stderr: {errs}')

  def terminate_serve(self):
    logging.info('Terminating bw serve')
    self.__bw_process.terminate()
    try:
      self.__bw_process.communicate(timeout=10)
      logging.info('bw serve (PID: %d) terminated', self.__bw_process.pid)
    except subprocess.TimeoutExpired:
      logging.warn('bw serve didn\'t terminate, killing it')
      self.__bw_process.kill()
    self.__bw_process = None
    self.run('logout')

