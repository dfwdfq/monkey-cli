#!/usr/bin/env python3
"""
Tests for the data storage module.
"""

import os
import tempfile
from data_storage import DataStorage


def test_data_storage():
    """Test data storage functionality."""
    print("Running Data Storage tests...")
    
    # Create temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        # Test 1: Initialization
        storage = DataStorage(temp_file)
        assert os.path.exists(temp_file), "Data file should be created"
        print("✓ Initialization test passed")
        
        # Test 2: Save result
        storage.save_result(
            wpm=50.5,
            accuracy=95.5,
            correct_chars=200,
            incorrect_chars=10,
            total_chars=210,
            duration=30
        )
        results = storage.get_all_results()
        assert len(results) == 1, "Should have 1 result"
        assert results[0]["wpm"] == 50.5, "WPM should match"
        assert results[0]["accuracy"] == 95.5, "Accuracy should match"
        print("✓ Save result test passed")
        
        # Test 3: Multiple results
        for i in range(5):
            storage.save_result(
                wpm=50 + i,
                accuracy=90 + i,
                correct_chars=100 + i * 10,
                incorrect_chars=5 + i,
                total_chars=110 + i * 10,
                duration=30
            )
        results = storage.get_all_results()
        assert len(results) == 6, "Should have 6 results total"
        print("✓ Multiple results test passed")
        
        # Test 4: Get recent results
        recent = storage.get_recent_results(3)
        assert len(recent) == 3, "Should return 3 recent results"
        assert recent[-1]["wpm"] == 54, "Last result should have WPM 54"
        print("✓ Recent results test passed")
        
        # Test 5: Get statistics
        stats = storage.get_statistics()
        assert stats["total_tests"] == 6, "Should have 6 total tests"
        assert stats["best_wpm"] == 54, "Best WPM should be 54"
        assert stats["average_wpm"] > 0, "Average WPM should be calculated"
        print("✓ Statistics test passed")
        
        # Test 6: Clear history
        storage.clear_history()
        results = storage.get_all_results()
        assert len(results) == 0, "History should be empty"
        stats = storage.get_statistics()
        assert stats["total_tests"] == 0, "Total tests should be 0"
        print("✓ Clear history test passed")
        
        print("\n✅ All data storage tests passed!")
        
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)


if __name__ == "__main__":
    test_data_storage()
