import unittest     # Framework to structure and run tests
import venv         # Module for creating virtual environments
import tempfile     # Create temporary directory
import os           # Handle file paths and directories
import shutil       # Handles file creation, deletion, copying, etc.
import subprocess   # Allows to spawn new processes

class TestVenv(unittest.TestCase):
    def setUp(self):
        """Runs before each test case to set up the environment."""
        self.temp_dir = tempfile.TemporaryDirectory()                           # Create temp. dir.
        self.venv_path = os.path.join(self.temp_dir.name, "test_env")           # Defines the path where the virt. env. will be created
        
    def tearDown(self):
        """Clean up the temp. dir. after the test."""
        self.temp_dir.cleanup()

    def test_create_venv(self):
        """Test if virt. env. is created successfully."""                       # Create virt. env. at self.venv_path.
        venv.create(self.venv_path, with_pip=True)                              # with_pip=True ensures that pip is installed
        
        # Check if the created directories exist
        self.assertTrue(os.path.isdir(self.venv_path))

        # Checks for a "bin" directory if OS is not Windows, else "Scripts"
        self.assertTrue(os.path.isdir(os.path.join(self.venv_path, "bin" if os.name != "nt" else "Scripts")))
        
        # Checks for a "lib" directory if OS is not Windows, else "Lib"
        self.assertTrue(os.path.isdir(os.path.join(self.venv_path, "lib" if os.name != "nt" else "Lib")))
        
        # Checks if the activation script exists
        activate_script = os.path.join(self.venv_path, "bin", "activate") if os.name != "nt" else os.path.join(
            self.venv_path, "Scripts", "activate.bat")
        self.assertTrue(os.path.exists(activate_script))
        
    def test_pyvenv_cfg(self):
        """Checks if pyvenv.cfg exists."""
        # Create virtual environment
        venv.create(self.venv_path, with_pip=True)
        # Create path to pyvenv.cfg file
        config_path = os.path.join(self.venv_path, "pyvenv.cfg")
        # Checks if the file exists
        self.assertTrue(os.path.isfile(config_path))
        
    def test_invalid_path(self):
        """Check if error is raised for invalid paths."""
        # Checks if OSError is raised at an invalid path
        with self.assertRaises(OSError):
            venv.create("invalid<>path", with_pip=True)
        
    def test_non_writeable_directory(self):
        """Checks if FileNotFoundError error is raised on non-existing file path."""
        with self.assertRaises(FileNotFoundError):
            venv.create("Z:\\invalid\\path", with_pip=True)
            
    def test_cleanup(self):
        """Makes sure virt. env. does not exist after deletion."""
        # Create virtual environment
        venv.create(self.venv_path, with_pip=True)
        # Delete virtual environment
        shutil.rmtree(self.venv_path)
        # Check if virtual environment's path still exists
        self.assertFalse(os.path.exists(self.venv_path))
        
    def test_pip_installed(self):
        """Checks if pip is installed in the virtual environment."""
        # Create virtual environment with pip
        venv.create(self.venv_path, with_pip=True)
        # Locate python.exe
        python_exec = os.path.join(self.venv_path, "Scripts", "python.exe")
        # Use subprocess.run to write command in cmd, capture output as a text
        result = subprocess.run([python_exec, "-m", "pip", "--version"], capture_output=True, text=True)
        # Checks if "pip" is in the output
        self.assertIn("pip", result.stdout)
        
    def test_pip_not_installed(self):
        """Checks if pip is indeed not installed when with_pip=False."""
        # Create virtual environment without pip
        venv.create(self.venv_path, with_pip=False)
        # Locate python.exe
        python_exec = os.path.join(self.venv_path, "Scripts", "python.exe")
        # Use subprocess.run to write command in cmd, capture output as text
        result = subprocess.run([python_exec, "-m", "pip", "--version"], capture_output=True, text=True)
        # Make sure "pip" is not in the output
        self.assertNotIn("pip", result.stdout)



if __name__ == '__main__':
    unittest.main()