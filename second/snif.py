import socket
import struct
import signal


CTRL_C = False


def event_function(*args, **kwargs):
  global CTRL_C
  CTRL_C = True
  printf("CTRC+C")


signal.signal(signal.SIGINT, event_function)


class Ethernet(object):
  def __init__(self, data):
    dest, src, proto = struct.unpack('! 6s 6s H', data[:14])
    self.eth_dest = self.translate_mac(dest)
    self.eth_src = self.translate_mac(src)
    self.eth_proto = socket.htons(proto)
    self.data = data[14:]

  def translate_mac(self, mac_byte):
    mac_str = map('{0:02x}'.format, map(ord, mac_byte))
    return ':'.join(mac_str).upper()

  def __repr__(self):
    return '\nEthernet Frame:\nDestination: {}, Source: {}, Protocol: {}'\
      .format(self.eth_dest, self.eth_src, self.eth_proto)


class IPv4(Ethernet):
  def __init__(self, data):
    super(IPv4, self).__init__(data)
    if self.eth_proto == 8:
      self.encode_ipv4_data()
    else:
      self.IPv4=False

  def encode_ipv4_data(self):
    ipv4data = self.data
    version_header_length = ord(ipv4data[0])
    self.ipv4_version = version_header_length >> 4
    self.ipv4_header_length = (version_header_length & 15) * 4
    self.ipv4_ttl, self.ipv4_proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', ipv4data[:20])
    self.ipv4_src = self.encode_ipv4_address(src)
    self.ipv4_target = self.encode_ipv4_address(target)
    self.data = ipv4data[self.ipv4_header_length:]

  def encode_ipv4_address(self, addr):
    return '.'.join(map(str, map(ord, addr)))

  def __repr__(self):
    eth_repr = super(IPv4, self).__repr__()
    if not getattr(self, 'IPv4', True): return eth_repr
    ipv4_repr = '\n\tIPv4 Packet:'
    ipv4_repr+= '\n\t\tVersion: {}, Header Length: {}, TTL: {},'\
      .format(self.ipv4_version,
              self.ipv4_header_length,
              self.ipv4_ttl,
      )
    ipv4_repr += '\n\t\tProtocol: {}, Source: {}, Target: {}'\
      .format(self.ipv4_proto,
              self.ipv4_src,
              self.ipv4_target,
      )
    return eth_repr+ipv4_repr


def scan_network():
  global CTRL_C
  connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
  while not CTRL_C:
    data, addr = connection.recvfrom(65535)
    ethernet = IPv4(data)
    print(ethernet)


if __name__ == '__main__':
  scan_network()