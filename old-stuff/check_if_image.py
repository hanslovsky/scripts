#!/usr/bin/python


import vigra

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', dest='fn', required=True)
    args = vars(parser.parse_args())
    fn = args['fn']
    if vigra.impex.isImage(fn):
        sys.exit(0)
    else:
        sys.exit(1)
