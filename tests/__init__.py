"""
Test suite for financial news sentiment analysis project.

Run tests with: python -m pytest tests/
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test that basic imports work"""
    try:
        import pandas as pd
        import numpy as np
        assert True
    except ImportError:
        assert False, "Basic imports failed"

if __name__ == "__main__":
    test_imports()
    print(" Basic imports test passed")
