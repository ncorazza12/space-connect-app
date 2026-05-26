# 🚀 SPACE CONNECT — CI/CD Pipeline

![Status](https://img.shields.io/badge/status-ONLINE-brightgreen)
![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue)

Projeto desenvolvido para a **Global Solution – DevOps & CI/CD** da FIAP.

## 📡 Sobre o Projeto

A **SPACE CONNECT** é uma aplicação de monitoramento de sistemas espaciais com pipeline CI/CD automatizada via Jenkins, Docker e GitHub.

## 🗂️ Estrutura

space-connect-app/
├── app.py                  # Aplicação Flask
├── requirements.txt        # Dependências Python
├── Dockerfile              # Container da aplicação
├── Jenkinsfile             # Pipeline CI/CD declarativa
├── jenkins/
│   ├── Dockerfile          # Imagem Jenkins com Docker CLI
│   └── docker-compose.yml  # Orquestração do Jenkins
├── evidencias/             # Prints das etapas
└── README.md

## ⚙️ Endpoints

| Endpoint  | Descrição              |
|-----------|------------------------|
| `GET /`   | Status da missão       |
| `GET /health` | Health check       |

**Resposta exemplo:**
```json
{
  "mission": "SPACE CONNECT",
  "version": "1.0",
  "status": "ONLINE",
  "timestamp": "2026-05-25T23:00:00+00:00"
}
```

## 🐳 Executar localmente

```bash
docker build -t space-connect-app:latest .
docker run -d --name space-connect -p 5000:5000 space-connect-app:latest
curl http://localhost:5000/health
```

## 🔁 Pipeline Jenkins

A pipeline possui 3 estágios:

1. **Build** — Constrói a imagem Docker
2. **Test** — Valida os endpoints com `curl`
3. **Deploy Simulado** — Executa o container em produção

### Subir o Jenkins

```bash
cd jenkins/
docker compose up -d --build
```

Acesse: `http://localhost:8080`

## 👥 Integrantes

| Nome                 | RM       |
|----------------------|----------|
| Nickolas Corazza     | RM562265 |
| Dorivaldo Nascimento | RM565225 |
| Gabriel Lamata       | RM562093 |
| Luiz Parpinelli      | RM566493 |

## 🐛 Troubleshooting — Port is already allocated

Erro: Error response from daemon: driver failed programming external connectivity on endpoint [...]: Bind for 0.0.0.0:5001 failed: port is already allocated

O que significa: O Docker tentou mapear uma porta do host (ex: 5001) para o container, mas essa porta já está sendo usada por outro processo ou container no sistema operacional. O Docker Daemon não consegue fazer dois bindings simultâneos na mesma porta.

Como identificar a causa:

# Ver qual container está usando a porta
docker ps --format "table {{.Names}}\t{{.Ports}}" | grep 5001

# Ou no Linux/WSL, ver qual processo usa a porta
sudo ss -tulnp | grep :5001

Como resolver:

# Opção 1: Parar o container que ocupa a porta
docker stop space-connect-deploy
docker rm space-connect-deploy

# Opção 2: Usar uma porta diferente no docker run
docker run -d --name space-connect-deploy -p 5003:5000 space-connect-app:latest

No contexto do nosso Jenkinsfile, o stage "Deploy Simulado" já trata esse erro preventivamente com:

docker stop ${CONTAINER_NAME} 2>/dev/null || true
docker rm   ${CONTAINER_NAME} 2>/dev/null || true

Isso para e remove qualquer container anterior antes de subir o novo, evitando o conflito de porta.
Como evitar futuramente:

1. Sempre remover containers antigos antes de criar novos (como feito no Jenkinsfile)
2. Usar variáveis de ambiente para as portas, facilitando mudanças
3. Adotar orquestradores como Docker Compose ou Kubernetes que gerenciam esse ciclo de vida automaticamente
4. Implementar health checks no pipeline para validar se a porta está livre antes do deploy

## 🤖 Uso de IA durante a atividade

Como utilizamos IA durante a atividade: Utilizamos o Claude (Anthropic) como assistente técnico durante toda a atividade, especialmente para estruturar os arquivos do projeto e entender as configurações do Jenkins.

Prompts utilizados:

- "Me ajude a criar uma aplicação Flask com endpoints / e /health para uma missão DevOps chamada SPACE CONNECT"
- "Como configurar Jenkins rodando em Docker para executar comandos Docker via socket?"
- "Crie um Jenkinsfile com 3 stages: Build, Test e Deploy simulado"
- "Explique o erro 'port is already allocated' e como resolver no contexto de um pipeline CI/CD"

O que foi aproveitado diretamente: A estrutura base dos arquivos app.py, Dockerfile, Jenkinsfile e a lógica de stop/remove do container antes do deploy.

O que precisou ser ajustado manualmente:

- Adaptamos o host.docker.internal para funcionar especificamente com o Docker Desktop no Windows
- Ajustamos as portas usadas nos stages para não conflitar com o teste manual
- Preenchemos os dados do grupo no README.md

Como validamos as respostas geradas: Executamos cada comando no terminal e verificamos a saída real. O pipeline foi executado passo a passo e cada stage foi validado pelo Console Output do Jenkins. Não aceitamos nenhuma resposta sem executar e confirmar o funcionamento real.