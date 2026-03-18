import socket
import threading
import argparse
import time

parser = argparse.ArgumentParser(description="Port Scanner")
parser.add_argument("-t", "--target", required=True, help="IP ou host alvo")
parser.add_argument("-p", "--ports", required=True, help="Range de portas (ex: 1-100)")
parser.add_argument("-o", "--output", help="Arquivo para salvar resultado")
args = parser.parse_args()

target = socket.gethostbyname(args.target)
start_port, end_port = map(int, args.ports.split("-"))

open_ports = []
lock = threading.Lock()

start_time = time.time()

def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    
    try:
        s.connect((target, port))
        
        try:
            service = socket.getservbyport(port)
        except:
            service = "desconhecido"
        
        with lock:
            print(f"[OPEN] {port:5} | {service}")
            open_ports.append((port, service))
    
    except:
        pass
    
    finally:
        s.close()

threads = []

print(f"\n🔎 Escaneando {args.target} ({target})")
print(f"📡 Portas: {start_port}-{end_port}\n")

for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = time.time()
duration = end_time - start_time

print("\n📊 Resultado final:")
for port, service in open_ports:
    print(f"{port:5} | {service}")

print(f"\n⏱️ Tempo total: {duration:.2f} segundos")

if args.output:
    with open(args.output, "w") as f:
        for port, service in open_ports:
            f.write(f"{port} - {service}\n")
    
    print(f"\n💾 Resultado salvo em: {args.output}")