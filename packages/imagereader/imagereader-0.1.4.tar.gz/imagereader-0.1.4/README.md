# AnalistaDeImagem 📸  
Biblioteca Python para análise de imagens usando a API da OpenAI (Vision).  
Transforme imagens em texto descritivo de forma simples e rápida.  

---

## 🚀 Funcionalidades  
- Codificação de imagens em Base64.  
- Integração com o modelo GPT-4 Vision para descrever imagens.  
- Fácil de usar e configurar.  

---

## 🛠️ Instalação  

Você pode instalar a biblioteca diretamente via pip:  

```bash
pip install imagereader


🎯 Uso Rápido

from image_reader import Reader_image

# Inicializar o leitor
reader = Reader_image(
    imagem="caminho/da/imagem.jpg",
    modeloLLM="gpt-4o-mini",
    chaveAPI="sua-chave-api"
)

# Analisar imagem
descricao = reader.read_image()
print(descricao)


🛠️ Requisitos

Python 3.8+
OpenAI API Key
Dependências listadas em requirements.txt

📝 Licença
MIT License - veja LICENSE para mais detalhes.