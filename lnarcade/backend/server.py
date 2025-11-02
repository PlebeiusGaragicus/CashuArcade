"""
Backend server for arcade monitoring and admin control.

TODO: Implement using Streamlit or Flask for:
- Game statistics and monitoring
- Credit/coin management
- Remote configuration
- System health monitoring
"""

import logging
logger = logging.getLogger()


class ArcadeServerPage:
    """Placeholder backend server class."""
    
    def __init__(self, env_path: str):
        self.env_path = env_path
        logger.debug(f"ArcadeServerPage initialized with env_path: {env_path}")
    
    def start_server(self):
        """Start the backend server (not implemented)."""
        logger.info("Backend server thread started (no-op)")
        # TODO: Implement actual server
        pass
    
    def stop(self):
        """Stop the backend server (not implemented)."""
        logger.info("Backend server stopping (no-op)")
        pass
