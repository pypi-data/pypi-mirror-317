import os
import dotenv
import argparse
from .constants import (DEFAULT_VERSION, DEFAULT_THREAD_UPLOAD, RETRY_DELAY_SECONDS)

class Config:
    def __init__(self, 
                api_url: str = None,
                token: str = None,
                number_threads: int = DEFAULT_THREAD_UPLOAD,
                retry_delay_seconds: int = RETRY_DELAY_SECONDS) -> None:

        # eviroment config
        self.api_url = api_url
        self.version = DEFAULT_VERSION # default 
        self.token = token
        self.number_threads = number_threads
        self.retry_delay_seconds = retry_delay_seconds
    
