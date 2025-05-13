# Auth Service - Hyper App

Microsserviço FastAPI que gerencia a autenticação e criação de usuários. 

---

## 🚀 Como configurar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/iancdesponds/hyper-app-auth.git
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux/macOS
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente

Copie o arquivo .env.example para .env e preencha com seus dados:

```bash
cp .env.example .env
```

### 5. Entre no diretório do app

```bash
cd .\app\
```

### 6. Rode o servidor localmente

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8010
```

Acesse a interface Swagger para testar:

```bash
http://localhost:8010/docs
```
