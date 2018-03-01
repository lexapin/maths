# Снифер на socket-ах
# Запускать под пользователем root
# sudo python3 snif.py
# Время выполнения задания 5 часов

import socket
import struct
import signal


CTRL_C = False


def event_function(*args, **kwargs):
  """
  Функия обработчик на событие ctrl+c для остановки
  бесконечного цикла ловли пакетов.
  Останавливает по переменной CTRL_C.
  :param args:
  :param kwargs:
  :return:
  """
  global CTRL_C
  CTRL_C = True
  print("CTRC+C")

# Регистрация события CTRL+С
signal.signal(signal.SIGINT, event_function)


class Ethernet(object):
  """
  Базовый класс по обработке пакетов
  """
  def __init__(self, data):
    """
    Получает сырые данные с сокета и расшифровывает первые 14 байт:
    МАК отправителя 6 байт
    МАК получателя 6 байт
    Тип пакета 2 байта
    :param data:
    """
    dest, src, proto = struct.unpack('! 6s 6s H', data[:14])
    self.eth_dest = self.translate_mac(dest)
    self.eth_src = self.translate_mac(src)
    self.eth_proto = socket.htons(proto)
    self.data = data[14:]

  def translate_mac(self, mac_byte):
    """
    Получает мак адрес в байтах
    И переводит его в мак HEX
    :param mac_byte:
    :return: formated mac_str
    """
    mac_str = map('{0:02x}'.format, mac_byte)
    return ':'.join(mac_str).upper()

  def __repr__(self):
    """
    Отображает загаловок ethernet пакета
    :return:
    """
    return '\nEthernet Frame:\nDestination: {}, Source: {}, Protocol: {}'\
      .format(self.eth_dest, self.eth_src, self.eth_proto)


class IPv4(Ethernet):
  """
  Читает payload ethernet-фрейма
  """
  def __init__(self, data):
    # Инициализирует пакет IPv4
    super(IPv4, self).__init__(data)
    if self.eth_proto == 8:
      self.encode_ipv4_data()
    else:
      self.IPv4=False

  def encode_ipv4_data(self):
    """
    Берет 20 байт с payload ethernet и декодирует
    Здесь лучше смотреть изображение фрейма IPv4
    Потому что в байтах закодировано несколько переменных
    :return:
    """
    ipv4data = self.data
    version_header_length = ipv4data[0]
    self.ipv4_version = version_header_length >> 4
    self.ipv4_header_length = (version_header_length & 15) * 4
    self.ipv4_ttl, self.ipv4_proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', ipv4data[:20])
    self.ipv4_src = self.encode_ipv4_address(src)
    self.ipv4_target = self.encode_ipv4_address(target)
    self.data = ipv4data[self.ipv4_header_length:]

  def encode_ipv4_address(self, addr):
    """
    Приводит ip адрес к виду xxx.xxx.xxx.xxx
    :param addr:
    :return:
    """
    return '.'.join(map(str, addr))

  def __repr__(self):
    """
    Печатает заголовок пакета IPv4
    :return:
    """
    eth_repr = super(IPv4, self).__repr__()
    if not getattr(self, 'IPv4', True): return eth_repr
    ipv4_repr = '\n\tIPv4 Packet:'
    ipv4_repr+= '\n\tVersion: {}, Header Length: {}, TTL: {},'\
      .format(self.ipv4_version,
              self.ipv4_header_length,
              self.ipv4_ttl,
      )
    ipv4_repr += '\n\tProtocol: {}, Source: {}, Target: {}'\
      .format(self.ipv4_proto,
              self.ipv4_src,
              self.ipv4_target,
      )
    return eth_repr+ipv4_repr

  def encode_ipv4_payload(self):
    """
    Смотрит какой тип данных несет в себе IPv4
    И декодит его если знает
    Если не идентифицирует то возвращает исходны IPv4 пакет
    :return:
    """
    if not getattr(self, 'IPv4', True): return self
    packets = {
      1:  ICMP,
      6:  TCP,
      17: UDP,
    }
    Protocol = packets.get(self.ipv4_proto)
    if Protocol is None: return self
    return Protocol(self)


class ICMP(object):
  """
  ICMP
  """
  def __init__(self, ipv4):
    self.ipv4 = ipv4
    self.encode_ICMP()

  def encode_ICMP(self):
    data = self.ipv4.data
    self.type, self.code, self.checksum = struct.unpack('! B B H', data[:4])
    self.data = data[4:]

  def __repr__(self):
    ipv4_repr = self.ipv4.__repr__()
    icmp_repr = '\n\t\tICMP Packet:'
    icmp_repr += '\n\t\tType: {}, Code: {}, Checksum: {},'.format(self.type, self.code, self.checksum)
    return ipv4_repr+icmp_repr


class TCP(object):
  """
  TCP
  """
  def __init__(self, ipv4):
    self.ipv4 = ipv4
    self.encode_TCP()

  def encode_TCP(self):
    data = self.ipv4.data
    (self.src_port, self.dest_port, self.sequence, self.acknowledgment, offset_reserved_flags) = struct.unpack(
      '! H H L L H', data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    self.flag_urg = (offset_reserved_flags & 32) >> 5
    self.flag_ack = (offset_reserved_flags & 16) >> 4
    self.flag_psh = (offset_reserved_flags & 8) >> 3
    self.flag_rst = (offset_reserved_flags & 4) >> 2
    self.flag_syn = (offset_reserved_flags & 2) >> 1
    self.flag_fin = offset_reserved_flags & 1
    self.data = data[offset:]
    # TODO: Здесь можно прочитать HTTP пакет

  def __repr__(self):
    ipv4_repr = self.ipv4.__repr__()
    tcp_repr = '\n\t\tTCP Segment:'
    tcp_repr += '\n\t\tSource Port: {}, Destination Port: {}'.format(self.src_port, self.dest_port)
    tcp_repr += '\n\t\tSequence: {}, Acknowledgment: {}'.format(self.sequence, self.acknowledgment)
    tcp_repr += '\n\t\tFlags:'
    tcp_repr += '\n\t\tURG: {}, ACK: {}, PSH: {}'.format(self.flag_urg, self.flag_ack, self.flag_psh)
    tcp_repr += '\n\t\tRST: {}, SYN: {}, FIN: {}'.format(self.flag_rst, self.flag_syn, self.flag_fin)
    return ipv4_repr + tcp_repr


class UDP(object):
  """
  UDP
  """
  def __init__(self, ipv4):
    self.ipv4 = ipv4
    self.encode_UDP()

  def encode_UDP(self):
    data = self.ipv4.data
    self.src_port, self.dest_port, self.size = struct.unpack('! H H 2x H', data[:8])
    self.data = data[8:]

  def __repr__(self):
    ipv4_repr = self.ipv4.__repr__()
    udp_repr = '\n\t\tUDP Segment:'
    udp_repr += '\n\t\tSource Port: {}, Destination Port: {}, Length: {}'.format(self.src_port, self.dest_port, self.size)
    return ipv4_repr + udp_repr

def scan_network():
  # Сканирует сеть
  global CTRL_C
  # Сканируем сеть. Смотрим сырые пакеты.
  connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
  while not CTRL_C:
    # Читаем буфер
    data, addr = connection.recvfrom(65535)
    # Пробуем его как IPv4
    ipv4 = IPv4(data)
    # Если пакет IPv4 то его можно парсить дальше
    packet = ipv4.encode_ipv4_payload()
    # Печатаем параметры пакета
    print(packet)


if __name__ == '__main__':
  scan_network()