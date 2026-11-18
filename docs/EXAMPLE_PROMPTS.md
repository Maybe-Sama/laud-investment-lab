# Primeras consultas que podrás hacer a Claude en este repo

## Modo asesor: foto financiera

> Quiero evaluar mi situación financiera actual. Primero dime qué datos necesitas y ofrece la plantilla de `docs/INVESTOR_PROFILE.md`. No inventes mis importes, inversiones ni horizonte. Una vez te entregue el perfil, elabora un informe siguiendo `docs/DECISION_REPORT.md`, con fecha de datos, fuentes verificables, importes en EUR, escenarios, comisiones, posibles efectos fiscales españoles y alternativas de riesgo. No envíes órdenes.

## Modo asesor: decisión concreta

> Analiza [ISIN/ticker/mercado y divisa]. Contrasta precios y fundamentales con fuentes actuales, costes de compra y custodia, riesgo de divisa y escenarios. Di qué datos reales faltan antes de recomendar una asignación. Señala con claridad dónde hay incertidumbre.

## Modo trader: solo simulación

> En este repositorio, crea un experimento paper de una estrategia simple, con universo, fechas, métricas y benchmark. Separa entreno y test temporal, descuenta comisiones y slippage, evita look-ahead bias y produce un informe reproducible. NO conectes brokers reales, NO habilites live ni cambies los límites de riesgo sin autorización explícita.

## Modo investigación de repos

> Examina `catalog/repos.json`, ejecuta `python scripts/sync_upstreams.py list`, y luego selecciona únicamente dos candidatos para la próxima fase. Comprueba licencia y versión oficial antes de instalar, identifica costes, problemas abiertos, experiencia de usuarios y prueba a pequeña escala. Da una recomendación argumentada.
