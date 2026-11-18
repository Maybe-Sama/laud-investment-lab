# Brókeres y España — comprobación a 18 de noviembre de 2026

## Interactive Brokers (IBKR)

**Documentación primaria**:
- [Página AI Integration](https://www.interactivebrokers.com/en/trading/ai-integrations.php)
- [FAQ oficial sobre conectar Claude e IA](https://www.interactivebrokers.com/support/faq/content/connecting-ibkr-account-ai-platform-1437187133)
- [Plugin LEAN para Interactive Brokers](https://github.com/QuantConnect/Lean.Brokerages.InteractiveBrokers)

Hay que distinguir **tres canales**:

1. **MCP Research/Review & Approve**: Claude accede a datos autorizados y prepara instrucciones; el usuario las revisa y presenta órdenes manualmente. El FAQ oficial indica que soporta cuentas paper en este modo.
2. **IBKR AI Partition Autonomous Trading**: iniciativa nativa que, con cuenta elegible, permite ejecución automática en una partición financiada. **No es universal:** según el FAQ oficial consultado el 18-11-2026, el lanzamiento inicial solo incluye clientes de IBLLC, Australia, Singapur y Reino Unido. No asumir elegibilidad de una cuenta de una entidad europea. También existen criterios de historial previo, tipo de cuenta y capital.
3. **API de bróker/LEAN**: integración algorítmica convencional diferente de AI Partition. Puede permitir ejecución mediante software propio si el bróker, la cuenta, el país y los permisos lo admiten; requiere un estudio técnico y de riesgos separado. No queda activada por conectar Claude mediante MCP.

Una persona residente fiscal en España **no debe presuponer** que puede usar el modo autónomo nativo del MCP de IBKR. Confirmar entidad contractual, disponibilidad y términos vigentes antes de diseñar esa etapa.

## Alpaca

- [MCP oficial](https://github.com/alpacahq/alpaca-mcp-server)
- Su servidor contempla paper y live, pero la disponibilidad, productos y elegibilidad varían por jurisdicción. No dar por hecho que se pueda abrir una cuenta de corretaje live desde España.
- No pasar `ALPACA_PAPER_TRADE=false` sin proceso independiente de aprobación, y no montar el MCP con credenciales live en Claude Code durante la fase de evaluación.

## Fiscalidad y productos

En España, la fiscalidad y comercialización de ETF, fondos, acciones, distribuciones, dividendos y plusvalías depende del producto y situación personal. Antes de asignar porcentajes reales hay que contrastar costes, divisa, horizonte, liquidez y tributación vigente con fuentes oficiales o profesionales competentes. No introducir tipos tributarios fijos sin validar el año fiscal aplicable.
