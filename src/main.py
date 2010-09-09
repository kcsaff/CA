import pygame, window
from optparse import OptionParser

def main():
    options, args = OptionParser().parse_args()
    window.create(options, args, pygame).run()

if __name__ == '__main__':
    main()