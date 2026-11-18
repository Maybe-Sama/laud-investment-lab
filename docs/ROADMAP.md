# Hoja de ruta y entregas verificables

## Fase 0 — Entorno y auditoría (realizable hoy)

- Ejecutar `doctor`, `unittest`, `demo`.
- Revisar `catalog/repos.json` y enlaces oficiales; comprobar permisos/licencias de dependencias que se instalarán.
- Elegir un proveedor de datos y analizar coste, cobertura UE/EE. UU., latencia, divisa y límites de API.
- Elegir si el usuario prefiere Claude Code, Claude Desktop o API (cambia opciones de conectores y costes).
- Entregable: registro de decisiones y dependencias fijadas por versión.

## Fase 1 — Modo asesor (prioridad alta)

- Recoger un perfil personal voluntario mediante `docs/INVESTOR_PROFILE.md` (sin contraseñas).
- Crear esquema `PortfolioSnapshot` validado (fecha, divisa, posiciones, cash, coste, fiscalidad relevante).
- Implementar importación CSV/JSON **solo lectura** de cartera y extractos; sin credenciales iniciales.
- Integrar OpenBB u otro feed con trazabilidad de fuentes y caché de datos caducados.
- Encapsular TradingAgents en adaptador de solo análisis; contrastar sus conclusiones con reglas de asignación, riesgo y costes.
- Informes con plantilla `docs/DECISION_REPORT.md`: números, hipótesis, escenarios, incertidumbre y alternativa conservadora.
- Entregable: ejemplo reproducible (y posteriormente uno del usuario con autorización).

## Fase 2 — Sistema paper medible

- Mantener `strategy -> risk -> paper executor` como procesos/interfases independientes.
- Implementar simulación con cotizaciones históricas *point-in-time*; cubrir splits, dividendos, dividend withholding, FX y calendario bursátil.
- Evaluar con LEAN o motor cuantitativo; separar in-sample, out-of-sample y walk-forward.
- Baseline: índice diversificado adecuado al universo, buy-and-hold y estrategia simple sin IA.
- Métricas: rentabilidad neta de gastos, volatilidad, Sharpe cuando proceda, máximo drawdown, turnover, exposición, éxito de órdenes y coste de inferencia.
- Estrategia no se acepta solo por un buen backtest; paper durante un plazo definido y tamaño mínimo estadístico.
- Entregable: informe de comparación con intervalos de incertidumbre y log auditable.

## Fase 3 — Integraciones con bróker (pendiente de autorización futura)

- Comparar IBKR MCP (Research/Review & Approve/AI Partition) y LEAN + plugin IBKR por API; son flujos distintos.
- Verificar entidad y productos disponibles para residente fiscal en España; no asumir IBKR AI Partition disponible.
- Diseño de credenciales de mínimo privilegio, llaves paper separadas, límites en servidor, supervisión, alarmas, idempotencia, reconciliación, circuit breakers y procedimientos de emergencia.
- Revisión de seguridad antes de implementar un adaptador de ejecución real, cuya activación **no es parte de este repositorio inicial**.

## Criterios de no-go

No hay operativa real si no existe evidencia de que la infraestructura funciona, benchmark razonable, logs completos, límites efectivos y autorización humana inequívoca. Un agente nunca puede decidir por sí mismo levantar este bloqueo.
