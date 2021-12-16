#!/usr/bin/env python3
import functools
import operator
import utils


class BITSStream:
    def __init__(self, hex_data):
        if len(hex_data) % 2 != 0:
            hex_data += "0"
        self.data = bytes.fromhex(hex_data)
        self.pos = 0

    def next_bits(self, n):
        result = 0
        while n > 0:
            src_byte = self.pos // 8
            src_bit = self.pos % 8
            read_bits = min(n, 8 - src_bit)

            mask = (1 << read_bits) - 1
            src = self.data[src_byte]

            data = (src >> (8 - (src_bit + read_bits))) & mask
            result |= data

            n -= read_bits
            self.pos += read_bits
            result <<= n
        return result


class PacketBase:
    def __init__(self, version):
        self.version = version

    def print_header(self, indent):
        print("  " * indent, end="")
        print(f"{type(self).__name__} @ {self.version}: ", end="")


class Literal(PacketBase):
    def __init__(self, version, _value):
        super().__init__(version)
        self._value = _value

    def pretty_print(self, indent=0):
        self.print_header(indent)
        print(self._value)

    def version_sum(self):
        return self.version

    def value(self):
        return self._value


class Operator(PacketBase):
    def __init__(self, version, packets):
        super().__init__(version)
        self.packets = packets

    def pretty_print(self, indent=0):
        self.print_header(indent)
        print()
        for packet in self.packets:
            packet.pretty_print(indent + 1)

    def version_sum(self):
        return self.version + sum(p.version_sum() for p in self.packets)

    def values(self):
        return (p.value() for p in self.packets)


class Sum(Operator):
    def value(self):
        return sum(self.values())


class Product(Operator):
    def value(self):
        return functools.reduce(operator.mul, self.values(), 1)


class Minimum(Operator):
    def value(self):
        return min(self.values())


class Maximum(Operator):
    def value(self):
        return max(self.values())


class BinaryOperator(Operator):
    def __init__(self, version, packets):
        if len(packets) != 2:
            raise ValueError(f"{type(self)} requires 2 packets, got {packets}")
        super().__init__(version, packets)


class Gt(BinaryOperator):
    def value(self):
        if self.packets[0].value() > self.packets[1].value():
            return 1
        else:
            return 0


class Lt(BinaryOperator):
    def value(self):
        if self.packets[0].value() < self.packets[1].value():
            return 1
        else:
            return 0


class Eq(BinaryOperator):
    def value(self):
        if self.packets[0].value() == self.packets[1].value():
            return 1
        else:
            return 0


OPERATORS = {
    0: Sum,
    1: Product,
    2: Minimum,
    3: Maximum,
    5: Gt,
    6: Lt,
    7: Eq,
}


def read_literal_value(stream):
    value = 0
    while True:
        next_group = stream.next_bits(5)
        value <<= 4
        value |= next_group & 0b1111
        if next_group & 0b10000 == 0:
            return value


def read_packet(stream):
    version = stream.next_bits(3)
    type_id = stream.next_bits(3)
    if type_id == 4:
        return Literal(version, read_literal_value(stream))
    else:
        length_type = stream.next_bits(1)
        if length_type == 0:
            packets = []
            subpacket_length = stream.next_bits(15)
            end = stream.pos + subpacket_length
            while stream.pos < end:
                packets.append(read_packet(stream))
        else:
            subpacket_count = stream.next_bits(11)
            packets = [read_packet(stream) for _ in range(subpacket_count)]
        return OPERATORS[type_id](version, packets)


def main():
    stream = BITSStream(utils.test_input().read().strip())
    packet = read_packet(stream)
    packet.pretty_print()
    print(packet.value())


if __name__ == "__main__":
    main()
