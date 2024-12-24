from .exceptions import AddressError


class Memory:
    def __init__(self, block, start=0, offset=0):
        self.block = block
        self.start = start
        self.offset = offset
        self.current = 0
        self.min_addr = offset
        self.max_addr = offset + len(block) - 1

    def next_byte(self):
        if self.current < len(self.block):
            b = self.block[self.current]
            self.current += 1
            return b
        return None

    def rewind(self):
        self.current = 0

    @property
    def addr(self):
        return self.current + self.offset

    @addr.setter
    def addr(self, value):
        if value < self.min_addr or value > self.max_addr:
            raise AddressError(f"invalide addr {value:04x}")
        self.current = value - self.offset

    def __len__(self):
        return len(self.block)

    def addr_in(self, addr):
        return self.min_addr <= addr <= self.max_addr

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < self.min_addr or index > self.max_addr:
                raise AddressError(f"{index:04x} out of range")
            return self.block[index - self.offset]

        if not isinstance(index, slice):
            raise AddressError(f"invalide index {index!r}")

        start, stop = index.start, index.stop
        if start is None:
            start = self.min_addr

        if stop is None:
            stop = self.max_addr + 1

        if start < self.min_addr or stop > self.max_addr + 1:
            raise AddressError(f"invalide slice ${start}:${stop:04x}")

        return self.block[start - self.offset : stop - self.offset]
