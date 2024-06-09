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

# Fluxo de criação dos anais
- **Etapa 1)** Criar evento;
- **Etapa 2)** Cadastrar trabalhos:
  - **Entrada**: Arquivo CSV 
    - O arquivo CSV deve possuir as colunas id, titulo, autores, area, ignorar;
  - **Saída**: Trabalhos pré-cadastrados (falta o preenchimento da quantidade de páginas);
- **Etapa 3)** Processar PDFs referentes aos trabalhos:
  - **Entrada**: Arquivo ZIP 
    - Cada arquivo PDF dentro do zip deve ser nomeado com o id do trabalho presente no CSV;
  - **Saída**: Finalização do cadastro de trabalhos e arquivo PDF com todos os trabalhos agrupados;
- **Etapa 4)** Gerar sumário:
  - **Saída**: Arquivo PDF referente ao sumário;
- **Etapa 5)** Gerar os anais:
  - **Entrada**: Arquivo PDF referente a capa;
  - **Saída**: Arquivo PDF referente ao anal (Capa + sumário + artigos agrupados);

# Fluxo de envio dos certificados
- **Etapa 1)** Cadastro dos inscritos:
  - **Entrada**: Arquivo CSV
    - O arquivo CSV deve possuir as colunas cpf, email;
- **Etapa 2)** Cadastro dos ouvintes:
  - Ouvintes são inscritos que participaram das atividades dos eventos;
  - **Entrada**: Arquivo CSV
    - O arquivo CSV deve possuir as colunas nome, email, ch;
- **Etapa 3)**: Envio dos certificados;
  - Envio dos certificados para os ouvintes;