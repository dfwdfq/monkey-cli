import argparse

parser = argparse.ArgumentParser(
                    prog='monkey-cli',
                    description='A minimalistic typing test application for your terminal - inspired by Monkeytype.')


parser.add_argument("-d","--duration",help="test time in seconds.",type=int,default=30)
parser.add_argument("-w","--word-count",help="amount of words.",type=int,default=50)

def get_arguments():
    args = parser.parse_args()
    return args.duration, args.word_count
