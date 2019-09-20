# library imports
from argparse import ArgumentParser
# local file imports
from AES.aes_demo import demo_aes


if __name__ == '__main__':
    # Set up argument parser and options
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    parser.add_argument("-A", "--algorithm", help="supply a specific algorithm name to run",
                        choices=["aes"], default="aes")

    # parse supplied arguments
    args = parser.parse_args()
    algorithm = args.algorithm

    # run algorithm
    if algorithm is "aes":
        demo_aes()
    else:
        print("ERROR: received unknown algorithm string. Exiting")
        exit(code=-1)
