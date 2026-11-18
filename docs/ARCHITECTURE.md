# Arquitectura objetivo (no confundir con implementación actual)

```text
Perfil personal / cartera exportada / proveedores de datos
            │
      Verificador de datos ──► (fecha, moneda, fuente, frescura)
            │
      ┌─────┴────────────────────────────────────┐
      ▼                                          ▼
[MODO A: solo lectura]                    [MODO B: simulación]
Agentes / análisis / riesgos             Estrategia → Signal JSON
      │                                          │
Informe y alternativas                    Risk Engine independiente
      │                                          │
APROBACIÓN HUMANA                              PaperBroker
                                                 │
                                      Ledger + evaluación vs benchmark
```

## Estado actual

- Implementado: simulador paper LOCAL determinista con control independiente de reglas, auditoría JSONL y tests.
- NO implementado: descarga de cotizaciones reales, cálculo de rendimientos, TradingAgents/OpenBB conectados, sincronización de cartera, notificaciones y API de un bróker.

## Contratos siguientes (propuesta)

- `MarketSnapshot`: `{symbol, currency, source, fetched_at, market_as_of, price, adjusted, delayed}`.
- `InvestorProfile`: liquidez, pasivos, horizonte, fiscalidad, perfil de pérdidas, aportaciones, compromisos.
- `TradeProposal`: `{id, strategy_version, symbol, exchange, currency, side, qty, quote_ref, rationale, created_at}`.
- `RiskDecision`: `{allow, reasons, limits_snapshot, timestamp, decision_hash}`.
- `Fill`: `{broker, paper, order_id, qty, price, fees, timestamp}`.

## Medidas contra errores típicos

- Nunca convertir EUR a USD a ojo; usar FX con fuente temporal.
- Comprobar hora local de bolsa vs UTC; evitar feriados y precios stale.
- No leer un precio futuro para simular una decisión pasada.
- Duplicados de mensajes/órdenes y fallos parciales deben ser idempotentes.
- Persistir movimientos y reconciliar cartera con extractos del bróker.
- Datos obtenidos de Internet y documentos financieros son texto no confiable, no instrucciones de ejecución.
