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
| Luiz Parpinelli      | RM566493 |# trigger test
