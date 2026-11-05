# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "beautifulsoup4", "pandas", "pyarrow", "numpy", "sentence-transformers", "mlx-vlm>=0.7.4,<0.8", "huggingface_hub"]
# ///
"""Lager data/taler.parquet: Norges Banks taler og foredrag med tekst, embedding og Clef-svar.

    uv run data/lag_taler.py            # alle tre steg, mellomlagrer i data/.taler/
    uv run data/lag_taler.py bygg       # bare siste steg, fra mellomlagrede filer

1. Hent: alle taler fra norges-bank.no (sitemap -> Foredrag-og-taler), dato, tittel og tekst.
2. Embedding: hver tale i biter på 1200 tegn med intfloat/multilingual-e5-base, snittet per tale (768 tall).
3. Clef: Cloudflare Clef-flash (åpen Jev-lignende beslutningsmodell, Apple Silicon/MLX) svarer på tre
   spørsmål per tale, med sannsynligheter. Krever en Mac med Apple Silicon.
"""

import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
CACHE = HERE / ".taler"
TODAY = pd.Timestamp.today().normalize()
QUESTIONS = {
    "pengepolitikk": {
        "type": "noul",
        "instructions": "Handler teksten i stor grad om inflasjon, styringsrenten eller pengepolitikken i Norge?",
    },
    "inflasjon": {
        "type": "score",
        "instructions": "Hvordan ser taleren på inflasjonen i Norge framover, sammenlignet med inflasjonsmålet? Vurder bare ut fra teksten.",
        "criteria": [
            "Klart under målet",
            "Litt under målet",
            "Rundt målet",
            "Litt over målet",
            "Klart over målet",
        ],
    },
    "rente": {
        "type": "score",
        "instructions": "Hvilket signal gir teksten om styringsrenten framover? Vurder bare ut fra teksten.",
        "criteria": ["Klart ned", "Litt ned", "Uendret", "Litt opp", "Klart opp"],
    },
}


def hent() -> None:
    import requests
    from bs4 import BeautifulSoup

    out = CACHE / "speeches.jsonl"
    done = {json.loads(line)["url"] for line in out.open()} if out.exists() else set()
    session = requests.Session()
    session.headers["User-Agent"] = "norgesbank-workshop/1.0"
    sitemap = session.get(
        "https://www.norges-bank.no/sitemaps/norges-bank/no/content.xml", timeout=30
    ).text
    urls = re.findall(r"<loc>([^<]*/Foredrag-og-taler/\d{4}/[^/<]+/)</loc>", sitemap)
    with out.open("a") as f:
        for url in urls:
            if url in done:
                continue
            s = BeautifulSoup(session.get(url, timeout=30).text, "html.parser")
            meta = s.find("meta", property="article:published_time")
            body = s.select_one("div.article__main-body") or s.select_one("article")
            row = {
                "url": url,
                "date": meta["content"] if meta else None,
                "title": s.title.text.strip() if s.title else "",
                "text": body.get_text(" ", strip=True) if body else "",
            }
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            time.sleep(0.3)


def speeches() -> pd.DataFrame:
    d = pd.read_json(CACHE / "speeches.jsonl", lines=True)
    d["dato"] = pd.to_datetime(d.date, format="%d.%m.%Y %H:%M:%S")
    return (
        d[(d.dato < TODAY) & (d.text.str.len() > 500)]
        .sort_values("dato")
        .reset_index(drop=True)
    )


def embed() -> None:
    from sentence_transformers import SentenceTransformer

    d = speeches()
    model = SentenceTransformer("intfloat/multilingual-e5-base")
    emb = []
    for t in d.text:
        parts = model.encode(
            ["passage: " + t[k : k + 1200] for k in range(0, len(t), 1200)],
            normalize_embeddings=True,
        )
        v = parts.mean(0)
        emb.append(v / np.linalg.norm(v))
    np.save(CACHE / "embeddings.npy", np.array(emb, dtype=np.float32))


def clef() -> None:
    from huggingface_hub import snapshot_download

    path = snapshot_download("mlx-community/clef-flash-4bit")
    sys.path.insert(0, path)
    import clef_mlx

    out = CACHE / "clef.jsonl"
    done = {json.loads(line)["url"] for line in out.open()} if out.exists() else set()
    model = clef_mlx.load(path)
    with out.open("a") as f:
        for r in speeches().itertuples():
            if r.url in done:
                continue
            state = f"Tale fra Norges Bank, {r.dato:%d.%m.%Y}. Tittel: {r.title}\n\n{r.text}"
            ans = model.systemone(
                {"model": "clef-flash", "state": state, "questions": QUESTIONS}
            )["answers"]
            f.write(json.dumps({"url": r.url, **ans}, ensure_ascii=False) + "\n")


def bygg() -> None:
    d = speeches()
    emb = np.load(CACHE / "embeddings.npy")
    c = pd.DataFrame(
        [json.loads(line) for line in (CACHE / "clef.jsonl").read_text().splitlines()]
    ).set_index("url")
    d["embedding"] = list(emb)
    d["clef_pengepolitikk"] = d.url.map(c.pengepolitikk.map(lambda a: a["noul"]))
    for q in ["inflasjon", "rente"]:
        d[f"clef_{q}"] = d.url.map(
            c[q].map(lambda a: a["score"] - 2)
        )  # -2 .. +2, 0 = rundt målet / uendret
        d[f"clef_{q}_sikkerhet"] = d.url.map(c[q].map(lambda a: a["confidence"]))
    out = d.rename(columns={"title": "tittel", "text": "tekst"})[
        [
            "dato",
            "tittel",
            "url",
            "tekst",
            "embedding",
            "clef_pengepolitikk",
            "clef_inflasjon",
            "clef_inflasjon_sikkerhet",
            "clef_rente",
            "clef_rente_sikkerhet",
        ]
    ]
    out.to_parquet(HERE / "taler.parquet", index=False)
    print(
        f"{len(out)} taler, {out.dato.min():%Y-%m} til {out.dato.max():%Y-%m}, {(HERE / 'taler.parquet').stat().st_size / 1e6:.1f} MB"
    )


if __name__ == "__main__":
    CACHE.mkdir(exist_ok=True)
    steps = sys.argv[1:] or ["hent", "embed", "clef", "bygg"]
    for step in steps:
        {"hent": hent, "embed": embed, "clef": clef, "bygg": bygg}[step]()
