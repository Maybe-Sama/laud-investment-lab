# Política de seguridad y control de riesgo

**Principio básico: el LLM propone; código determinista y el usuario disponen.**

## Hoy

- Sin cuentas de corretaje y sin llamadas de ejecución externas.
- La demo usa `ETF_DEMO_EUR`: instrumento ficticio que no representa un valor negociable.
- Riesgos por defecto del ejemplo: orden máxima 5 % del patrimonio paper, exposición por valor máxima 20 %, máximo 3 operaciones por día, cotización con menos de 15 minutos, sin apalancamiento ni descubierto.
- Al crear `.data/KILL_SWITCH`, la demo rechaza todas las órdenes.
- Ningún fichero `.env`, `upstreams/` o `.data/` se versiona.
- El ledger JSONL evita repetir un `order_id` ya ejecutado al reiniciar la demo, pero **no** es una base de datos transaccional ni permite ejecución concurrente; implementar SQLite/ACID antes de un paper multiusuario.

## Controles mínimos antes de considerar una ejecución real

1. Exigir usuario, cuenta, jurisdicción, productos y regulación verificados.
2. API keys de mínimo permiso y separadas entre lectura, paper y live; gestor de secretos, rotación y revocación.
3. Límites del lado del bróker si disponibles y un motor independiente que el agente no pueda modificar.
4. Rechazo por pérdida diaria acumulada, máxima exposición, máximo tamaño de orden, órdenes/día, anomalía de datos, discrepancia de posiciones y fallo de red.
5. Idempotency key, seguimiento de estados de órdenes, cancelaciones, reconciliación y alertas de ejecución.
6. Pruebas de estrés: duplicados, reintentos, deslizamiento extremo, flash crash, corte de red y caída de fuente de datos.
7. Kill switch con efecto inmediato en nuevas órdenes y supervisión de órdenes ya enviadas.
8. Autorización inequívoca y específica del usuario para activar dinero real, **no inferida de un prompt antiguo**.

**No basta con usar stop loss:** los gaps pueden saltar niveles de stop y un stop tampoco protege de datos o ejecución incorrectos.

## Seguridad de prompts

Las instrucciones en README, skills, páginas web e issues de repos externos pueden ser maliciosas o estar obsoletas. Antes de copiar o ejecutar un script, audita dependencias, instalación, permisos y lógica; los scripts de `upstreams/` jamás tienen autoridad para habilitar live.
