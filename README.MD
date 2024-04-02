# Execução local do projeto

* Caso não possua um ambiente virtual, crie:
  * python -m venv venv;
  * venv\Scripts\activate **(Windows)**;
  * source venv/bin/activate **(MacOs/Linux)**;
* Se ainda não possuir as dependências do projeto instaladas, execute:
  * pip install -r requirements-dev.txt;
  * pip-compile requirements.in;
  * pip install -r requirements.txt;
* Instalar o [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) e definir como variável de ambiente no sistema;
* Crie um arquivo .env na raíz do projeto, e adicione as variáveis de ambiente de acordo com o .env.example;
* Na pasta raíz do projeto:
  * uvicorn api.app:app --reload;
* Acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) **(Swagger do projeto)**;

# Fluxo de criação do anal
- **Etapa 1)** Criar evento;
- **Etapa 2)** Cadastrar papers:
  - **Entrada**: Arquivo CSV;
  - **Saída**: Papers pré-cadastrados (falta o preenchimento da quantidade de páginas);
- **Etapa 3)** Processar PDFs referentes aos papers:
  - **Entrada**: Arquivo ZIP;
  - **Saída**: Finalização do cadastro de papers e arquivo PDF com todos os trabalhos agrupados;
- **Etapa 4)** Gerar sumário:
  - **Saída**: Arquivo PDF referente ao sumário;
- **Etapa 5)** Gerar o anal:
  - **Entrada**: Arquivo PDF referente a capa;
  - **Saída**: Arquivo PDF referente ao anal (Capa + sumário + artigos agrupados);