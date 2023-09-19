from scapy.all import rdpcap, TCP

# 读取 PCAP 文件
packets = rdpcap("/root/traffic/cl2022_iothoneypot.pcap")

# 打开文本文件以保存 Telnet 数据
with open("/root/traffic/telnet_data.txt", "w") as f:
    for packet in packets:
        if packet.haslayer(TCP) and (packet[TCP].dport == 23 or packet[TCP].sport == 23):
            # 提取 Telnet 数据
            telnet_data = packet[TCP].payload.load if packet[TCP].payload else ""
            
            # 检查 telnet_data 的类型并适当地写入文件
            if isinstance(telnet_data, bytes):
                f.write(telnet_data.decode(errors='replace'))
            else:
                f.write(telnet_data)
            
            f.write("\n" + "-"*50 + "\n")





