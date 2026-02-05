import curses
import time
import random
from typing import List, Tuple
from datetime import datetime
from data_storage import DataStorage
from word_list import load_word_list


class TypingTest:
    """Main typing test application class."""
    
    def __init__(self,
                 stdscr,
                 duration: int      = 30,
                 word_count: int    = 50,
                 show_history: bool = False,
                 dict_name:str      = "default"):
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
        self.dict_name = dict_name
        
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
        self.show_history = show_history

        
        self.results_drawn = False #use this flag to prevent from re-calculating accuracy
        self.wpm = None
        self.accuracy = None
        
        
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
        w_list = load_word_list(self.dict_name)
        random.shuffle(w_list)
        return [random.choice(w_list) for _ in range(self.word_count)]
    
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
        """Draw the target text with color-coded characters in a single centered line."""
        height, width = self.stdscr.getmaxyx()
        
        center_row = height // 2
        
        max_visible_chars = width - 4
        
        if self.current_position <= max_visible_chars // 2:
            start_pos = 0
        elif len(self.target_text) - self.current_position <= max_visible_chars // 2:
            start_pos = max(0, len(self.target_text) - max_visible_chars)
        else:
            start_pos = self.current_position - max_visible_chars // 2
        
        end_pos = min(len(self.target_text), start_pos + max_visible_chars)
        
        text_to_display = self.target_text[start_pos:end_pos]
        start_col = (width - len(text_to_display)) // 2
        
        for i in range(len(text_to_display)):
            actual_pos = start_pos + i
            char = text_to_display[i]
            col = start_col + i
            
            if actual_pos < len(self.user_input):
                if self.user_input[actual_pos] == char:
                    color = curses.color_pair(1)
                else:
                    color = curses.color_pair(2)
            elif actual_pos == len(self.user_input):
                color = curses.color_pair(3) | curses.A_UNDERLINE
            else:
                color = curses.color_pair(3)
            
            try:
                self.stdscr.addstr(center_row, col, char, color)
            except curses.error:
                pass
        
        if len(self.user_input) >= len(self.target_text):
            try:
                self.stdscr.addstr(center_row, start_col + len(text_to_display), 
                                 "|", curses.color_pair(3) | curses.A_BOLD)
            except curses.error:
                pass
        
        progress_width = 40
        progress_bar = "[" + "=" * int((self.current_position / len(self.target_text)) * progress_width) + \
                       ">" + " " * (progress_width - int((self.current_position / len(self.target_text)) * progress_width)) + "]"
        progress_text = f"Position: {self.current_position}/{len(self.target_text)}"
        
        try:
            self.stdscr.addstr(center_row + 1, (width - len(progress_bar)) // 2, 
                             progress_bar, curses.color_pair(3))
            self.stdscr.addstr(center_row + 2, (width - len(progress_text)) // 2,
                             progress_text, curses.color_pair(4))
        except curses.error:
            pass
    
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
        
        #Results
        if not self.results_drawn:
            self.wpm = self._calculate_wpm()
            self.accuracy = self._calculate_accuracy()
            self.results_drawn = True
        
        results = [
            f"WPM: {self.wpm:.2f}",
            f"Accuracy: {self.accuracy:.2f}%",
            f"Correct Characters: {self.correct_chars}",
            f"Incorrect Characters: {self.incorrect_chars}",
            f"Total Characters: {self.total_chars_typed}"
        ]
        
        for i, line in enumerate(results):
            self.stdscr.addstr(height // 2 - 4 + i, max(0, (width - len(line)) // 2), 
                             line, curses.color_pair(4))
        
        # Instructions
        instruction = "Press ESC to restart |  Ctrl+C to quit"
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
        footer = "Ctrl+C to quit"
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
        self.results_drawn = False
        while True:
            # Clear and redraw
            self.stdscr.clear()
            
            if self.show_history:
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
                    # ESC key
                    if char == 27:
                        # Restart requested
                        return True
                    #THIS IS LITERALLY NOT OK
                    #but...
                    #This dirty af hack fixes vibe-coded bug
                    #that was inserted on line after my hack
                    #by some random indian guy, who wrote
                    #this project with his only companion - Copilot.
                    #It works and it's good enough, so let it be.
                    #Let this code will be forever and ever crap.                
                    if not self.results_drawn:
                        if not self._handle_input(char):
                            # Restart requested
                            return True
            except KeyboardInterrupt:
                return False
        
        return False
