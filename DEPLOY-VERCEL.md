# Subir o formulário na Vercel

O projeto já está configurado. São três etapas: publicar, gravar o domínio nas meta tags
e ligar o destino das respostas.

---

## Antes de começar

Crie uma conta gratuita em [vercel.com](https://vercel.com) (dá para entrar com GitHub,
GitLab ou e-mail). O plano gratuito cobre esse formulário com folga.

---

## Etapa 1 — Publicar

### Caminho A · Terminal (mais rápido, 2 minutos)

Abra o terminal **dentro da pasta do projeto** e rode:

```bash
npx vercel login
```

Depois:

```bash
npx vercel --prod
```

Na primeira vez ele faz algumas perguntas. As respostas:

| Pergunta | Resposta |
|---|---|
| Set up and deploy? | **Y** |
| Which scope? | sua conta |
| Link to existing project? | **N** |
| What's your project's name? | `ye-formulario` (ou o que preferir) |
| In which directory is your code located? | `./` |
| Want to modify these settings? | **N** |

No fim ele imprime o endereço, algo como `https://ye-formulario.vercel.app`.

Para publicar qualquer alteração futura, basta rodar `npx vercel --prod` de novo.

### Caminho B · GitHub (deploy automático a cada mudança)

```bash
git init
git add .
git commit -m "Formulário de entrada YE"
```

Crie um repositório vazio no GitHub, conecte e envie:

```bash
git remote add origin https://github.com/SEU-USUARIO/ye-formulario.git
git branch -M main
git push -u origin main
```

Em seguida, em [vercel.com/new](https://vercel.com/new), importe o repositório.
A Vercel detecta um site estático sozinho — **não preencha build command nem output
directory**, deixe tudo em branco e clique em Deploy.

A partir daí, todo `git push` publica automaticamente.

---

## Etapa 2 — Gravar o domínio nas meta tags

Com o endereço em mãos, rode uma vez:

```bash
python definir-dominio.py https://ye-formulario.vercel.app
```

Isso deixa absolutas as URLs da imagem de prévia — aquela que aparece quando alguém manda
o link no WhatsApp ou no Instagram. Com caminho relativo funciona na maioria dos casos;
com o endereço completo funciona em todos.

Depois publique de novo (`npx vercel --prod` ou `git push`).

Para conferir a prévia, cole o link em
[developers.facebook.com/tools/debug](https://developers.facebook.com/tools/debug/)
e clique em *Scrape Again*.

---

## Etapa 3 — Ligar o destino das respostas

**Essa etapa é obrigatória antes de divulgar.** Enquanto `CONFIG.endpoint` estiver vazio
no `index.html`, o formulário completa o fluxo mas as respostas não chegam a lugar nenhum.

O passo a passo está no [LEIA-ME.md](LEIA-ME.md) — Google Sheets (recomendado) ou Formspree.

Uma observação sobre a Vercel: o `vercel.json` traz uma política de segurança que só permite
o formulário conversar com o Google Apps Script e o Formspree. Se você usar outro serviço,
acrescente o endereço dele na linha `connect-src` do `vercel.json`, senão o navegador
bloqueia o envio.

---

## Domínio próprio

No painel do projeto: **Settings → Domains → Add**. Digite o domínio
(ex.: `entrada.ye.com.br`), e a Vercel mostra os registros DNS para cadastrar no seu
provedor. O certificado HTTPS é emitido automaticamente.

Se trocar de domínio, rode `definir-dominio.py` de novo com o endereço novo.

---

## O que cada arquivo faz

| Arquivo | Vai para o servidor? | Papel |
|---|---|---|
| `index.html` | sim | o formulário inteiro, foto embutida |
| `og.jpg` | sim | imagem da prévia do link (1200×630) |
| `robots.txt` | sim | libera a indexação no Google |
| `vercel.json` | config | cabeçalhos de segurança e cache |
| `.vercelignore` | config | mantém os arquivos de trabalho fora do servidor |
| `LEIA-ME.md` | não | documentação |
| `DEPLOY-VERCEL.md` | não | este guia |
| `google-apps-script.gs` | não | código para colar na planilha |
| `trocar-foto.py` | não | troca a foto do topo |
| `definir-dominio.py` | não | grava o domínio nas meta tags |
| `foto-grupo.jpg` | não | cópia da foto, só para conferência |

---

## Detalhes da configuração

**Cache** — o HTML é servido com `must-revalidate`, então quando você publicar uma correção
todo mundo vê na hora, sem precisar limpar cache. A imagem de prévia tem cache de 24h.

**Cabeçalhos de segurança** — `nosniff`, `X-Frame-Options`, `Referrer-Policy`,
`Permissions-Policy` (câmera, microfone e localização bloqueados, já que o formulário não
usa nada disso) e uma Content-Security-Policy restrita.

**URLs limpas** — `cleanUrls` e `trailingSlash: false`: o formulário abre na raiz do
domínio, sem `/index.html` no endereço.

**Tirar do Google** — se preferir o formulário só por link direto, troque o `robots.txt`
pelo bloco comentado que está dentro dele e mude a meta tag `robots` no `index.html`
para `content="noindex, nofollow"`.
