"""
YE — grava o domínio definitivo nas meta tags de compartilhamento.

Rode UMA VEZ, depois do primeiro deploy:

    python definir-dominio.py https://ye-formulario.vercel.app

Por que isso importa: o WhatsApp, o Instagram e o LinkedIn preferem URLs
absolutas na imagem de prévia. Com o caminho relativo a prévia funciona na
maioria dos casos, mas com o endereço completo ela funciona em todos.

Depois de rodar, faça o deploy de novo para publicar a mudança.
"""

import io
import re
import sys

HTML = r"C:\Users\lucas\OneDrive\Documents\YE\index.html"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    base = sys.argv[1].strip().rstrip("/")

    if not base.startswith("http"):
        print("ERRO: informe o endereco completo, comecando com https://")
        sys.exit(1)

    with io.open(HTML, encoding="utf-8") as f:
        html = f.read()

    # Remove um dominio anterior, caso o script ja tenha rodado antes.
    html = re.sub(r'(content=")https?://[^"]*?(/og\.jpg")', r"\1\2", html)
    html = re.sub(r'\n<link rel="canonical"[^>]*>', "", html)
    html = re.sub(r'\n<meta property="og:url"[^>]*>', "", html)

    trocas = 0

    def absoluto(m):
        nonlocal trocas
        trocas += 1
        return m.group(1) + base + m.group(2)

    html = re.sub(r'(content=")(/og\.jpg")', absoluto, html)

    # canonical + og:url logo depois da meta robots
    ancora = '<meta name="robots" content="index, follow">'
    extra = (
        ancora
        + '\n<link rel="canonical" href="' + base + '/">'
        + '\n<meta property="og:url" content="' + base + '/">'
    )
    if ancora in html:
        html = html.replace(ancora, extra, 1)

    if not trocas:
        print("Nada para trocar — o dominio ja estava definido?")
        sys.exit(1)

    with io.open(HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print("dominio definido: " + base)
    print("agora rode o deploy de novo para publicar")


if __name__ == "__main__":
    main()
