from ._core import _process_array

def process_array(input_array):
    """
    Wrapper function for process_array with some additional checks.
    
    Args:
        input_array (numpy.ndarray): Input 2D NumPy array
    
    Returns:
        numpy.ndarray: Processed array
    """
    return _process_array(input_array)

__all__ = ['process_array']