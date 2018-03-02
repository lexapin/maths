# -*- coding: utf-8 -*-
# Пассивный снифер ARP реализован на библиотеке scapy
from scapy.all import *


def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2):
        return pkt.sprintf("%ARP.hwsrc% - %ARP.psrc%")


# Слушает сеть, фильтрует ARP-пакеты.
# Для отображения результата использует call-back функцию
# которая возвращает маску mac - ip
sniff(prn=arp_monitor_callback, filter="arp", store=0)