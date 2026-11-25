from bs4 import BeautifulSoup
import csv
import re

ARQUIVO_HTML = "kb.htm"
ARQUIVO_CSV = "kanban_status.csv"

COR_EMPTY = "#fbc36e"
COR_VERDE = "#79c666"

with open(ARQUIVO_HTML, "r", encoding="utf-8", errors="ignore") as f:
    soup = BeautifulSoup(f, "html.parser")

resultado = []

for tr in soup.find_all("tr"):

    nobrs = tr.find_all("nobr")

    if not nobrs:
        continue

    # Primeiro procura o material na linha
    material = None

    for nobr in nobrs:
        texto = nobr.get_text(" ", strip=True)

        # Ignora os números dos cartões Kanban
        if re.fullmatch(r"\d{3}[+-]?", texto):
            continue

        # Primeira palavra da célula
        if texto:
            candidato = texto.split()[0]

            # Material pode ser numérico ou alfanumérico
            if candidato:
                material = candidato
                break

    if not material:
        continue

    cores_kanban = []

    for nobr in nobrs:

        texto = nobr.get_text(strip=True)

        # Identifica cartão Kanban: 001, 002, etc.
        if re.fullmatch(r"\d{3}[+-]?", texto):

            style = nobr.get("style", "").lower().replace(" ", "")

            if COR_EMPTY in style:
                cores_kanban.append("empty")

            elif COR_VERDE in style:
                cores_kanban.append("green")

    # Só processa linhas que realmente possuem Kanbans
    if not cores_kanban:
        continue

    # TRUE somente se TODOS forem amarelos
    empty = "VERDADEIRO" if all(cor == "empty" for cor in cores_kanban) else "FALSO"

    resultado.append({
        "Material": material,
        "Empty": empty
    })


with open(
    ARQUIVO_CSV,
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=["Material", "Empty"],
        delimiter=";"
    )

    writer.writeheader()
    writer.writerows(resultado)


print(f"{len(resultado)} materiais processados.")
print(f"Arquivo gerado: {ARQUIVO_CSV}")