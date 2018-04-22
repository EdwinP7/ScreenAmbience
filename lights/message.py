import ctypes
import socket
import struct
import sys
from bitstruct import pack, byteswap, calcsize
from binascii import hexlify
from time import sleep, clock

frame_header_format = 'u16u2u1u1u12u32'
frame_header_byteswap = '224'

frame_address_format = 'u64u48u6u1u1u8'
frame_address_byteswap = '8611'

protocol_header_format = 'u64u16u16'
protocol_header_byteswap = '822'

# Packet building reference on LIFX forums: https://community.lifx.com/t/building-a-lifx-packet/59/3
def send_packet(packet):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    result = bytes.fromhex(packet.hex())
    sock.sendto(result, ("10.0.0.255", 56700))

def sizeof(format):
    return calcsize(format)

def make_frame_header(size, origin, tagged, addressable, protocol, source):
    unswapped_header = pack(frame_header_format, size, origin, 0, addressable, protocol, source)
    frame_header = byteswap(frame_header_byteswap, unswapped_header)
    return frame_header

def make_frame_address(target, ack_required, res_required, sequence):
    mac = '142626d573d0'
    mac = int(mac, 16)

    unswapped_header = pack(frame_address_format, mac, 0, 0, ack_required, res_required, sequence)
    
    frame_address = byteswap(frame_address_byteswap, unswapped_header)
    return frame_address


def make_protocol_header(message_type):
    unswapped_header = pack(protocol_header_format, 0, message_type, 0)
    protocol_header = byteswap(protocol_header_byteswap, unswapped_header)
    return protocol_header


def set_color(average_screen_color, start, end):
    payload_format = 'u8u8u16u16u16u16u32u8'
    payload_byteswap = '11222241'

    packet_size = (sizeof(frame_header_format + frame_address_format + protocol_header_format + payload_format)) / 8
    frame_header = make_frame_header(packet_size, 0, 0, 1, 1024, 0)
    frame_address = make_frame_address(0, 0, 0, 0)
    protocol_header = make_protocol_header(501)
    header = frame_header + frame_address + protocol_header
    unswapped_payload = pack (payload_format, start, end, *average_screen_color, 1)
    payload = byteswap(payload_byteswap, unswapped_payload)
    packet = header + payload
    send_packet(packet)