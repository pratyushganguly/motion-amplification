"""
Unit tests for amplification functions.
"""
import unittest
import numpy as np
from scipy import signal
from core.filters import apply_temporal_filter

class TestAmplify(unittest.TestCase):
    
    def test_apply_temporal_filter(self):
        """Test temporal filtering and amplification."""
        # Create synthetic data
        time_points = 100
        luma_stack = np.random.rand(time_points, 50, 50).astype(np.float32)
        
        # Create filter
        sos = signal.butter(2, [0.1, 0.4], btype='band', fs=30, output='sos')
        alpha = 10.0
        
        result = apply_temporal_filter(luma_stack, sos, alpha)
        
        # Check output shape matches input
        self.assertEqual(result.shape, luma_stack.shape)
        # Check that amplification was applied (result should differ from input)
        self.assertFalse(np.array_equal(result, luma_stack))

if __name__ == '__main__':
    unittest.main()