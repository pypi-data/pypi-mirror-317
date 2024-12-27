Extraia histórias do Wattpad com facilidade! Com este pacote, você pode buscar histórias, baixá-las diretamente e até convertê-las para formatos de eBook como EPUB e PDF (em desenvolvimento).

Importante: Este é um código baseado em no código oficial do Ayobamidele, pois como não havia uma biblioteca hospedada, eu resolvi hospedar. 
- [GitHub do Projeto original](https://github.com/Ayobamidele/wattpad-scraper)

## Funcionalidades Principais
- Pesquisar histórias no Wattpad.
- Baixar histórias utilizando a URL.
- Converter histórias para o formato EPUB.
- Login para acessar conteúdos exclusivos.

### Links Importantes
- [GitHub do Projeto](https://github.com/josyelbuenos/jb-wattpad-scraper)

## Instalação

Para instalar o pacote, basta usar o comando abaixo no terminal:

```bash
pip install jb-wattpad-scraper
```

## Como Usar

### Baixar História por URL
```python
from wattpad_scraper import Wattpad

wattpad = Wattpad()
url_historia = "https://www.wattpad.com/story/162756571-bending-the-rules-the-rules-1"
historia = wattpad.get_book_by_url(url_historia)

print(historia.title)  # Título da história
print(historia.author.name, historia.author.url)  # Autor e link do perfil
print(historia.description)  # Descrição
print(historia.chapters[0].title, historia.chapters[0].content)  # Primeiro capítulo e conteúdo
```

### Pesquisar Histórias
```python
from wattpad_scraper import Wattpad

wattpad = Wattpad()
resultados = wattpad.search_books('romance histórico', completed=True, mature=True, free=True, paid=False, limit=5)

for historia in resultados:
    print(historia.title)  # Exibe os títulos encontrados
```

### Converter História para EPUB
```python
from wattpad_scraper import Wattpad

wattpad = Wattpad()
historia = wattpad.search_books('fantasia mágica')[0]
historia.convert_to_epub()  # Converte e salva no diretório atual
```

### Autenticação (Beta)
```python
from wattpad_scraper import Wattpad

wattpad = Wattpad("seu_usuario", "sua_senha")
historia = wattpad.search_books("aventura épica")[0]
print(historia.chapters[2].content)  # Conteúdo do terceiro capítulo
```

#### Usando Arquivo de Cookies
1. Instale a extensão "Cookie - Editor" no navegador.
2. Exporte os cookies e salve como um arquivo `.json`.
3. Utilize no código conforme o exemplo abaixo:

```python
from wattpad_scraper import Wattpad

wattpad = Wattpad(cookie_file='/caminho/para/cookies.json')
resultados = wattpad.search_books("histórias exclusivas")
```

## Contribua
Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

---

Desenvolvido com 💖 para todos os fãs de leitura.
