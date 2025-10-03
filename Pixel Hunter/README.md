A partir do código Python fornecido, segue um modelo de arquivo **README.md** que você pode usar para o seu projeto. Este README inclui uma descrição clara, instruções de uso e instalação, e informações sobre as tecnologias utilizadas.

-----

# 🎯 Pixel Hunter - Caçador de Pixels

Uma ferramenta simples e poderosa para desenvolvedores e entusiastas de automação, permitindo a **captura de coordenadas e cores de pixels** na tela com um **zoom em tempo real**. Ideal para scripts que interagem com jogos ou outras aplicações que não têm uma API para automação.

## ✨ Funcionalidades

  * **Visualização com Zoom:** Uma janela flutuante com zoom 10x (200x200 pixels ampliados a partir de uma área 20x20) que segue o seu mouse, permitindo ver os pixels com precisão.
  * **Informações em Tempo Real:** Exibe as coordenadas absolutas (da tela) e relativas (da janela), além do código de cor em **HEX**, **RGB** e o formato **ColorRef** (ótimo para uso com a biblioteca `pywin32`).
  * **Captura Rápida:** Pressione a tecla `` ` `` (crase) para imprimir todas as informações do pixel atual diretamente no terminal, facilitando a cópia e uso em seu código.
  * **Janela no Topo:** A janela do Pixel Hunter se mantém sempre no topo das outras aplicações, garantindo que você não a perca de vista.

## ⚙️ Instalação

O Pixel Hunter é compatível com **Windows**. Para usá-lo, você precisa ter o Python instalado.

1.  **Clone o repositório ou baixe o arquivo:**

    ```bash
    git clone https://github.com/seu-usuario/pixel-hunter.git
    cd pixel-hunter
    ```

    (Substitua o link pelo do seu repositório).

2.  **Instale as dependências necessárias:**

    ```bash
    pip install pillow keyboard pywin32
    ```

## 🚀 Como Usar

1.  **Execute o script:**

    ```bash
    python pixel_hunter.py
    ```

2.  Uma janela flutuante será exibida e um prompt de comando com instruções aparecerá.

3.  **Mova o mouse** sobre a área da tela que você deseja inspecionar. A janela do Pixel Hunter irá mostrar uma versão ampliada da área sob o cursor.

4.  Quando encontrar o pixel desejado, pressione a tecla **`` ` `` (crase)**. As coordenadas e a cor serão impressas no terminal.

5.  Para sair da ferramenta, pressione a tecla **`ESC`**.

## 🤝 Contribuição

Contribuições são bem-vindas\! Se você encontrou um bug ou tem uma ideia de melhoria, sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.
