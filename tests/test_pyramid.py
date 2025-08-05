"""
Unit tests for pyramid operations.
"""
import unittest
import numpy as np
from core.pyramid import build_pyramid

class TestPyramid(unittest.TestCase):
    
    def test_build_pyramid_gray(self):
        """Test pyramid building with grayscale mode."""
        # Create dummy frames
        frames = [np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8) for _ in range(5)]
        result = build_pyramid(frames, "gray")
        
        self.assertEqual(result.shape[0], 5)  # 5 frames
        self.assertEqual(len(result.shape), 3)  # (time, height, width)
        self.assertTrue(np.all(result >= 0) and np.all(result <= 1))  # Normalized values

if __name__ == '__main__':
    unittest.main()