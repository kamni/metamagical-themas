"""
J Leadbetter <j@jleadbetter.com>
MIT License

This is a script that modifies its own source code each time you run it. To
try it out:

```bash
$ python self_modifying_script.py
This script has modified itself 1 time.
$ python self_modifying_script.py
This script has modified itself 2 times.
```

And so on. Please reset the script counter back to 0 before submitting any
changes to this script.
"""

from __future__ import print_function

import os
import re


class SelfModifier(object):
    """
    Class that modifies its source code each time 'run' is called.

    This class is not thread safe and is only intended as a simple demo of
    how code might rewrite itself.
    """

    def __init__(self):
        self.times_run = 0
        self.module_code = ''

    def run(self):
        self.times_run = self.get_times_run()
        return self.times_run_text()

    def get_times_run(self):
        times_run = self.times_run

        filename = os.path.abspath(__file__)
        with open(filename, 'r') as current_file:
            code = current_file.readlines()

        times_run_base = 'self.times_run = {}'
        times_run_regex = times_run_base.format('(\d+)')

        for idx, line in enumerate(code):
            times_run_found = re.search(times_run_regex, line)
            if times_run_found:
                times_run = int(times_run_found.groups()[0]) + 1

                replace_string = times_run_base.format(times_run)
                code[idx] = re.sub(times_run_regex, replace_string, line)

                with open(filename, 'w') as current_file:
                    current_file.writelines(code)
                break

        return times_run

    def times_run_text(self):
        """
        Provides display text for how many times 'number_of_times_run' was called.

        :return: a string indicating times that this script has been run.
        :rtype: str
        """

        plural = ['s', ''][int(self.times_run == 1)]
        return 'This script has modified itself {} time{}.'.format(
            self.times_run, plural
        )


if __name__ == '__main__':
    sm_class = SelfModifier()
    print(sm_class.run())
