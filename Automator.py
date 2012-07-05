"""
This is a Autmation script for Android App testing.
"""
import logging
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description='Autmation script for Android App testing.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                         help='an integer for the accumulator')
    parser.parse_args()

if __name__ == "__main__":
    sys.agrv += ["-h"]
    main()
