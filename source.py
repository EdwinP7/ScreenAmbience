import ctypes
import socket
import struct
from bitstruct import pack, byteswap, calcsize
from binascii import hexlify
from time import sleep, clock
from screen.colors import ScreenColor
    
frame_header_format = 'u16u2u1u1u12u32'
frame_header_byteswap = '224'

frame_address_format = 'u64u48u6u1u1u8'
frame_address_byteswap = '8611'

protocol_header_format = 'u64u16u16'
protocol_header_byteswap = '822'

def send_packet(packet):
    # Broadcast the packet as a UDP message to all bulbs on the network. (Your broadcast IP address may vary?)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    result = bytes.fromhex(packet.hex())
    sock.sendto(result, ("10.0.0.255", 56700))

def sizeof(format):
    return calcsize(format)

def make_frame_header(size, origin, tagged, addressable, protocol, source):
    # Make the frame header, specifying the size of the whole packet, the origin, whether it's tagged and addressable,
    # what protocol it uses, and what source it comes from)
    unswapped_header = pack(frame_header_format, size, origin, 0, addressable, protocol, source)
    #print "\nunswapped frame header: %s" % hexlify(unswapped_header)
    frame_header = byteswap(frame_header_byteswap, unswapped_header)
    #print "frame header: %s" % hexlify(frame_header)
    return frame_header

def make_frame_address(target, ack_required, res_required, sequence):
    # Make the frame address header, specifying the target, whether acknowledgement or response are required, and what
    # number packet in the current sequence this is.
    mac = '142626d573d0'
    mac = int(mac, 16)

    unswapped_header = pack(frame_address_format, mac, 0, 0, ack_required, res_required, sequence)
    #print "\nunswapped frame address: %s" % hexlify(unswapped_header)
    
    frame_address = byteswap(frame_address_byteswap, unswapped_header)
    return frame_address


def make_protocol_header(message_type):
    # Make the protocol header, specifying the message type.
    unswapped_header = pack(protocol_header_format, 0, message_type, 0)
    #print "\nunswapped protocol header: %s" % hexlify(unswapped_header)
    protocol_header = byteswap(protocol_header_byteswap, unswapped_header)
    #print "protocol header: %s" % hexlify(protocol_header)
    return protocol_header


def set_color(screen_space):
    # Set the format of the payload for this type of message
    payload_format = 'u8u16u16u16u16u32'
    payload_byteswap = '122224'

    # Use the payload format and the header formats to calculate the total size of the packet, in bytes
    packet_size = (sizeof(frame_header_format + frame_address_format + protocol_header_format + payload_format)) / 8
    #print "\npacket size is %s" % packet_size

    # CREATE THE HEADERS
    # 1. Frame header: use packet_size to indicate the length, set origin to 0, set tagged to 1 (because we want all bulbs
    # to respond to it), set addressable to 1, set protocol to 1024, set source to 0 (because we're a dumb client and
    # don't care about responses).
    frame_header = make_frame_header(packet_size, 0, 0, 1, 1024, 0)
    # 2. Frame address: set target to 0 (because we want all bulbs to respond), set ack_required and res_required to 0
    # (because we don't need an acknowledgement or response), and sequence number to 0 (because it doesn't matter what
    # order in the sequence this message is).
    frame_address = make_frame_address(0, 0, 0, 0)
    # 3. Protocol header: set message type to 102, which is a "SetColor" message.
    protocol_header = make_protocol_header(102)
    # 4. Add all the headers together.
    header = frame_header + frame_address + protocol_header
    # CREATE THE PAYLOAD
    # 1. Convert the colours into the right format
    
    average_screen_color = screen_space.average_color()

    
    #print "\nhue %s %s\nsaturation %s %s\nbrightness %s %s\nkelvin %s %s\nduration %s %s" % (hue, hex(hue), saturation, hex(saturation), brightness, hex(brightness), kelvin, hex(kelvin), duration, hex(duration))
    # 2. Pack the payload information
    unswapped_payload = pack (payload_format, 0, *average_screen_color)
    #print "\nunswapped payload: %s" % hexlify(unswapped_payload)
    payload = byteswap(payload_byteswap, unswapped_payload)
    #print "payload: %s" % hexlify(payload)

    # CREATE THE PACKET AND SEND IT
    packet = header + payload
    send_packet(packet)



def stream_lights():
    screen_space = ScreenColor(1920, 1080, 10, 450, 4500)
    print("Gathering screen colors...")
    while True:
        sleep(0.5)
        set_color(screen_space)

if __name__ == '__main__':
    stream_lights()
