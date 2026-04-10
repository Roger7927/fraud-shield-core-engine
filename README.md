# FraudShield Core Engine 🛡️

**API de alta performance para detecção de fraudes comportamentais, construída com FastAPI, Docker e SQLAlchemy.**

## 🏛️ Propriedade Intelectual
- **Autor:** Guillermo Roger Hernandez Chandia
- **Status:** Todos os Direitos Reservados
- **Contexto:** Projeto Acadêmico - Análise e Desenvolvimento de Sistemas (ADS)

## 🚀 Diferenciais Técnicos
- **FastAPI:** Framework assíncrono de alto desempenho.
- **Score Comportamental:** Lógica que detecta anomalias baseadas em frequência e valor.
- **Segurança:** Proteção via API Key e Variáveis de Ambiente.
- **Dockerizado:** Pronto para deploy em qualquer infraestrutura.

## 🛠️ Como Executar (Docker)
```bash
docker build -t fraud-shield-core .
docker run -p 8000:8000 --env-file .env fraud-shield-core
