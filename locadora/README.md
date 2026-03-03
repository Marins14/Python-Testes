# Projeto básico para conexão com um banco de dados PostgreSQL via Python

## Passo a Passo para deixar funcionando a aplicação

1. Na pasta raiz do projeto rodar: 
```bash
docker compose up -d
```

2. Preparando o venv
```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

3. Rodando o script
```bash
python3 app/main.py
```