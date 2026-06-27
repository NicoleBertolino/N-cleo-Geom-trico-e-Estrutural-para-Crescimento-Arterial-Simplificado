import os
import numpy as np
import pyvista as pv


def carregar_segmentos(nome_arquivo):
    """Lê o arquivo de segmentos gerado pelo código C/C++ e prepara

    os dados para o formato exigido pelo PyVista.
    """
    if not os.path.exists(nome_arquivo):
        raise FileNotFoundError(
            f"O arquivo '{nome_arquivo}' não foi encontrado. "
            f"Certifique-se de gerar a árvore no C/C++ primeiro."
        )

    points = []
    lines = []
    idx_contador = 0

    with open(nome_arquivo, "r") as f:
        for linha in f:
            linha = linha.strip()
            # Ignora cabeçalhos ou linhas vazias
            if not linha or linha.startswith("id") or linha.startswith("#"):
                continue

            try:
                # Trata separação por vírgula ou espaço
                valores = linha.replace(",", " ").split()
                if len(valores) < 4:
                    continue

                # Coordenadas dos dois pontos que formam o segmento (vaso)
                x1, y1, x2, y2 = map(float, valores[:4])

                # O PyVista trabalha em 3D, então adicionamos z = 0.0 para o plano 2D
                points.append([x1, y1, 0.0])
                points.append([x2, y2, 0.0])

                # Formato de linha do PyVista: [número_de_pontos, id_ponto1, id_ponto2]
                lines.append([2, idx_contador, idx_contador + 1])
                idx_contador += 2

            except ValueError:
                continue

    return np.array(points), np.hstack(lines)


def main():
    # Nome do arquivo que sua nova função no C deverá gerar (ex: "arvore.txt" ou "arvore.csv")
    arquivo_dados = "pontos.csv"

    try:
        points, lines = carregar_segmentos(arquivo_dados)
    except Exception as e:
        print(f"Erro: {e}")
        return

    # Construindo a malha geométrica (PolyData) sugerida no enunciado
    mesh = pv.PolyData()
    mesh.points = points  # [cite: 139, 141]
    mesh.lines = lines  # [cite: 140, 142]

    # Configuração do Plotter (Janela de exibição)
    plotter = pv.Plotter()  # [cite: 143]
    plotter.title = "Visualização da Árvore Arterial - MiniCCO-0"
    plotter.set_background("white")  # Fundo branco para destacar o vermelho

    # Adiciona a malha da árvore
    plotter.add_mesh(
        mesh,
        color="red",  # Cor vermelha para os vasos
        line_width=3,  # Espessura sugerida na especificação [cite: 144]
        label="Árvore Arterial",
    )

    # Força a visão a ficar em 2D (plano XY) de forma estática/organizada
    plotter.view_xy()
    plotter.show_axes()
    plotter.add_legend(bcolor=None)

    # Abre a janela interativa
    plotter.show()  # [cite: 145]


if __name__ == "__main__":
    main()