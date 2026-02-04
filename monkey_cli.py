#!/usr/bin/env python3
"""
Monkey-CLI: A Monkeytype clone for the terminal.
A minimalistic typing test application with real-time WPM and accuracy tracking.
"""
from arguments import get_arguments
from typing_test import TypingTest
import curses

def main(stdscr):
    """Main entry point for the application."""
    duration,word_count,history = get_arguments()
    while True:
        test = TypingTest(stdscr, duration=duration, word_count=word_count,show_history=history)
        restart = test.run()
        if not restart:
            break


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("quit Monkey-CLI.")
