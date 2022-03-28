import os
import fcntl

class FileLock:
    """ File Lock to coordinate between process """
    def __init__(self, lock_path: str) -> None:
        self.path = lock_path
        self.lock_file = None

    def try_lock(self, timeout:float = 0.1) -> bool:
        """ try to lock return False it timed out or fail to lock """
        if self.lock_file is not None:
            return True
        fd = os.open(self.path, os.O_RDWR | os.O_CREAT | os.O_TRUNC) 
        start_time = current_time = time.time()
        while current_time < start_time + timeout:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX| fcntl.LOCK_NB)
            except (IOError, OSError):
                pass
            else:
                self.lock_file = fd
                break
            time.sleep(0.1)
            current_time = time.time()
        if self.lock_file is None:
            os.close(fd)
        return self.lock_file is not None

    def lock(self):
        """ lock and block """
        if self.lock_file is not None:
            return True
        fd = os.open(self.path, os.O_RDWR | os.O_CREAT | os.O_TRUNC) 
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
        except (IOError, OSError):
            pass
        else:
            self.lock_file = fd
        if self.lock_file is None:
            os.close(fd)
        return self.lock_file is not None

    def unlock(self):
        """ unlock """
        if self.lock_file:
            fcntl.flock(self.lock_file, fcntl.LOCK_UN)
            os.close(self.lock_file)
            self.lock_file = None

    def __enter__(self):
        self.lock()
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.unlock()
