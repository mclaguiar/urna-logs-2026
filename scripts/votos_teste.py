"""Votos associados a cada teste estatístico.

Nas linhas de seção, votos é a soma da quantidade que o teste olha,
dentro das seções marcadas. Nas linhas de UF (último dígito, número
redondo, Mebane), votos é o total nacional dessa quantidade.
"""

from pathlib import Path

import pandas as pd

from urna_logs.config import PROJECT_ROOT

RAIZ = PROJECT_ROOT / "data" / "anomalias" / "2026"
DESTINO = PROJECT_ROOT / "data" / "anomalias" / "votos_teste.csv"


def _codigo(valor) -> str:
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        return ""
    return str(valor).removesuffix(".0")


def carregar(turno: int) -> tuple[pd.Series, pd.Series, pd.Series]:
    comparecimento = []
    votos = []
    for path in sorted(RAIZ.glob(f"secao_*_{turno}t.parquet")):
        comparecimento.append(
            pd.read_parquet(path, columns=["join_key", "bu_comparecimento"])
        )
    for path in sorted(RAIZ.glob(f"votos_*_{turno}t.parquet")):
        frame = pd.read_parquet(path, columns=["join_key", "tipo", "numero", "votos_bu"])
        frame = frame[frame["tipo"] == "nominal"]
        frame["numero"] = frame["numero"].map(_codigo)
        frame = frame[frame["numero"].isin(["13", "22"])]
        votos.append(frame)
    comp = pd.concat(comparecimento, ignore_index=True)
    comp["bu_comparecimento"] = pd.to_numeric(comp["bu_comparecimento"], errors="coerce").fillna(0)
    nominal = pd.concat(votos, ignore_index=True)
    nominal["votos_bu"] = pd.to_numeric(nominal["votos_bu"], errors="coerce").fillna(0)
    por_numero = nominal.groupby(["join_key", "numero"])["votos_bu"].sum()
    return (
        comp.groupby("join_key")["bu_comparecimento"].sum(),
        por_numero.xs("13", level="numero"),
        por_numero.xs("22", level="numero"),
    )


def somar(serie: pd.Series, chaves: pd.Series) -> int:
    if chaves.empty:
        return 0
    return int(serie.reindex(chaves.to_numpy()).fillna(0).sum())


def main() -> None:
    alertas = pd.read_csv(
        PROJECT_ROOT / "data" / "anomalias" / "alertas.csv",
        usecols=["teste", "candidato", "turno", "join_key"],
        low_memory=False,
    )
    alertas["candidato"] = alertas["candidato"].map(_codigo)
    linhas = []
    for turno in (1, 2):
        comp, v13, v22 = carregar(turno)
        pais = {"": int(comp.sum()), "13": int(v13.sum()), "22": int(v22.sum())}
        parte = alertas[alertas["turno"] == turno]
        marcadas = {
            ("z_comparecimento", ""): somar(comp, parte.loc[parte.teste == "z_comparecimento", "join_key"]),
            ("z_candidato", "13"): somar(v13, parte.loc[(parte.teste == "z_candidato") & (parte.candidato == "13"), "join_key"]),
            ("z_candidato", "22"): somar(v22, parte.loc[(parte.teste == "z_candidato") & (parte.candidato == "22"), "join_key"]),
            ("residuo_2t", "13"): somar(v13, parte.loc[(parte.teste == "residuo_2t") & (parte.candidato == "13"), "join_key"]),
            ("residuo_2t", "22"): somar(v22, parte.loc[(parte.teste == "residuo_2t") & (parte.candidato == "22"), "join_key"]),
        }
        for (teste, cand), votos in marcadas.items():
            if teste == "residuo_2t" and turno == 1:
                continue
            linhas.append({"teste": teste, "candidato": cand, "turno": turno, "votos": votos, "escopo": "secoes"})
        for cand, votos in pais.items():
            for teste in ("ultimo_digito", "numero_redondo", "mebane"):
                linhas.append({"teste": teste, "candidato": cand, "turno": turno, "votos": votos, "escopo": "pais"})
    frame = pd.DataFrame(linhas)
    frame.to_csv(DESTINO, index=False)
    print(frame.to_string(index=False))
    print(f"escrito {DESTINO}")


if __name__ == "__main__":
    main()
