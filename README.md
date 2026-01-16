# Projeto Invoice Automation (Python 3.13)

Este projeto é uma automação em Python para processar **invoices (faturas) em PDF**, extrair informações principais, salvar os dados em um arquivo JSON local e gerar análises com **pandas**.

Os PDFs utilizados como exemplo foram obtidos no dataset público do Kaggle:  
https://www.kaggle.com/datasets/ayoubcherguelaine/company-documents-dataset

---

## O que este projeto faz

### 1) Ingestão (leitura e extração de dados dos PDFs)
O sistema lê todos os arquivos PDF de uma pasta indicada e extrai:

- **Order ID**
- **Order Date**
- **Customer ID**
- **Itens da fatura**, contendo:
  - Produto
  - Quantidade
  - Preço Unitário

### 2) Armazenamento local
Após extrair e validar os dados, o projeto salva tudo em um arquivo chamado:

- **database.json**

### 3) Validação com Pydantic
Antes de gravar no JSON, os dados são validados para garantir consistência e integridade.

### 4) Analytics com pandas
O sistema realiza análises em cima do `database.json` e retorna:

- Média do valor total das faturas
- Produto mais frequente
- Total gasto por produto
- Lista de produtos com preço unitário

---

## Requisitos

- **Python 3.13**
- Dependências instaladas via `requirements.txt`

Bibliotecas principais utilizadas:
- `pdfplumber` (leitura de PDF)
- `pydantic` (validação)
- `pandas` (análises)

---

## Como instalar

1) Clone o repositório e entre na pasta do projeto:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd projeto-invoice
```

2) Crie e ative um ambiente virtual (recomendado): 
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3) Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como preparar os PDFs de exemplo (Kaggle)

Este projeto foi testado usando invoices do dataset público do Kaggle:  
https://www.kaggle.com/datasets/ayoubcherguelaine/company-documents-dataset

Passos sugeridos para obter os PDFs:

1) Acesse o link do dataset  
2) Vá em **Data Explorer**  
3) Selecione a pasta **Invoices**  
4) Baixe alguns arquivos PDF (ex: `invoice_10248.pdf`, `invoice_10249.pdf`...)  
5) Coloque os PDFs dentro da pasta:

```bash
data/invoices/
```
---

## Como executar

O projeto possui dois comandos principais:

### 1) Rodar a ingestão (ler PDFs e gerar o `database.json`)

Comando:
python main.py ingest

O que acontece ao executar:
- o sistema lê todos os PDFs da pasta `data/invoices/`
- extrai os dados da fatura e dos itens (produto, quantidade e preço unitário)
- valida os dados com **Pydantic**
- cria ou atualiza o arquivo `database.json`
- impede duplicidade: se um **Order ID** já existir no JSON, ele não será gravado novamente

### 2) Rodar as análises (analytics)

Comando:
python main.py analytics

O que acontece ao executar:
- o sistema lê o arquivo `database.json`
- calcula métricas com **pandas**
- retorna os resultados no terminal em formato **JSON**

---

## Fluxo recomendado de uso
  1) `python main.py ingest`  
  2) `python main.py analytics`
