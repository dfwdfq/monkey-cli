import argparse
import sys

parser = argparse.ArgumentParser(
                    prog='monkey-cli',
                    description='A minimalistic typing test application for your terminal - inspired by Monkeytype.')


parser.add_argument("-d","--duration",help="test time in seconds.",type=int,default=30)
parser.add_argument("-w","--word-count",help="amount of words.",type=int,default=50)
parser.add_argument("-H","--history",help="display history.",action="store_true")

def get_arguments():
    try:
        args = parser.parse_args()
        wc = args.word_count
        d = args.duration
        if wc <= 0 or d <= 0:
            print("oh, dude! come on! No ZeroShitException in this app!")
            sys.exit(-1)
            
        return d, wc,args.history
    except SystemExit:
        sys.exit(0)
