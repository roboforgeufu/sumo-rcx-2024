# sumo-rcx-2024

Códigos e materiais da programação para os robôs da categoria de Sumô LEGO da Robocore Experience 2024, da equipe Roboforge.

- **Regras**: As regras do desafio estão no arquivo `/regras.pdf`, na pasta raiz do repositório.
- **Rascunhos**: A pasta `/drafts` contém arquivos, materiais e códigos referentes a testes, rascunhos e algoritmos implementados em fase de validação de cada robô.
- **Código Fonte**: o projeto a ser transferido e executado por cada robô está na pasta `/src`.
  - A pasta `/src/core` contém código útil a ambos os robôs.
  - As outras sub-pastas contém códigos específicos a cada um dos robôs.

## Configurações do Projeto

### Extensão EV3

Para enviar apenas as pastas desejadas pro EV3, utilizamos as configurações da extensão do VSCode ev3dev-browser. A configuração acontece no arquivo `./.vscode/settings.json`.

O conteúdo da opção `ev3devBrowser.download.include` é um padrão _glob_ incluindo a lista de _wildcards_ dos arquivos a serem incluidos no download pro brick.

No exemplo, enviando todos os arquivos da pasta `src` e da pasta `drafts`:

```json
{
  "ev3devBrowser.download.include": "{src/**,drafts/**}"
}
```
