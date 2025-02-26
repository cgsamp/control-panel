import time

class I2CDevice:
    def __init__(self, i2c: I2C, device_address: int) -> None:
        self.i2c = i2c
        self.device_address = device_address

    def write(
        self, buf: ReadableBuffer, *, start: int = 0, end: Optional[int] = None
    ) -> None:
        if end is None:
            end = len(buf)
        self.i2c.writeto(self.device_address, buf)
        
    def __exit__(
        self,
        exc_type: Optional[Type[type]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        pass
        #self.i2c.unlock()
        return False

    def __enter__(self) -> "I2CDevice":
        pass
        #while not self.i2c.try_lock():
         #   time.sleep(0)
        return self
