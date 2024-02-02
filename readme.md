### Orientações para rodar a aplicação - Linux

- Instale virtualenv

``` 
pip install virtualenv
```

- Crie e ative o ambiente virtual

```
virtualenv .env 
source .env/bin/activate
```

- Instale as dependências

```
pip install -r requirements.txt
```

- Rode a aplicação

```
python3 app.py
```

### Rodando a aplicação em produção

```
gunicorn -b 127.0.0.1:5000 app:app
```