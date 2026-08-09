"""
YE — troca a foto do topo do formulário.

Uso:
    python trocar-foto.py caminho\\da\\foto.jpg
    python trocar-foto.py caminho\\da\\foto.jpg --foco 0.35

A foto é recortada em formato de faixa, comprimida e embutida dentro do
index.html (o arquivo continua sendo um só, sem imagem externa).

--foco  Onde ficam os rostos na altura da foto original, de 0 (topo) a 1 (base).
        Padrão 0.42. Se os rostos ficarem cortados, ajuste e rode de novo.
        Só tem efeito em fotos verticais/quadradas — fotos já em faixa são
        usadas como estão.
"""

import base64
import io
import os
import re
import sys

from PIL import Image

PASTA = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(PASTA, "index.html")
COPIA = os.path.join(PASTA, "foto-grupo.jpg")
OG = os.path.join(PASTA, "og.jpg")

LARGURA_MAX = 900          # largura final em pixels
PROPORCAO = 1.47           # largura / altura da faixa (≈ 3:2)
QUALIDADE = 82


def recortar(im, foco):
    largura, altura = im.size
    proporcao_atual = largura / altura

    # Já está em formato de faixa? Usa como está.
    if 1.2 <= proporcao_atual <= 2.4:
        print(f"  proporcao {proporcao_atual:.2f} ja e uma faixa — sem recorte")
        return im

    alvo = int(largura / PROPORCAO)
    if alvo >= altura:
        return im

    centro = altura * foco
    topo = int(max(0, min(centro - alvo / 2, altura - alvo)))
    print(f"  recortando altura {topo}..{topo + alvo} de {altura}")
    return im.crop((0, topo, largura, topo + alvo))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    origem = sys.argv[1]
    foco = 0.42
    if "--foco" in sys.argv:
        foco = float(sys.argv[sys.argv.index("--foco") + 1])

    if not os.path.isfile(origem):
        print(f"ERRO: nao encontrei {origem}")
        sys.exit(1)

    im = Image.open(origem)
    im = im.convert("RGB")
    print(f"origem: {im.size[0]}x{im.size[1]}")

    im = recortar(im, foco)

    if im.size[0] > LARGURA_MAX:
        nova_altura = round(im.size[1] * LARGURA_MAX / im.size[0])
        im = im.resize((LARGURA_MAX, nova_altura), Image.LANCZOS)
        print(f"  redimensionado para {im.size[0]}x{im.size[1]}")

    im.save(COPIA, "JPEG", quality=QUALIDADE, optimize=True, progressive=True)
    print(f"copia salva: foto-grupo.jpg ({os.path.getsize(COPIA) // 1024} KB)")

    # Prévia do link (WhatsApp/Instagram) — 1200x630, o formato que eles esperam.
    og_h = round(im.size[0] / (1200 / 630))
    if og_h <= im.size[1]:
        topo = (im.size[1] - og_h) // 2
        og = im.crop((0, topo, im.size[0], topo + og_h))
    else:
        og = im
    og.resize((1200, 630), Image.LANCZOS).save(OG, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"previa salva: og.jpg ({os.path.getsize(OG) // 1024} KB)")

    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=QUALIDADE, optimize=True)
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

    with open(HTML, encoding="utf-8") as f:
        html = f.read()

    novo, trocas = re.subn(
        r'(<figure class="photo-hero">\s*<img src=")[^"]*(")',
        lambda m: m.group(1) + uri + m.group(2),
        html,
        count=1,
    )

    if not trocas:
        print("ERRO: nao achei a tag <img> do topo dentro do index.html")
        sys.exit(1)

    with open(HTML, "w", encoding="utf-8") as f:
        f.write(novo)

    print(f"index.html atualizado ({len(novo) // 1024} KB)")


if __name__ == "__main__":
    main()
