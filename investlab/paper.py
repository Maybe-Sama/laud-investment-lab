"""Motor paper minimalista; NO se comunica con redes, LLMs ni brókeres."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import json

D=Decimal
CENT=D('0.01')

def money(value: Decimal) -> Decimal:
    return value.quantize(CENT,rounding=ROUND_HALF_UP)

@dataclass(frozen=True)
class Quote:
    symbol: str
    price: Decimal
    as_of: datetime
    currency: str='EUR'
    source: str='DEMO/FICTICIA'

@dataclass(frozen=True)
class ProposedOrder:
    order_id: str
    symbol: str
    side: str
    quantity: int

@dataclass(frozen=True)
class RiskLimits:
    max_order_fraction: Decimal=D('0.05')
    max_position_fraction: Decimal=D('0.20')
    max_orders_per_day: int=3
    max_quote_age: timedelta=timedelta(minutes=15)
    commission: Decimal=D('0.50')

@dataclass
class PaperPortfolio:
    cash: Decimal
    positions: dict[str,int]=field(default_factory=dict)
    completed_order_ids: set[str]=field(default_factory=set)
    orders_today: int=0

    def total_equity(self, quotes: dict[str,Quote]) -> Decimal:
        equity=self.cash
        for symbol, qty in self.positions.items():
            if symbol not in quotes:
                raise ValueError(f'Falta precio para valorar {symbol}')
            equity+=quotes[symbol].price*qty
        return money(equity)

@dataclass(frozen=True)
class Decision:
    allowed: bool
    reasons: tuple[str,...]
    notional: Decimal

def assess(order: ProposedOrder, portfolio: PaperPortfolio, quotes: dict[str,Quote],
           now: datetime, limits: RiskLimits, kill_switch: Path) -> Decision:
    reasons=[]
    if kill_switch.exists(): reasons.append('KILL_SWITCH activo')
    if order.order_id in portfolio.completed_order_ids: reasons.append('order_id duplicado')
    if order.side not in ('BUY','SELL'): reasons.append('Lado no admitido')
    if order.quantity <= 0 or not isinstance(order.quantity,int): reasons.append('Cantidad inválida')
    if portfolio.orders_today >= limits.max_orders_per_day: reasons.append('Límite diario de órdenes alcanzado')
    quote=quotes.get(order.symbol)
    if quote is None:
        reasons.append('Falta cotización'); return Decision(False,tuple(reasons),D('0'))
    if quote.price <= 0: reasons.append('Precio inválido')
    if quote.currency!='EUR': reasons.append('FX no implementado; solo EUR')
    if quote.source!='DEMO/FICTICIA': reasons.append('Solo cotizaciones ficticias permitidas en el MVP')
    if now.tzinfo is None or quote.as_of.tzinfo is None:
        reasons.append('Timestamp sin zona horaria')
    elif (now-quote.as_of)>limits.max_quote_age or (quote.as_of-now)>timedelta(seconds=30):
        reasons.append('Cotización caducada o futura')
    if reasons: return Decision(False,tuple(reasons),D('0'))
    notional=money(quote.price*order.quantity)
    try:
        equity=portfolio.total_equity(quotes)
    except ValueError as exc:
        return Decision(False,(str(exc),),notional)
    if equity <= 0:
        reasons.append('Patrimonio no positivo')
    else:
        if notional > equity*limits.max_order_fraction:
            reasons.append('Orden supera máximo 5 % del patrimonio')
        current_position=portfolio.positions.get(order.symbol,0)
        if order.side=='BUY':
            if portfolio.cash < notional+limits.commission:
                reasons.append('Efectivo insuficiente; prohibido margen')
            if quote.price*(current_position+order.quantity)>equity*limits.max_position_fraction:
                reasons.append('Concentración supera 20 %')
        if order.side=='SELL' and current_position<order.quantity:
            reasons.append('No se permite posición corta')
    return Decision(not reasons,tuple(reasons),notional)

def execute_paper(order: ProposedOrder, portfolio: PaperPortfolio, quotes: dict[str,Quote],
                  now: datetime, limits: RiskLimits, kill_switch: Path,
                  audit_path: Path) -> dict:
    """Ejecución determinista local. No tiene llamadas HTTP ni API de bróker."""
    # Idempotencia local entre sesiones: un order_id previamente ejecutado en el
    # ledger no debe ejecutarse por segunda vez aunque el proceso se reinicie.
    # Esto NO sustituye las transacciones ACID de un futuro motor de bróker.
    if audit_path.exists():
        with audit_path.open('r', encoding='utf-8') as prior:
            for line in prior:
                try:
                    old_record=json.loads(line)
                except json.JSONDecodeError:
                    # En producción: detener, reconciliar y reparar un ledger dañado.
                    return {'mode':'PAPER-DEMO','status':'REJECTED',
                            'order_id':order.order_id,'reasons':['Ledger corrupto; se detiene']}
                if old_record.get('order_id')==order.order_id and old_record.get('status')=='FILLED_PAPER':
                    portfolio.completed_order_ids.add(order.order_id)
    decision=assess(order,portfolio,quotes,now,limits,kill_switch)
    record={
      'mode':'PAPER-DEMO', 'order_id':order.order_id, 'symbol':order.symbol,
      'side':order.side, 'quantity':order.quantity, 'as_of':now.isoformat(),
      'status':'FILLED_PAPER' if decision.allowed else 'REJECTED',
      'reasons':list(decision.reasons), 'notional_eur':str(decision.notional),
      'commission_eur':str(limits.commission) if decision.allowed else '0.00',
      'source':quotes.get(order.symbol).source if order.symbol in quotes else 'MISSING',
    }
    if decision.allowed:
        sign=1 if order.side=='BUY' else -1
        # Comisión siempre descontada, incluso al vender.
        portfolio.cash=money(portfolio.cash-(decision.notional*sign)-limits.commission)
        portfolio.positions[order.symbol]=portfolio.positions.get(order.symbol,0)+order.quantity*sign
        portfolio.completed_order_ids.add(order.order_id)
        portfolio.orders_today+=1
    audit_path.parent.mkdir(parents=True,exist_ok=True)
    with audit_path.open('a',encoding='utf-8') as f:
        f.write(json.dumps(record,ensure_ascii=False)+'\n')
    return record
