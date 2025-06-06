# ProjetoDW Iris

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Ambiente virtual

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/Pereira-Sah/ProjetoDW.git
   cd ProjetoDW
   ```

2. **Crie e ative um ambiente virtual:**

   ```bash
   python -m venv ambienteVirtual
   # No Windows:
   ambienteVirtual\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações do banco de dados:**

   ```bash
   python manage.py migrate
   ```

5. **(Opcional) Crie um superusuário para acessar o admin:**

   ```bash
   python manage.py createsuperuser
   ```

## Execução

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

Acesse o projeto no navegador através de `http://127.0.0.1:8000/`.

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [SQLite](https://www.sqlite.org/index.html)
- HTML, CSS
