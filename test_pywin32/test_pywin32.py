import unittest             # Testing framework
import win32serviceutil     # Utility functions for managing Win services
import win32service         # Contains constants and functions for Win services
import win32event           # Event handling functions for Win events

class TestWin32ServiceUtil(unittest.TestCase):
    """Tests for win32serviceutil module."""
    # Windows Update Service
    SERVICE_NAME = "wuauserv"
    
    def test_query_service_status(self):
        """Test querying the status of a known Windows server."""
        # Retrieve status from the Windows Update Service
        status = win32serviceutil.QueryServiceStatus(self.SERVICE_NAME)
        self.assertIsInstance(status, tuple)
        self.assertGreater(len(status), 0)
        
    def test_service_running(self):
        """Check if the service is running."""
        # Get only the 2nd element from the tuple, as that reflects the service current state
        status = win32serviceutil.QueryServiceStatus(self.SERVICE_NAME)[1]
        #Check if state is either running (4), stopped (1), paused (7).
        self.assertIn(status, [win32service.SERVICE_RUNNING, win32service.SERVICE_STOPPED, win32service.SERVICE_PAUSED])



if __name__ == '__main__':
    unittest.main()