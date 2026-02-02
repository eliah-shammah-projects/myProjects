# Tanakh Verse Classifier

Este projeto cria um modelo de Machine Learning para classificar versos hebraicos da Tanakh em Torah, Nevi'im ou Ketuvim.

## Instalação

1. Crie um ambiente virtual: `python -m venv .venv`
2. Ative o ambiente: `.venv\Scripts\activate` (Windows)
3. Instale dependências: `pip install -r requirements.txt`

## Uso

1. **Buscar dados**: Execute `python data_fetch.py` para baixar versos da API Sefaria e salvar em `verses_data.json`. (Pode demorar devido ao volume de dados.)

2. **Treinar modelo**: Execute `python train_model.py` para pré-processar, treinar e salvar o modelo em `classification_model.pkl` e vetorizador em `tfidf_vectorizer.pkl`.

3. **Rodar backend (Flask)**: Execute `python app.py` para iniciar o servidor Flask em http://127.0.0.1:5000/. (Para API de predições.)

4. **Rodar front-end (React)**: Navegue para a pasta `front/`, instale dependências com `npm install`, depois `npm run dev` para iniciar em http://localhost:5173/.

5. **Testar**: No front-end React, insira um verso hebraico e veja a predição. (Atualmente usa dados mock; para conectar ao backend, edite `App.jsx` para fazer fetch para o Flask.)

## Estrutura

- `data_fetch.py`: Busca dados da API.
- `preprocess.py`: Limpa e vetoriza texto.
- `train_model.py`: Treina o modelo.
- `predict.py`: Função de predição.
- `app.py`: Backend Flask.
- `templates/index.html`: Front-end simples (Flask).
- `front/`: Front-end React moderno.
- `requirements.txt`: Dependências Python.

## Troubleshooting

- Erro de rede: Verifique conexão com internet para API Sefaria.
- Pacotes faltando: Execute `pip install -r requirements.txt`.
- Modelo não encontrado: Execute `train_model.py` primeiro.
- Porta ocupada: Mude a porta em `app.run(port=5001)`.
- Front-end: Instale Node.js se necessário para `npm`.