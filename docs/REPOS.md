# Repositorios recopilados y criterios

Metadatos completos y URLs canónicas en [`catalog/repos.json`](../catalog/repos.json). Todas las referencias se contrastaron con páginas de GitHub públicas el **18/11/2026**; las versiones concretas, estrellas y licencias pueden cambiar. Ningún resultado de rentabilidad ha sido auditado por este repositorio.

| Id de descarga | Propósito | Riesgo principal |
|---|---|---|
| `tradingagents` | Comité de analistas de IA | Errores de datos, costes y recomendaciones no probadas |
| `openbb` | Datos/infraestructura | Proveedores, latencia, cobertura y permisos |
| `ai-hedge-fund` | Laboratorio educativo | No está pensado para operar dinero real |
| `alpaca-mcp` | Integración con bróker | Paper/live con credenciales y permisos distintos |
| `ai-trader` | Referencia de autonomía | Rentabilidad no verificada y riesgo operacional |
| `lean` | Engine cuantitativo | Complejidad, muchos recursos y backtest engañoso |
| `lean-ibkr` | Conector IBKR para LEAN | Configuración, elegibilidad y riesgo de órdenes reales |
| `claude-stock-picker` | Experimento de picks | Poca adopción independiente y dependencias de pago |

## Cómo se recopilan sin crear un monorrepo inmanejable

`python scripts/sync_upstreams.py clone tradingagents openbb` descarga esos dos proyectos a `upstreams/`, uno por carpeta. Mantienen su licencia, `.git` y trayectoria upstream. No se ejecuta `pip install` ni ningún comando que los habilite. Las carpetas de terceros están en `.gitignore` para no apropiarse de su código ni crear cientos de MB en tu GitHub.

`clone --all` es posible, pero **no es recomendable para arrancar**: LEAN y OpenBB son grandes. Cuando integremos algo, fijar una referencia de versión/commit en un lockfile y revisar su licencia real en esa versión. Este directorio local es de trabajo, no un *submodule* Git formal.

## Evidencia y límites

- GitHub stars/forks: miden atención y uso potencial, **no ROI de trading**.
- Los repos de investigación pueden mejorar el flujo de trabajo sin mejorar el rendimiento económico.
- Exigir backtests reproducibles con datos *point-in-time* y resultados fuera de muestra, descontando comisiones, slippage, spread y coste del modelo.
- Cualquier cifra de una clasificación pública se considera no verificada hasta inspeccionar sus datos de operaciones, reglas y posibles sesgos.

## Licencias

Cada upstream conserva sus condiciones. **No se declara ninguna licencia de terceros en nombre de sus autores**. El archivo `LICENSE` de este repositorio cubre solamente el código y documentación originales de este hub.
