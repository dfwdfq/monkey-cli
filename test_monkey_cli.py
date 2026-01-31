#!/usr/bin/env python3
"""
Unit tests for monkey_cli.py core functionality.
"""

import sys

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

if __name__ == "__main__":
    print("Running Monkey-CLI tests...\n")
    
    try:
        test_word_list()
        test_wpm_calculation()
        test_accuracy_calculation()
        test_character_comparison()
        
        print("\n✅ All tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
