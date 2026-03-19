# 🔎 Port Scanner

Ferramenta leve em Python para varredura de portas TCP, com suporte a multithreading e banner grabbing para identificação de serviços.

---

## 🚀 Funcionalidades

* Varredura de portas TCP
* Multithreading (execução rápida)
* Suporte a IP e domínio
* Identificação básica de serviços
* Banner grabbing (detecção de versão/tecnologia)
* Exportação de resultados para arquivo

---

## 💻 Uso

```bash
python scanner.py -t <alvo> -p <portas> -o <arquivo>
```

### Exemplo

```bash
python scanner.py -t scanme.nmap.org -p 20-80 -o resultado.txt
```

---

## 📊 Resultado

![result](assets/results.png)

---

## 🧰 Tecnologias

* Python 3
* Socket
* Threading

---

## ⚠️ Aviso

Este projeto foi desenvolvido para fins educacionais.
Não utilize em sistemas sem autorização.
