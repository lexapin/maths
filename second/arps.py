# -*- coding: utf-8 -*-
# Пассивный и активный снифер ARP реализован на библиотеке scapy
from scapy.all import *


def arp_monitor_callback(pkt):
  if ARP in pkt and pkt[ARP].op in (1,2):
    return pkt.sprintf("%ARP.hwsrc% - %ARP.psrc%")


def sniff_arp():
  # Слушает сеть, фильтрует ARP-пакеты.
  # Для отображения результата использует call-back функцию
  # которая возвращает маску mac - ip
  # Для моей сети выдает следующий лог:
  # b0:c7:45:6b:ba:94 - 10.0.0.1
  # 30:e3:7a:69:47:77 - 10.0.0.106
  # 3c:83:75:e3:1e:44 - 10.0.0.120
  # b0:c7:45:6b:ba:94 - 10.0.0.1
  # 30:e3:7a:69:47:77 - 10.0.0.106
  # b0:c7:45:6b:ba:94 - 10.0.0.1
  # b0:c7:45:6b:ba:94 - 10.0.0.1

  sniff(prn=arp_monitor_callback, filter="arp", store=0)


def ping_arp():
  # Посылает широковещательный активный запрос ARP в сеть
  # Получает и выводит таблицу mac - ip
  # Для моей сети выдает следующий лог:
  # Received 2763 packets, got 2 answers, remaining 254 packets
  # b8:27:eb:97:1b:08 10.0.0.142
  # c4:8e:8f:b1:40:9d 10.0.0.148
  ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="10.0.0.0/24"),timeout=2)
  ans.summary(lambda (s,r): r.sprintf("%Ether.src% %ARP.psrc%") )


if __name__ == '__main__':
  # sniff_arp()
  ping_arp()