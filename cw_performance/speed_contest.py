# coding=utf-8
import timeit

__author__ = 'Cezary Wagner'
__copyright__ = 'Copyright 2015-2018, Cezary K. Wagner.'
__license__ = 'Apache License 2.0'
__version__ = '1.0'


class ContestFunction(object):
    """ Function which will participate in contest. """

    def __init__(self, test, setup=None):
        self.test = test
        "Test functions."

        self.setup = setup
        "Setup function for test function."

        self.result = None
        "Result of function."

    def __repr__(self):
        return (f'{self.__class__.__qualname__}('
                f'test={self.test!r}, '
                f'setup={self.setup!r}, '
                f'result={self.result!r})')


class SpeedContest(object):
    """ Speed contest for functions. """

    def __init__(self):
        self.functions = []
        "List of functions."

    def add_function(self, test, setup='pass'):
        """ Add expression or function for contest. """
        self.functions.append(ContestFunction(test, setup))

    def timeit_functions(self, timer=timeit.default_timer, number=timeit.default_number,
                         verbose=False):
        """ Measure speed on functions with use time it and show winner. """

        if verbose:
            print('Starting speed contest.')
        for function in self.functions:
            function.result = timeit.timeit(function.test, function.setup, timer=timer, number=number)
            if verbose:
                print('%s %.3e' % (function.test.__name__, function.result))

        max_time = max(x.result for x in self.functions)
        min_time = min(x.result for x in self.functions)
        functions = sorted(self.functions, key=lambda x: x.result, reverse=True)

        if verbose:
            print()
            print('Speed contest winners (the best is the last).')
            print('name, result, relative to maximum, relative to minimum')
            for function in functions:
                print('%s %.3e %.3f %.3f' % (
                    function.test.__name__,
                    function.result,
                    function.result / max_time,
                    function.result / min_time
                ))

        return functions, max_time, min_time

    def repeat_functions(self, timer=timeit.default_timer, number=timeit.default_number, repeat=timeit.default_repeat,
                         verbose=False):
        """ Measure speed with use repeat on functions and show winner. """

        if verbose:
            print('Starting speed contest.')
        for function in self.functions:
            function.result = timeit.repeat(function.test, function.setup, timer=timer, number=number, repeat=repeat)
            if verbose:
                print('%s %.3e' % (function.test.__name__, function.result))

        max_time = max(sum(x.result) for x in self.functions)
        min_time = max(sum(x.result) for x in self.functions)
        functions = sorted(self.functions, key=lambda x: sum(x.result),reverse=True)

        if verbose:
            print()
            print('Speed contest winners (the best is the last).')
            print('name, result, relative to maximum, relative to minimum')
            for function in functions:
                print('%s %.3e %.3f %.3f' % (
                    function.test.__name__,
                    function.result,
                    function.result / max_time,
                    function.result / min_time
                ))

        return functions, max_time, min_time

