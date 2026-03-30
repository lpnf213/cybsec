# 🛡️ Iptables & Network Management Module

Este módulo centraliza a interação do toolkit com o subsistema de rede do kernel Linux (`netfilter`). É o "cérebro" que configura como os pacotes devem fluir durante um ataque ou auditoria.

---

## 🏗️ Anatomia do Iptables (Guia Profundo)

O `iptables` funciona como um pipeline de decisão por onde cada pacote de rede tem de passar.

### 🏷️ 1. As Tabelas (Tables)
*   **Filter:** A tabela padrão para segurança. Controla quem entra e quem sai.
*   **NAT (Network Address Translation):** Usada para alterar o IP ou o Porto de origem/destino. Essencial para redirecionar tráfego para um Proxy.
*   **Mangle:** Usada para "esquartejar" e alterar campos específicos do cabeçalho IP/TCP (ex: TTL, MSS, Type of Service).

### ⛓️ 2. As Correntes (Chains)
*   **PREROUTING:** Antes de o Kernel decidir para onde vai o pacote. Ótimo para redirecionar tráfego que vem de fora.
*   **INPUT:** Para pacotes que o destino final é o "Localhost" (o teu Kali).
*   **FORWARD:** Para pacotes que o teu computador está apenas a transportar (MIM).
*   **POSTROUTING:** O último passo. Usado para "Masquerading" (esconder o IP de origem) ou ajuste de MSS.

---

## ⚙️ 3. Comandos e Flags Cruciais

### Estrutura:
`sudo iptables -t [tabela] -[A/D/I/C] [Chain] [Filtros] -j [Target]`

| Flag | Nome | Função |
| :--- | :--- | :--- |
| `-A` | Append | Adiciona a regra ao fim da lista (executada por último). |
| `-I` | Insert | Insere no topo da lista (executada primeiro - alta prioridade). |
| `-D` | Delete | Remove uma regra específica. |
| `-C` | Check | Verifica se a regra já existe (evita duplicados). |
| `-L -v -n` | List | Lista as regras com contadores e sem resolver DNS (mais rápido). |

### Filtros Comuns:
*   `-p [tcp/udp/icmp]`: Filtra pelo protocolo.
*   `--dport [porto]`: Filtra pelo porto de destino (ex: 80, 443).
*   `-s [IP] / -d [IP]`: Filtra pela origem (Source) ou destino (Destination).
*   `-i [interface]`: Filtra pela interface de entrada (ex: `eth0`).

### Alvos (Targets):
*   `ACCEPT`: Deixa o pacote passar.
*   `DROP`: Ignora o pacote silenciosamente (o emissor pensa que houve timeout).
*   `REJECT`: Bloqueia e envia um erro de volta (mais educado, mas revela que há um firewall).
*   `REDIRECT`: Desvia o pacote para um porto local.
*   `LOG`: Não bloqueia, apenas escreve no log do kernel (`dmesg`).

---

## 🧪 4. Casos de Uso em Cibersegurança

### A. Redirecionamento Transparente (SSL Strip / Intercepção)
`sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080`
*Isso força todo o tráfego HTTP da vítima a passar pelo teu servidor proxy (ex: mitmproxy) sem ela saber.*

### B. Otimização de MTU (O que o nosso código faz)
`sudo iptables -t mangle -A POSTROUTING -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu`
*Ajusta o tamanho dos segmentos TCP para garantir que pacotes grandes (como do GitHub) não sejam descartados durante o "hop" extra do ataque MIM.*

### C. Bloqueio de Descoberta (Anonymity)
`sudo iptables -A INPUT -p icmp --icmp-type echo-request -j DROP`
*Faz com que o teu Kali deixe de responder a Pings, tornando-o "invisível" a scanners de rede simples.*

---

## ⚠️ 5. Nota sobre Persistência
Lembre-te: Por segurança, o Linux **apaga todas as regras** quando reinicias. O nosso módulo Python garante que as regras necessárias são re-aplicadas sempre que inicias uma operação no toolkit.
