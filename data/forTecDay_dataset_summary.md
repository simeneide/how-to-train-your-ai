## Short summary

- **61 variables** in total, all active (`discontinued = false`). The data source converts everything to **monthly frequency** (`ds.frequency = 12`).
- **Native frequency:** 59 are monthly. Two are daily: `I44` and `DS.OILBRSV`. These are converted to monthly by the data source; which conversion method it uses is not stated in the catalogue.
- **CPI-ATE aggregates, 3 variables:** `MSA_PCPIJAE` (total), `MSA_PCPIJAEI` (domestic sources) and `MSA_PCPIJAEIMP` (imported consumer goods).
  - 2025 = 100, seasonally adjusted with X-12-ARIMA.
  - History before December 2002 comes from PPO, after that from SSB.
- **CPI-ATE main groups, 13 variables:** `MSA_PCPIJAE_25_K1`–`K13`.
  - 2025 = 100, seasonally adjusted in FAME, source SSB (`KPI.KPIJAE.25.Kxx.IPR.U`).
- **CPI subgroups, 40 variables:** `KPI.KPI.25.Kxxx.IPR.S`. These are subgroups of the **total CPI**, not CPI-ATE.
  - SSB table 14700, 2025 = 100, seasonally adjusted by SMART models created 12–20 October 2026 (type Calculated).
  - **Watch out:** `K062`, `K064` and `K133` have no seasonal pattern, so the "seasonally adjusted" series is identical to the unadjusted one.
- **Drivers, 5 variables:**
  - `MSA_IPK` and `MSA_IPI`: international price impulses to imported consumer goods and to capital/intermediate goods (excluding energy). Calculated, seasonally adjusted.
  - `NAV.HL.TOT.PST.S` (alias `MSA_URR`): registered unemployment rate from NAV, based on NAV's seasonally adjusted series.
  - `I44` (import-weighted krone exchange rate) and `DS.OILBRSV` (Brent crude oil price): daily, type SERIES, **no vintages**. The catalogue does not describe them as seasonally adjusted.
- **Mixed seasonal adjustment:** X-12-ARIMA (CPI-ATE aggregates), FAME (CPI-ATE main groups), SMART models (CPI subgroups), NAV (unemployment rate). Keep this in mind when comparing groups or aggregating.
- **Catalogue inconsistency:** The English description of `MSA_IPK` says "imported *intermediate* goods", but the Norwegian one says "importerte *konsumvarer*" (imported consumer goods). Since `MSA_IPI` is the intermediate-goods indicator, the Norwegian description is most likely correct.

## Variable table

Legend: SA = seasonally adjusted. S = U = the seasonally adjusted series equals the unadjusted one.

| # | Variable | Group | Description (catalogue) | Freq. |
|---|----------|-------|-------------------------|-------|
| 1 | MSA_PCPIJAE | CPI-ATE aggregate | CPI adjusted for tax changes and excluding energy (CPI-ATE). 2025 = 100. SA (X-12-ARIMA). PPO before Dec 2002, then SSB | Monthly |
| 2 | MSA_PCPIJAEI | CPI-ATE aggregate | CPI-ATE, domestic sources. 2025 = 100. SA (X-12-ARIMA). Source: PPO | Monthly |
| 3 | MSA_PCPIJAEIMP | CPI-ATE aggregate | CPI-ATE, imported consumer goods. 2025 = 100. SA (X-12-ARIMA). PPO before Dec 2002, then SSB | Monthly |
| 4 | MSA_PCPIJAE_25_K1 | CPI-ATE main group (01) | Food and non-alcoholic beverages. 2025 = 100. SA (FAME) | Monthly |
| 5 | MSA_PCPIJAE_25_K2 | CPI-ATE main group (02) | Alcoholic beverages and tobacco. 2025 = 100. SA (FAME) | Monthly |
| 6 | MSA_PCPIJAE_25_K3 | CPI-ATE main group (03) | Clothing and footwear. 2025 = 100. SA (FAME) | Monthly |
| 7 | MSA_PCPIJAE_25_K4 | CPI-ATE main group (04) | Housing, water, electricity, gas and other fuels. 2025 = 100. SA (FAME) | Monthly |
| 8 | MSA_PCPIJAE_25_K5 | CPI-ATE main group (05) | Furnishings, household equipment and routine maintenance. 2025 = 100. SA (FAME) | Monthly |
| 9 | MSA_PCPIJAE_25_K6 | CPI-ATE main group (06) | Health. 2025 = 100. SA (FAME) | Monthly |
| 10 | MSA_PCPIJAE_25_K7 | CPI-ATE main group (07) | Transport. 2025 = 100. SA (FAME) | Monthly |
| 11 | MSA_PCPIJAE_25_K8 | CPI-ATE main group (08) | Information and communication. 2025 = 100. SA (FAME) | Monthly |
| 12 | MSA_PCPIJAE_25_K9 | CPI-ATE main group (09) | Recreation, sport and culture. 2025 = 100. SA (FAME) | Monthly |
| 13 | MSA_PCPIJAE_25_K10 | CPI-ATE main group (10) | Education. 2025 = 100. SA (FAME) | Monthly |
| 14 | MSA_PCPIJAE_25_K11 | CPI-ATE main group (11) | Restaurants and accommodation services. 2025 = 100. SA (FAME) | Monthly |
| 15 | MSA_PCPIJAE_25_K12 | CPI-ATE main group (12) | Insurance and financial services. 2025 = 100. SA (FAME) | Monthly |
| 16 | MSA_PCPIJAE_25_K13 | CPI-ATE main group (13) | Miscellaneous goods and services. 2025 = 100. SA (FAME) | Monthly |
| 17 | KPI.KPI.25.K021.IPR.S | CPI subgroup (02) | Alcoholic beverages | Monthly |
| 18 | KPI.KPI.25.K023.IPR.S | CPI subgroup (02) | Tobacco | Monthly |
| 19 | KPI.KPI.25.K131.IPR.S | CPI subgroup (13) | Personal care | Monthly |
| 20 | KPI.KPI.25.K132.IPR.S | CPI subgroup (13) | Other personal effects | Monthly |
| 21 | KPI.KPI.25.K139.IPR.S | CPI subgroup (13) | Other services | Monthly |
| 22 | KPI.KPI.25.K121.IPR.S | CPI subgroup (12) | Insurance | Monthly |
| 23 | KPI.KPI.25.K122.IPR.S | CPI subgroup (12) | Financial services | Monthly |
| 24 | KPI.KPI.25.K111.IPR.S | CPI subgroup (11) | Food and beverage serving services | Monthly |
| 25 | KPI.KPI.25.K112.IPR.S | CPI subgroup (11) | Accommodation services | Monthly |
| 26 | KPI.KPI.25.K051.IPR.S | CPI subgroup (05) | Furniture, furnishings and loose carpets | Monthly |
| 27 | KPI.KPI.25.K052.IPR.S | CPI subgroup (05) | Household textiles | Monthly |
| 28 | KPI.KPI.25.K053.IPR.S | CPI subgroup (05) | Household appliances | Monthly |
| 29 | KPI.KPI.25.K054.IPR.S | CPI subgroup (05) | Glassware, tableware and household utensils | Monthly |
| 30 | KPI.KPI.25.K055.IPR.S | CPI subgroup (05) | Tools and equipment for house and garden | Monthly |
| 31 | KPI.KPI.25.K056.IPR.S | CPI subgroup (05) | Goods and services for routine household maintenance | Monthly |
| 32 | KPI.KPI.25.K091.IPR.S | CPI subgroup (09) | Recreational durables | Monthly |
| 33 | KPI.KPI.25.K092.IPR.S | CPI subgroup (09) | Other recreational goods | Monthly |
| 34 | KPI.KPI.25.K093.IPR.S | CPI subgroup (09) | Garden products and pets | Monthly |
| 35 | KPI.KPI.25.K096.IPR.S | CPI subgroup (09) | Cultural services | Monthly |
| 36 | KPI.KPI.25.K097.IPR.S | CPI subgroup (09) | Newspapers, books and stationery | Monthly |
| 37 | KPI.KPI.25.K081.IPR.S | CPI subgroup (08) | Information and communication equipment | Monthly |
| 38 | KPI.KPI.25.K083.IPR.S | CPI subgroup (08) | Information and communication services | Monthly |
| 39 | KPI.KPI.25.K071.IPR.S | CPI subgroup (07) | Purchase of vehicles | Monthly |
| 40 | KPI.KPI.25.K072.IPR.S | CPI subgroup (07) | Operation of personal transport equipment | Monthly |
| 41 | KPI.KPI.25.K073.IPR.S | CPI subgroup (07) | Passenger transport services | Monthly |
| 42 | KPI.KPI.25.K061.IPR.S | CPI subgroup (06) | Medicines and health products | Monthly |
| 43 | KPI.KPI.25.K031.IPR.S | CPI subgroup (03) | Clothing | Monthly |
| 44 | KPI.KPI.25.K032.IPR.S | CPI subgroup (03) | Footwear | Monthly |
| 45 | KPI.KPI.25.K041.IPR.S | CPI subgroup (04) | Actual rental payments for housing | Monthly |
| 46 | KPI.KPI.25.K042.IPR.S | CPI subgroup (04) | Imputed rental payments for housing | Monthly |
| 47 | KPI.KPI.25.K043.IPR.S | CPI subgroup (04) | Maintenance, repair and security of the dwelling | Monthly |
| 48 | KPI.KPI.25.K044.IPR.S | CPI subgroup (04) | Water supply and misc. services relating to the dwelling | Monthly |
| 49 | KPI.KPI.25.K045.IPR.S | CPI subgroup (04) | Electricity, gas and other fuels | Monthly |
| 50 | KPI.KPI.25.K011.IPR.S | CPI subgroup (01) | Food | Monthly |
| 51 | KPI.KPI.25.K012.IPR.S | CPI subgroup (01) | Non-alcoholic beverages | Monthly |
| 52 | KPI.KPI.25.K074.IPR.S | CPI subgroup (07) | Transport services for goods | Monthly |
| 53 | KPI.KPI.25.K098.IPR.S | CPI subgroup (09) | Package holidays | Monthly |
| 54 | KPI.KPI.25.K064.IPR.S | CPI subgroup (06) | Other health services (no seasonal pattern, S = U) | Monthly |
| 55 | KPI.KPI.25.K062.IPR.S | CPI subgroup (06) | Out-patient services (no seasonal pattern, S = U) | Monthly |
| 56 | KPI.KPI.25.K133.IPR.S | CPI subgroup (13) | Social protection (no seasonal pattern, S = U) | Monthly |
| 57 | I44 | Exchange rate | Import-weighted krone exchange rate, 44 trading partners | Daily |
| 58 | NAV.HL.TOT.PST.S | Labour market | Registered unemployment rate (NAV), completely unemployed, both sexes. Based on NAV's SA series. Alias `MSA_URR` | Monthly |
| 59 | DS.OILBRSV | Oil price (Datastream) | Brent crude, BFO Dated FOB North Sea | Daily |
| 60 | MSA_IPI | Price impulses | International price impulses to imported capital and intermediate goods (IPI), excluding energy. 2015 = 100. SA | Monthly |
| 61 | MSA_IPK | Price impulses | Price impulses to imported goods (IPK). Index, 2001 = 100. Seasonally adjusted. | Monthly |

All 61 variables have `discontinued = false` in the catalogue. All have vintages except `I44` and `DS.OILBRSV`.
Descriptions are shortened from the catalogue's English text. For `MSA_PCPIJAE_25_K2`, `K11` and `K13`, the wording follows the Norwegian description where the English one differs.
