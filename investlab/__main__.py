"""CLI segura para arrancar el laboratorio."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import argparse
import json
import shutil
import sys

from .paper import PaperPortfolio, ProposedOrder, Quote, RiskLimits, execute_paper

ROOT=Path(__file__).resolve().parents[1]

def doctor() -> int:
    print('Claude Investment Lab · diagnóstico de entorno (sin red ni credenciales)')
    ok=sys.version_info >= (3,11)
    print(f'Python: {sys.version.split()[0]} | '+('OK' if ok else 'requiere 3.11+'))
    print('Git: '+(shutil.which('git') or 'NO encontrado'))
    print('Modo: SOLO PAPER / Datos: FICTICIOS / Bróker live: NO IMPLEMENTADO')
    print('Kill switch: '+('ACTIVO' if (ROOT/'.data'/'KILL_SWITCH').exists() else 'inactivo'))
    return 0 if ok else 1

def demo() -> int:
    now=datetime.now(timezone.utc)
    quotes={'ETF_DEMO_EUR':Quote('ETF_DEMO_EUR',Decimal('205.00'),now)}
    portfolio=PaperPortfolio(cash=Decimal('9000.00'), positions={'ETF_DEMO_EUR':5})
    limits=RiskLimits()
    print('*** DEMO FICTICIA: NO MERCADOS REALES, NO RECOMENDACION DE COMPRA ***')
    print('Patrimonio paper inicial EUR:',portfolio.total_equity(quotes))
    run_id=now.strftime('%Y%m%d%H%M%S%f')
    orders=[ProposedOrder(f'{run_id}-too-large','ETF_DEMO_EUR','BUY',4),
            ProposedOrder(f'{run_id}-ok','ETF_DEMO_EUR','BUY',1)]
    for order in orders:
        result=execute_paper(order,portfolio,quotes,now,limits,
                             ROOT/'.data'/'KILL_SWITCH',ROOT/'.data'/'paper_ledger.jsonl')
        print(json.dumps(result,ensure_ascii=False,indent=2))
    print('Efectivo simulado restante EUR:',portfolio.cash)
    print('Posiciones ficticias:',portfolio.positions)
    print('Auditoría local: .data/paper_ledger.jsonl')
    return 0

def main() -> int:
    parser=argparse.ArgumentParser(description='Claude Investment Lab, modo exclusivamente simulado.')
    parser.add_argument('command',choices=['doctor','demo'])
    args=parser.parse_args()
    return doctor() if args.command=='doctor' else demo()

if __name__=='__main__':
    raise SystemExit(main())
