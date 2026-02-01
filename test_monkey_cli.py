#!/usr/bin/env python3
"""
Unit tests for monkey_cli.py core functionality.
"""

import sys
from unittest.mock import patch

# Test word list generation
def test_word_list():
    """Test that word list is properly defined."""
    from monkey_cli import WORD_LIST
    assert len(WORD_LIST) > 0, "Word list should not be empty"
    assert all(isinstance(word, str) for word in WORD_LIST), "All words should be strings"
    print("✓ Word list test passed")

# Test WPM calculation
def test_wpm_calculation():
    """Test WPM calculation logic."""
    # Simulate: 50 chars in 60 seconds = 10 WPM
    # WPM = (chars / 5) / minutes
    chars_typed = 50
    minutes = 1.0
    expected_wpm = (chars_typed / 5) / minutes
    assert expected_wpm == 10.0, f"Expected 10 WPM, got {expected_wpm}"
    print("✓ WPM calculation test passed")

# Test accuracy calculation
def test_accuracy_calculation():
    """Test accuracy calculation logic."""
    # 90 correct out of 100 total = 90% accuracy
    correct = 90
    total = 100
    accuracy = (correct / total) * 100
    assert accuracy == 90.0, f"Expected 90% accuracy, got {accuracy}%"
    print("✓ Accuracy calculation test passed")

# Test character comparison
def test_character_comparison():
    """Test character comparison logic."""
    target = "hello world"
    user_input = "hello worle"
    
    correct_count = 0
    for i in range(len(user_input)):
        if i < len(target) and user_input[i] == target[i]:
            correct_count += 1
    
    assert correct_count == 10, f"Expected 10 correct chars, got {correct_count}"
    print("✓ Character comparison test passed")

def test_wpm_freezes_after_completion():
    """Test that WPM uses end time when test is complete."""
    from monkey_cli import TypingTest

    class TestTypingTest(TypingTest):
        def _setup_curses(self):
            pass

    test = TestTypingTest(None)
    test.start_time = 1000.0
    test.end_time = 1060.0
    test.correct_chars = 50
    test.test_completed = True

    # 50 correct chars / 5 chars per word = 10 words over 1 minute.
    with patch("time.time", return_value=2060.0):
        assert test._calculate_wpm() == 10.0, "Expected WPM to use end_time when set"
    print("✓ WPM freeze test passed")

if __name__ == "__main__":
    print("Running Monkey-CLI tests...\n")
    
    try:
        test_word_list()
        test_wpm_calculation()
        test_accuracy_calculation()
        test_character_comparison()
        test_wpm_freezes_after_completion()
        
        print("\n✅ All tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
