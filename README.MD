# Execução local do projeto

* Caso não possua um ambiente virtual, crie:
  * python -m venv venv
  * venv\Scripts\activate **(Windows)**
  * source venv/bin/activate **(MacOs/Linux)**
* Se ainda não possuir as dependências do projeto instaladas, execute:
  * pip install -r requirements-dev.txt
  * pip-compile requirements.in
* Crie um arquivo .env na raíz do projeto, e adicione as variáveis de ambiente de acordo com o .env.example
* Na pasta raíz do projeto:
  * uvicorn api.app:app --reload
* Acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) **(Swagger do projeto)**