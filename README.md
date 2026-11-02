# How to train your AI: fra statistiske modeller til nevrale nettverk

Workshop, Tech Day, Norges Bank, 6. november 2026 (90 min). Simen Eide.

Vi bygger modelltyper fra SMART (AR, VAR, BVAR, faktormodell) på nytt i PyTorch, og gjør dem om til nevrale nettverk steg for steg. Deltakerne trenger ikke kode: hver oppgave har et skjema med tall de endrer.

> **K2 - INTERNT / UNNTATT OFFENTLIGHET.** Datasettet i `data/` er fra Norges Bank. Repoet skal være privat. Ikke del dataene videre.

## Innhold

- `workshop.ipynb`: notebooken (Colab eller VS Code/Jupyter).
- `data/forTecDay.xlsx`: datasettet fra Norges Bank (61 månedlige serier: KPI-JAE, hovedgrupper, delindekser og drivere).
- `data/forTecDay_dataset_summary.md`: Yvas beskrivelse av seriene, med fallgruver (blandet sesongjustering, serier uten sesongmønster).

## Oppgaver

1. **AR er et nevralt nett med ett lag:** `nn.Linear(P, 1)`, sammenlignet med OLS.
2. **VAR og prior:** flere serier gir overtilpasning, og weight decay (= BVAR-prior) hjelper.
3. **Fra faktormodell til nevralt nett:** skjult lag som flaskehals, så ReLU og dropout.
4. **Slå AR:** fri modell, valgt på valideringsfeil. Ledertavle og prognose for oktober-KPI (SSB publiserer 10. november).

Trening 2003-2016, validering 2017-2020, test 2021-. Mål: RMSE på månedsendringen i KPI-JAE.

## Kjøre lokalt

```sh
uv run --with jupyter --with torch --with pandas --with openpyxl --with matplotlib jupyter lab workshop.ipynb
```

I Colab: åpne notebooken fra GitHub (krever innlogging, repoet er privat) og last opp `data/forTecDay.xlsx` når første celle spør.
