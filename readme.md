# LLM-ConvoBotAI

Este é um projeto de chatbot AI que utiliza modelos locais de linguagem (LLM) para conversas contínuas, mantendo o contexto da sessão. Ou seja, durante uma conversa, o chatbot consegue "lembrar" das interações anteriores, permitindo uma experiência mais fluida e natural. O chatbot pode ser executado em ambientes Windows com suporte ao modelo manual (Phi-3), além de oferecer a possibilidade de usar o **Ollama** como backend local em qualquer sistema operacional. Também é possível integrar com a **Hugging Face** para usar modelos pré-treinados disponíveis na plataforma.

Diferente do projeto [AI-chatbot](https://github.com/Abiscula/AI-chatbot) que implementei com o Groq, este oferece uma maior flexibilidade na escolha do modelo de linguagem, permitindo ao usuário selecionar entre uma ampla variedade de modelos, como o GPT-3 ou Phi-3, conforme suas necessidades. O suporte a diferentes provedores, como o Ollama e Hugging Face, permite que o chatbot seja executado em diversos sistemas, com a possibilidade de escolher entre uma solução local (para Windows) ou via API. Isso dá aos usuários mais controle sobre o modelo que estão utilizando e como o chatbot é configurado, sem a necessidade de depender de uma solução única. Além disso, o LLM-ConvoBotAI foi otimizado para uma experiência mais fluida, com um sistema de manutenção de contexto robusto e sem limitações de infraestrutura, o que não era possível com a solução anterior baseada no Groq.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Ollama**: Plataforma para executar LLMs localmente.
- **Phi-3 (quantized)**: Modelo de linguagem para ser carregado manualmente.
- **Streamlit**: Framework para criar a interface interativa do chatbot.
- **LangChain**: Biblioteca usada para integrar LLMs e orquestrar conversas.
- **Hugging Face**: Para usar modelos pré-treinados via API.

## Como Rodar o Projeto

### 1. Pré-requisitos

- **Python 3.8+**
- **Pip** para instalar as dependências
- **Ollama**: Caso deseje utilizar o Ollama como backend para o modelo local
- **Hugging Face API Key**: Caso deseje usar modelos da Hugging Face

### 2. Configurando o Ambiente

#### 1. Clone este repositório para o seu ambiente local:

```bash
git clone <URL_DO_REPOSITORIO>
cd <DIRETORIO_DO_REPOSITORIO>
```

#### 2. Crie um ambiente virtual:

```bash
 python3 -m venv venv
 source venv/bin/activate  # Para Linux/MacOS
 venv\Scripts\activate     # Para Windows
```

#### 3. Instale as dependências do projeto:

```bash
 pip install -r requirements.txt
```

#### 4. Configure a Hugging Face API Key:

Para usar modelos da Hugging Face, você precisa configurar a chave da API. Crie um arquivo .env no diretório raiz do projeto e adicione a seguinte linha:

```bash
 HF_API_KEY=seu_token_da_hugging_face
```

Substitua seu_token_da_hugging_face pelo seu token da API da Hugging Face, que pode ser obtido em Hugging Face - API.

### 3. Rodando o Modelo

#### Opção 1: Usando Ollama

Para usar o Ollama, você precisará instalar o aplicativo Ollama localmente.

    1.	Instale o Ollama:
    •	Para Windows: Faça o download e instale o Ollama a partir do site oficial do Ollama.
    •	Para MacOS e Linux: Utilize o Homebrew para instalar o Ollama:

```bash
 brew install ollama
```

    2.	Inicie o servidor Ollama:

Execute o seguinte comando para iniciar o servidor Ollama em sua máquina:

```bash
 ollama serve
```

#### Opção 2: Usando o Modelo Manual (para Windows)

Caso esteja em um dispositivo Windows ou não queira usar o Ollama, você pode optar pelo modelo manual (Phi-3).

1. Baixe o modelo Phi-3 quantizado:
   • Baixe o modelo manualmente e coloque-o em um diretório específico dentro do seu projeto.
2. Rodando o chatbot com Phi-3:
   O modelo será carregado manualmente a partir do diretório onde você o colocou.
3. Iniciar o chatbot:
   Quando você executar o código, o modelo manual será utilizado no lugar do Ollama.

#### Opção 3: Usando Hugging Face

Se você preferir usar um modelo pré-treinado da Hugging Face, você pode configurar o projeto para se conectar à API da Hugging Face.

1. Certifique-se de que o arquivo .env está configurado com a sua API Key (conforme a etapa 4 do item anterior).
2. Escolha um modelo na Hugging Face:
   Vá até Hugging Face Models e escolha um modelo de sua preferência.
3. Execute o chatbot:
   Com a API configurada, basta rodar o chatbot com o modelo desejado. O código irá automaticamente se conectar à Hugging Face para carregar o modelo e utilizá-lo para gerar as respostas.

### 4. Restrição do Modelo Local no Windows

• Ollama funciona em qualquer sistema operacional (Windows, MacOS, Linux).
• Modelo manual (Phi-3) tem suporte específico para dispositivos Windows, devido à necessidade de carregar modelos quantizados manualmente.
• Hugging Face pode ser usado em qualquer sistema operacional, desde que a API Key esteja configurada corretamente.
