# Execução local do projeto

* Caso não possua um ambiente virtual, crie:
  * python -m venv venv
  * venv\Scripts\activate **(Windows)**
  * source venv/bin/activate **(MacOs/Linux)**
* Se ainda não possuir as dependências do projeto instaladas, execute:
  * pip install -r requirements-dev.txt
  * pip-compile requirements.in
  * pip install -r requirements.txt
* Crie um arquivo .env na raíz do projeto, e adicione as variáveis de ambiente de acordo com o .env.example
* Na pasta raíz do projeto:
  * uvicorn api.app:app --reload
* Acesse [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) **(Swagger do projeto)**

# Fluxo de criação do anal
- Criar evento
- Criar o PDF com todos os trabalhos juntos (fluxo "merged_papers")
  - Entrada: Arquivo ZIP
  - Durante esta etapa, é feito um pré cadastro dos trabalhos ("papers") com as informações sobre o id do trabalho e o total de páginas
  - Saída: Arquivo PDF com todos os trabalhos agrupados
- Preencher todos os papers pré-cadastrados com o restante das informações (fluxo "batch_update_papers")
  - Entrada: Arquivo CSV
  - Durante esta etapa, o arquivo CSV é percorrido e em cada linha é obtido o campo id que é usado para buscar o trabalho no banco e atualizá-lo com o restante das informações.
- Gerar sumário (fluxo "summary")
  - Por meio dos trabalhos totalmente cadastrados é criado o sumário.
  - Saída: Arquivo PDF
- Gerar o anal (fluxo não definido na aplicação)
  - Entrada: Arquivo PDF
  - Realizar a junção de todos os arquivos PDF gerados até o momento.
  - Saída: Arquivo PDF