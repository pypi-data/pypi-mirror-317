import os
import subprocess
import logging
import platform  # For platform detection
import coloredlogs
from colorama import Fore

# Set up logging
logger = logging.getLogger(Fore.RED + "+ HLS + ")
coloredlogs.install(level='DEBUG', logger=logger)

class HLS:
    def __init__(self):
        self.manifest_url = None
        self.output_name = None
        self.decryption_key = None  # Default to None, making it optional
        self.binary_path = self._get_binary_path()

    def _get_binary_path(self):
        """Determine the correct binary path based on the platform."""
        base_path = os.path.join(os.path.dirname(__file__), 'bin', 'N_m3u8DL-RE')
        
        if platform.system() == 'Windows':
            binary = f"{base_path}.exe"
        elif platform.system() == 'Linux':
            binary = base_path  # Linux binaries usually have no extension
        elif platform.system() == 'Darwin':  # macOS
            binary = base_path  # Adjust if necessary for macOS-specific binaries
        else:
            logger.error(f"Unsupported platform: {platform.system()}")
            raise OSError(f"Unsupported platform: {platform.system()}")
        
        if not os.path.exists(binary):
            logger.error(f"Binary not found: {binary}")
            raise FileNotFoundError(f"Binary not found: {binary}")
        
        return binary

    def hls_downloader(self):
        if not self.manifest_url:
            logger.error("Manifest URL is not set.")
            return
        
        command = self._build_command()
        
        # logger.debug(f"Running command: {command}")
        self._execute_command(command)

    def _build_command(self):
        # Build the command to pass to os.system()
        command = [
            self.binary_path,  # Path to the binary
            self.manifest_url,  # Manifest URL (no need for quotes)
            '--auto-select',
            '-mt',
            '--thread-count', '12',
            '--save-dir', 'downloads',
            '--tmp-dir', 'downloads',
            '--save-name', self.output_name  # The output name (no quotes)
        ]
        
        # Only add decryption_key if it's provided
        if self.decryption_key:
            command.append(f'--key {self.decryption_key}')  # Ensure correct format: KID:KEY
        
        # Join the command as a single string for system execution
        command_str = ' '.join(command)
        # logger.debug(f"Command string: {command_str}")
        
        return command_str

    def _execute_command(self, command):
        try:
            # Use os.system to run the command as a string
            result = os.system(command)
            
            if result == 0:
                logger.info("Downloaded using N_m3u8DL-RE successfully.")
            else:
                logger.error(f"Download failed with result code: {result}")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")