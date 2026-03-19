import socket
import threading
import argparse
import time

# =============================
# CONFIGURAÇÃO DOS ARGUMENTOS
# =============================
parser = argparse.ArgumentParser(description="Port Scanner with Banner Grabbing")
parser.add_argument("-t", "--target", required=True, help="IP ou host alvo")
parser.add_argument("-p", "--ports", required=True, help="Porta ou range (ex: 80 ou 1-100)")
parser.add_argument("-o", "--output", help="Arquivo para salvar resultado")
args = parser.parse_args()

# =============================
# RESOLVER HOST → IP
# =============================
try:
    target = socket.gethostbyname(args.target)
except socket.gaierror:
    print("❌ Host inválido")
    exit()

# =============================
# TRATAR PORTAS
# =============================
if "-" in args.ports:
    start_port, end_port = map(int, args.ports.split("-"))
else:
    start_port = end_port = int(args.ports)

# =============================
# VARIÁVEIS GLOBAIS
# =============================
open_ports = []
lock = threading.Lock()
start_time = time.time()

# =============================
# FUNÇÃO DE SCAN
# =============================
def scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        # Tenta conectar (TCP handshake)
        s.connect((target, port))

        # =============================
        # BANNER GRABBING
        # =============================
        try:
            if port in [80, 8080]:
                # Envia requisição HTTP
                s.send(b"HEAD / HTTP/1.1\r\nHost: example.com\r\n\r\n")
            else:
                # Para outros serviços (ex: SSH)
                s.send(b"\r\n")

            banner = s.recv(1024).decode(errors="ignore").strip()

            if not banner:
                banner = "sem resposta"

        except:
            banner = "erro ao capturar banner"

        # =============================
        # PRINT THREAD-SAFE
        # =============================
        with lock:
            print(f"[OPEN] {port:5} | {banner[:60]}")
            open_ports.append((port, banner))

    except:
        # Porta fechada ou filtrada
        pass

    finally:
        s.close()

# =============================
# EXECUÇÃO
# =============================
threads = []

print(f"\n🔎 Escaneando {args.target} ({target})")
print(f"📡 Portas: {start_port}-{end_port}\n")

for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan, args=(port,))
    threads.append(t)
    t.start()

# Espera todas as threads terminarem
for t in threads:
    t.join()

# =============================
# RESULTADO FINAL
# =============================
end_time = time.time()
duration = end_time - start_time

print("\n📊 Resultado final:")
for port, banner in open_ports:
    first_line = banner.splitlines()[0]
    print(f"[OPEN] {port:5} | {first_line}")
    print(f"\n⏱️ Tempo total: {duration:.2f} segundos")

# =============================
# SALVAR EM ARQUIVO (opcional)
# =============================
if args.output:
    with open(args.output, "w", encoding="utf-8") as f:
        for port, banner in open_ports:
            f.write(f"{port} - {banner}\n")

    print(f"\n💾 Resultado salvo em: {args.output}")