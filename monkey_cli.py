#!/usr/bin/env python3
"""
Monkey-CLI: A Monkeytype clone for the terminal.
A minimalistic typing test application with real-time WPM and accuracy tracking.
"""

import curses
import time
import random
from typing import List, Tuple
from datetime import datetime
from data_storage import DataStorage
from arguments import get_arguments

# Common English words for typing tests
WORD_LIST = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
    "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
    "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
    "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
    "even", "new", "want", "because", "any", "these", "give", "day", "most", "us",
    "is", "was", "are", "been", "has", "had", "were", "said", "did", "having",
    "may", "should", "find", "very", "through", "between", "such", "being", "under", "why",
    "system", "each", "those", "both", "world", "still", "own", "where", "men", "much",
    "long", "down", "side", "many", "must", "before", "right", "too", "same", "tell",
    "boy", "follow", "came", "show", "every", "part", "once", "place", "made", "name",
    "develop", "create", "program", "computer", "software", "hardware", "network", "internet", "website", "application",
    "function", "variable", "method", "class", "object", "array", "string", "number", "boolean", "loop",
    "condition", "statement", "operator", "expression", "parameter", "argument", "return", "value", "type", "data",
    "structure", "algorithm", "process", "thread", "memory", "storage", "database", "server", "client", "request",
    "response", "protocol", "security", "encryption", "authentication", "authorization", "session", "cookie", "token", "api"
]


class TypingTest:
    """Main typing test application class."""
    
    def __init__(self, stdscr, duration: int = 30, word_count: int = 50):
        """
        Initialize the typing test.
        
        Args:
            stdscr: curses standard screen object
            duration: Test duration in seconds
            word_count: Number of words to generate
        """
        self.stdscr = stdscr
        self.duration = duration
        self.word_count = word_count
        
        # Data storage
        self.storage = DataStorage()
        
        # Generate random words
        self.words = self._generate_words()
        self.target_text = " ".join(self.words)
        
        # User input tracking
        self.user_input = ""
        self.current_position = 0
        
        # Statistics
        self.start_time = None
        self.end_time = None
        self.correct_chars = 0
        self.incorrect_chars = 0
        self.total_chars_typed = 0
        
        # Test state
        self.test_active = False
        self.test_completed = False
        
        # Setup curses
        self._setup_curses()
    
    def _setup_curses(self):
        """Initialize curses settings."""
        curses.curs_set(1)  # Show cursor
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Correct
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Incorrect
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Normal text
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Stats (kept separate for easy customization)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Title (kept separate for easy customization)
        self.stdscr.clear()
    
    def _generate_words(self) -> List[str]:
        """Generate random words for the test."""
        return [random.choice(WORD_LIST) for _ in range(self.word_count)]
    
    def _calculate_wpm(self) -> float:
        """Calculate words per minute."""
        if not self.start_time:
            return 0.0
        
        end_time = self.end_time if self.end_time else time.time()
        elapsed = end_time - self.start_time
        if elapsed == 0:
            return 0.0
        
        # WPM = (characters typed / 5) / minutes elapsed
        minutes = elapsed / 60
        words_typed = self.correct_chars / 5
        return words_typed / minutes if minutes > 0 else 0.0
    
    def _calculate_accuracy(self) -> float:
        """Calculate typing accuracy."""
        if self.total_chars_typed == 0:
            return 100.0
        return (self.correct_chars / self.total_chars_typed) * 100
    
    def _get_time_remaining(self) -> float:
        """Get remaining time in seconds."""
        if not self.start_time:
            return self.duration
        
        elapsed = time.time() - self.start_time
        remaining = self.duration - elapsed
        return max(0, remaining)
    
    def _draw_header(self):
        """Draw the header with title and timer."""
        height, width = self.stdscr.getmaxyx()
        
        # Title
        title = "MONKEY-CLI - Terminal Typing Test"
        self.stdscr.addstr(0, max(0, (width - len(title)) // 2), title, 
                          curses.color_pair(5) | curses.A_BOLD)
        
        # Timer and stats
        if self.test_active and not self.test_completed:
            time_remaining = self._get_time_remaining()
            wpm = self._calculate_wpm()
            accuracy = self._calculate_accuracy()
            
            stats = f"Time: {time_remaining:.1f}s | WPM: {wpm:.0f} | Accuracy: {accuracy:.1f}%"
        else:
            stats = f"Duration: {self.duration}s | Press any key to start..."
        
        self.stdscr.addstr(1, max(0, (width - len(stats)) // 2), stats, 
                          curses.color_pair(4))
        
        # Separator
        self.stdscr.addstr(2, 0, "─" * width)
    
    def _draw_text(self):
        """Draw the target text with color-coded characters."""
        height, width = self.stdscr.getmaxyx()
        start_row = 4
        
        # Calculate display window for text
        max_display_chars = width * (height - start_row - 5)
        display_start = max(0, self.current_position - 100)
        display_end = min(len(self.target_text), display_start + max_display_chars)
        
        row = start_row
        col = 0
        
        for i in range(display_start, display_end):
            if row >= height - 3:
                break
            
            char = self.target_text[i]
            
            # Determine color based on typing status
            if i < len(self.user_input):
                # Already typed
                if self.user_input[i] == char:
                    color = curses.color_pair(1)  # Green for correct
                else:
                    color = curses.color_pair(2)  # Red for incorrect
            elif i == len(self.user_input):
                # Current position (cursor)
                color = curses.color_pair(3) | curses.A_UNDERLINE
            else:
                # Not yet typed
                color = curses.color_pair(3)
            
            try:
                self.stdscr.addstr(row, col, char, color)
            except curses.error:
                pass  # Ignore if we can't write to screen edge
            
            col += 1
            if col >= width - 1:
                row += 1
                col = 0
    
    def _draw_footer(self):
        """Draw the footer with instructions."""
        height, width = self.stdscr.getmaxyx()
        
        footer = "ESC: Restart | Ctrl+C: Quit"
        try:
            self.stdscr.addstr(height - 1, max(0, (width - len(footer)) // 2), 
                             footer, curses.color_pair(3))
        except curses.error:
            pass
    
    def _draw_results(self):
        """Draw the final results screen."""
        height, width = self.stdscr.getmaxyx()
        
        self.stdscr.clear()
        
        # Title
        title = "Test Complete!"
        self.stdscr.addstr(height // 2 - 6, max(0, (width - len(title)) // 2), 
                          title, curses.color_pair(5) | curses.A_BOLD)
        
        # Results
        wpm = self._calculate_wpm()
        accuracy = self._calculate_accuracy()
        
        results = [
            f"WPM: {wpm:.2f}",
            f"Accuracy: {accuracy:.2f}%",
            f"Correct Characters: {self.correct_chars}",
            f"Incorrect Characters: {self.incorrect_chars}",
            f"Total Characters: {self.total_chars_typed}"
        ]
        
        for i, line in enumerate(results):
            self.stdscr.addstr(height // 2 - 4 + i, max(0, (width - len(line)) // 2), 
                             line, curses.color_pair(4))
        
        # Instructions
        instruction = "Press ESC to restart | H for history | Ctrl+C to quit"
        self.stdscr.addstr(height // 2 + 4, max(0, (width - len(instruction)) // 2), 
                          instruction, curses.color_pair(3))
        
        self.stdscr.refresh()
    
    def _save_result(self):
        """Save the test result to storage."""
        if self.test_completed and self.start_time:
            wpm = self._calculate_wpm()
            accuracy = self._calculate_accuracy()
            self.storage.save_result(
                wpm=wpm,
                accuracy=accuracy,
                correct_chars=self.correct_chars,
                incorrect_chars=self.incorrect_chars,
                total_chars=self.total_chars_typed,
                duration=self.duration
            )
    
    def _draw_history(self):
        """Draw the history screen with statistics and graphs."""
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        
        # Get statistics
        stats = self.storage.get_statistics()
        recent = self.storage.get_recent_results(10)
        
        row = 1
        
        # Title
        title = "Typing History & Statistics"
        self.stdscr.addstr(row, max(0, (width - len(title)) // 2), 
                          title, curses.color_pair(5) | curses.A_BOLD)
        row += 2
        
        # Overall statistics
        if stats["total_tests"] > 0:
            self.stdscr.addstr(row, 2, "Overall Statistics:", curses.color_pair(5))
            row += 1
            
            stats_lines = [
                f"  Total Tests: {stats['total_tests']}",
                f"  Average WPM: {stats['average_wpm']:.2f}",
                f"  Best WPM: {stats['best_wpm']:.2f}",
                f"  Average Accuracy: {stats['average_accuracy']:.2f}%",
                f"  Best Accuracy: {stats['best_accuracy']:.2f}%",
                f"  Total Characters Typed: {stats['total_chars']}"
            ]
            
            for line in stats_lines:
                self.stdscr.addstr(row, 2, line, curses.color_pair(3))
                row += 1
            
            row += 1
            
            # Recent results graph
            if recent:
                self.stdscr.addstr(row, 2, "Recent WPM Trend (Last 10 Tests):", 
                                 curses.color_pair(5))
                row += 1
                
                # Draw simple bar chart
                max_wpm = max(r["wpm"] for r in recent)
                max_bar_width = width - 20
                
                for i, result in enumerate(recent):
                    # Date
                    try:
                        date = datetime.fromisoformat(result["timestamp"])
                        date_str = date.strftime("%m/%d %H:%M")
                    except:
                        date_str = "Unknown"
                    
                    # Bar
                    bar_length = int((result["wpm"] / max_wpm) * max_bar_width) if max_wpm > 0 else 0
                    bar = "█" * bar_length
                    
                    # Display
                    line = f"  {date_str}: {bar} {result['wpm']:.1f}"
                    if row < height - 2:
                        try:
                            self.stdscr.addstr(row, 2, line[:width-3], curses.color_pair(4))
                        except curses.error:
                            pass
                    row += 1
        else:
            self.stdscr.addstr(row, 2, "No test history yet. Complete a test to see statistics!", 
                             curses.color_pair(3))
        
        # Footer
        footer = "Press ESC to return | Ctrl+C to quit"
        try:
            self.stdscr.addstr(height - 1, max(0, (width - len(footer)) // 2), 
                             footer, curses.color_pair(3))
        except curses.error:
            pass
        
        self.stdscr.refresh()
    
    def _handle_input(self, char: int):
        """Handle user input."""
        # Start test on first keypress
        if not self.test_active:
            self.test_active = True
            self.start_time = time.time()
        
        # ESC key - restart
        if char == 27:
            return False
        
        # Backspace
        if char in [curses.KEY_BACKSPACE, 127, 8]:
            if len(self.user_input) > 0:
                # Get the character being deleted
                deleted_char = self.user_input[-1]
                deleted_pos = len(self.user_input) - 1
                
                # Adjust counters based on whether it was correct or incorrect
                if deleted_pos < len(self.target_text):
                    if deleted_char == self.target_text[deleted_pos]:
                        if self.correct_chars > 0:
                            self.correct_chars -= 1
                    else:
                        if self.incorrect_chars > 0:
                            self.incorrect_chars -= 1
                
                # Remove the character
                self.user_input = self.user_input[:-1]
                self.current_position = len(self.user_input)
                
                if self.total_chars_typed > 0:
                    self.total_chars_typed -= 1
            return True
        
        # Regular character
        if 32 <= char <= 126:  # Printable ASCII
            typed_char = chr(char)
            self.user_input += typed_char
            self.current_position = len(self.user_input)
            self.total_chars_typed += 1
            
            # Check if character is correct
            if len(self.user_input) <= len(self.target_text):
                if self.user_input[-1] == self.target_text[len(self.user_input) - 1]:
                    self.correct_chars += 1
                else:
                    self.incorrect_chars += 1
            
            # Check if test is complete
            if self.user_input == self.target_text:
                self.test_completed = True
                self.end_time = time.time()
                self._save_result()
        
        return True
    
    def run(self):
        """Run the typing test main loop."""
        self.stdscr.timeout(100)  # 100ms timeout for non-blocking input
        viewing_history = False
        
        while True:
            # Clear and redraw
            self.stdscr.clear()
            
            if viewing_history:
                self._draw_history()
            elif self.test_completed:
                self._draw_results()
            else:
                self._draw_header()
                self._draw_text()
                self._draw_footer()
                self.stdscr.refresh()
            
            # Check time limit
            if self.test_active and not self.test_completed:
                if self._get_time_remaining() <= 0:
                    self.test_completed = True
                    self.end_time = time.time()
                    self._save_result()
            
            # Get input
            try:
                char = self.stdscr.getch()
                if char != -1:  # -1 means no input (timeout)
                    #this is buggy
                    if char in [ord('h'), ord('H')]:
                        if self.test_completed:
                            viewing_history = not viewing_history
                    # ESC key
                    elif char == 27:
                        if viewing_history:
                            viewing_history = False
                        else:
                            # Restart requested
                            return True
                    elif not viewing_history:
                        if not self._handle_input(char):
                            # Restart requested
                            return True
            except KeyboardInterrupt:
                return False
        
        return False


def main(stdscr):
    """Main entry point for the application."""
    duration,word_count = get_arguments()
    while True:
        test = TypingTest(stdscr, duration=duration, word_count=word_count)
        restart = test.run()
        if not restart:
            break


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("quit Monkey-CLI.")
