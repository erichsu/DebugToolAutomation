"""
This is a Autmation script for Android App testing.
"""
import logging
import sys
import argparse

class Automator():
    # def __call__(self, parser, namespace, values, option_string=None):
    #     print('%r %r %r' % (namespace, values, option_string))
    #     setattr(namespace, self.dest, values)
        
    def run(self):
        """
        init: check the test folder, 
        """
        print self.config
        pass

    def _get_test_list(self):
        """
        TODO: list folder with the name heading of TestCase_{%d}
        """
        pass
        
        """
        TODO
        class TestHandler:
            load_setting
            setup_environment
            start_debug_mode
            trigger_test
            stop_debug_mode
        """
        
def main():
    automator = Automator()
    parser = argparse.ArgumentParser(description='Autmation script for Android App testing.')
    parser.add_argument('-v', '--version', action='version', version='Automator 1.0',
                        help='show the version info')
    parser.add_argument('-c', '--config', action='store', 
                        help='set the config file path')
    parser.parse_args(namespace=automator)
    automator.run()
    

if __name__ == "__main__":
    sys.argv += "-c C:\\testing\\path".split()
    main()
