# Formulário de Entrada — YE | Jovens Empreendedores

Formulário em arquivo único (`index.html`). Não depende de internet, biblioteca externa
ou build. Abre em qualquer navegador, no celular ou no computador.

---

## O que ele faz

| | |
|---|---|
| **Abertura** | Animação de ~4,5s: o monograma YE é desenhado, o nome aparece e os quatro pilares surgem um a um. Tem botão **Pular**. |
| **Tela de boas-vindas** | Foto do grupo no topo (com fade para o fundo escuro) + descrição da comunidade + bloco **"Como funciona"** com 4 cartões (6 seções · ~7 min · progresso salvo · o que acontece depois). |
| **Preenchimento** | Uma seção por tela, com barra de progresso, contador `1/6` e nome da seção fixos no topo. |
| **Validação** | Mensagem específica por campo, rolagem automática até o primeiro erro. Nada de "preencha os campos obrigatórios" genérico. |
| **Rascunho** | Salva a cada tecla digitada. Se a pessoa fechar a aba, ao voltar o botão vira **"Retomar de onde parei"**. |
| **Envio** | Tela final com animação de confirmação e a assinatura do YE. |

Detalhes de usabilidade já embutidos:

- Telefone com máscara automática — a pessoa digita `11987654321`, vira `(11) 98765-4321`.
- Instagram aceita link colado (`instagram.com/fulano`) e converte para `@fulano`.
- Perguntas de texto longo mostram *"faltam X caracteres"* enquanto a resposta está curta demais.
- Campos condicionais: escolher **"Outro"** na pergunta 6 abre o campo de descrição; escolher
  **"Indicação de um participante"** na 17 pede o nome de quem indicou (obrigatório).
- `Enter` nos campos curtos avança para a próxima seção.
- Caixa de texto cresce sozinha conforme a pessoa escreve.
- Respeita `prefers-reduced-motion` (quem tem animações desligadas no sistema pula direto).

---

## Estado atual: modo de teste

O formulário **está funcionando, mas ainda não envia as respostas para lugar nenhum.**
Enquanto `CONFIG.endpoint` estiver vazio, as respostas ficam salvas só no navegador de quem
respondeu e aparece um botão para baixar o `.json` — útil para você testar, inútil em produção.

Escolha uma das duas opções abaixo antes de divulgar o link.

---

## Opção A — Google Sheets (recomendado, gratuito)

As respostas caem direto numa planilha sua.

**1.** Crie uma planilha nova no Google Sheets.

**2.** Menu **Extensões → Apps Script**. Apague o que estiver lá e cole o conteúdo de
`google-apps-script.gs` (está nesta pasta).

**3.** Clique em **Implantar → Nova implantação → Tipo: App da Web**, com:
- *Executar como:* **Eu**
- *Quem pode acessar:* **Qualquer pessoa**

**4.** Copie a URL gerada (termina em `/exec`).

**5.** Em `index.html`, procure o bloco `CONFIG` e cole a URL:

```js
const CONFIG = {
  endpoint: "https://script.google.com/macros/s/AKfy.../exec",
  storageKey: "ye_form_rascunho_v1"
};
```

Pronto. Cada envio vira uma linha na planilha, com cabeçalho criado automaticamente.

### Se der errado

Cole a URL `/exec` direto no navegador. Se aparecer **"YE — receptor ativo."**, está tudo
certo. Qualquer outra coisa indica problema:

| O que aparece | O que houve |
|---|---|
| `ReferenceError: ... (arquivo "Código")` | O arquivo `Código.gs` ainda tem outro código. Apague **todo** o conteúdo dele antes de colar o `google-apps-script.gs`. |
| Tela pedindo login | Na implantação, *Quem pode acessar* ficou como "Somente eu". Refaça com **Qualquer pessoa**. |
| Continua o erro antigo depois de corrigir | O Apps Script publica **versões**, não o código atual. Vá em **Implantar → Gerenciar implantações → ✏️ → Versão: Nova versão → Implantar**. A URL continua a mesma. |

> Detalhe importante: o Apps Script responde **HTTP 200 mesmo quando o script quebra** —
> devolve uma página de erro em vez de dados. O formulário confere o conteúdo da resposta,
> não só o código HTTP; se o script estiver quebrado, ele avisa a pessoa e preserva o
> rascunho em vez de mostrar "enviado" e perder a inscrição.

---

## Opção B — Formspree (mais rápido, plano gratuito limitado)

1. Crie um formulário em [formspree.io](https://formspree.io) e copie o endpoint
   (`https://formspree.io/f/xxxxxxx`).
2. Cole em `CONFIG.endpoint`.
3. Troque o `Content-Type` do envio: procure `"text/plain;charset=utf-8"` no arquivo e
   substitua por `"application/json"`.

---

## Onde hospedar

O projeto já está configurado para a **Vercel** — o passo a passo está em
[DEPLOY-VERCEL.md](DEPLOY-VERCEL.md).

> **Importante:** o envio para o Google Apps Script só funciona com o formulário hospedado
> (http/https). Aberto como `file://` o navegador bloqueia a requisição. Para testar
> localmente, use um servidor simples: `python -m http.server 5599` dentro da pasta,
> e acesse `http://localhost:5599`.

---

## Trocar a foto do topo

A foto está **embutida dentro do HTML** (base64), por isso o formulário continua sendo um
arquivo só — não existe imagem externa para subir junto nem para quebrar.

Para trocar por outra:

```bash
python trocar-foto.py "C:\caminho\da\nova-foto.jpg"
```

O script recorta em faixa, comprime e injeta a nova imagem no `index.html`.
Se os rostos ficarem cortados, ajuste onde ele corta na altura da foto — `0` é o topo,
`1` é a base:

```bash
python trocar-foto.py "C:\caminho\da\nova-foto.jpg" --foco 0.30
```

Fotos que já estão em formato horizontal são usadas sem recorte. A cópia recortada fica
salva como `foto-grupo.jpg` só para você conferir o resultado.

> Uma observação sobre a foto atual: além dos seis integrantes, aparecem ao fundo uma
> atendente e um cliente de outra mesa. Não atrapalha nada visualmente e é o tipo de coisa
> normal em foto de café — só vale você saber que estão ali, já que a página vai ser pública.

---

## Sistema visual

Tudo o que define a aparência está no bloco `:root`, no topo do arquivo — cores, tipografia,
espaçamentos e raios de canto são variáveis. Mudar uma linha ali muda a página inteira,
de forma consistente.

**Tipografia**

| | |
|---|---|
| Títulos | **Fraunces** — serifada variável, com eixos ópticos. Nos títulos grandes ela roda em `opsz 144` (contraste alto, ar editorial); nos textos pequenos em `opsz 20`, que engorda as hastes e mantém a legibilidade. |
| Texto e interface | **Inter** — desenhada para tela, com numerais tabulares no contador de seções. |

As duas vêm do Google Fonts. Se o visitante estiver sem conexão, o navegador cai para
Georgia + a fonte de sistema, e o layout continua íntegro.

Detalhes que fazem a diferença no acabamento: entrelinha apertada nos títulos (1.04) e
folgada no corpo (1.65); tracking negativo proporcional ao tamanho da fonte;
`text-wrap: balance` nos títulos, que impede a última linha órfã; `text-wrap: pretty`
nos parágrafos; e largura máxima de leitura de 36rem.

**Cor** — base preta com leve temperatura quente e um único destaque, o ouro `--gold: #CBA85F`.
Nada mais compete por atenção. Há um grão fino sobreposto à página inteira (`.atmos`) que
evita o aspecto "chapado" de fundo escuro puro.

**Outros detalhes**

- Progresso segmentado em 6 barras, uma por seção, em vez de uma barra contínua
- Numeração das perguntas suspensa na margem esquerda em telas ≥ 640px
- Perguntas entram em cascata (65ms de defasagem entre elas)
- Brilho que atravessa o botão principal ao passar o mouse
- Rolagem, seleção de texto e barra de rolagem com as cores do tema

---

## Personalizações rápidas

**Cores** — topo do arquivo, bloco `:root`. A cor de destaque é `--gold: #CBA85F`.

**Textos da abertura, boas-vindas e "Como funciona"** — estão em HTML puro, procure por
`<div id="intro">` e `id="screen-welcome"`.

**Perguntas** — todas ficam no array `SECTIONS` dentro do `<script>`. Cada pergunta é um objeto:

```js
{ n:7, name:"empresa", type:"text", label:"Qual é o nome da empresa...?",
  required:true, placeholder:"Nome da empresa ou projeto" }
```

- `type`: `"text"`, `"number"`, `"tel"`, `"textarea"` ou `"radio"`
- `required`: `true` / `false`
- `help`: texto de apoio abaixo da pergunta
- `min` / `max`: em `textarea`, mínimo e máximo de caracteres
- `followup`: campo extra que aparece só quando certas opções são escolhidas

Para adicionar uma pergunta, basta incluir um objeto novo na seção desejada — o formulário
se redesenha sozinho, incluindo validação, contador e salvamento.

**Tempo da animação de abertura** — a linha `setTimeout(closeIntro, reduced ? 400 : 4500);`
controla a duração. Os atrasos de cada elemento estão no CSS (`animation-delay`).

---

## Arquivos desta pasta

```
index.html               o formulário completo, foto inclusa
og.jpg                   imagem da prévia do link (WhatsApp, Instagram)
robots.txt               libera a indexação no Google
vercel.json              cabeçalhos de segurança e cache
.vercelignore            mantém os arquivos de trabalho fora do servidor

DEPLOY-VERCEL.md         como publicar
LEIA-ME.md               este arquivo
google-apps-script.gs    código para colar no Apps Script da planilha
trocar-foto.py           troca a foto do topo (atualiza index.html e og.jpg)
definir-dominio.py       grava o domínio nas meta tags de compartilhamento
foto-grupo.jpg           cópia recortada da foto atual (só para conferência)
.claude/launch.json      config para rodar o servidor local de teste
```
