import sys
import logging

import redirection


class StdPrint:
    """
    Redirects Python's sys.stdout to Java's System.out
    """

    def write(self, msg, *args, **kwargs):
        redirection.jpcy_print(msg)

    def flush(self):
        pass


sys.stdout = StdPrint()
sys.stderr = StdPrint()
logging.getLogger().info = sys.stdout.write
logging.getLogger().error = sys.stderr.write
