import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from investlab.paper import Quote, ProposedOrder, RiskLimits, PaperPortfolio, assess, execute_paper

class RiskTests(unittest.TestCase):
    def setUp(self):
        self.now=datetime(2026,11,18,10,0,tzinfo=timezone.utc)
        self.quote=Quote('ETF_DEMO_EUR',Decimal('100'),self.now)
        self.quotes={'ETF_DEMO_EUR':self.quote}
        self.portfolio=PaperPortfolio(cash=Decimal('10000'))
        self.limits=RiskLimits()
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.kill=Path(self.tmp.name)/'KILL_SWITCH'
        self.audit=Path(self.tmp.name)/'ledger.jsonl'

    def decision(self,oid='t1',side='BUY',qty=1):
        return assess(ProposedOrder(oid,'ETF_DEMO_EUR',side,qty),self.portfolio,self.quotes,self.now,self.limits,self.kill)

    def test_accept_valid_order(self):
        self.assertTrue(self.decision().allowed)

    def test_reject_excessive_size(self):
        self.assertFalse(self.decision(qty=6).allowed)  # 600 > 5% de 10000

    def test_reject_sell_without_position(self):
        self.assertFalse(self.decision(side='SELL').allowed)

    def test_reject_stale_quote(self):
        self.quotes['ETF_DEMO_EUR']=Quote('ETF_DEMO_EUR',Decimal('100'),self.now-timedelta(minutes=30))
        self.assertFalse(self.decision().allowed)

    def test_reject_non_demo_source(self):
        self.quotes['ETF_DEMO_EUR']=Quote('ETF_DEMO_EUR',Decimal('100'),self.now,source='LIVE')
        self.assertFalse(self.decision().allowed)

    def test_reject_currency_fx_missing(self):
        self.quotes['ETF_DEMO_EUR']=Quote('ETF_DEMO_EUR',Decimal('100'),self.now,currency='USD')
        self.assertFalse(self.decision().allowed)

    def test_kill_switch(self):
        self.kill.touch()
        self.assertFalse(self.decision().allowed)

    def test_execution_is_paper_and_idempotent(self):
        o=ProposedOrder('t1','ETF_DEMO_EUR','BUY',1)
        result=execute_paper(o,self.portfolio,self.quotes,self.now,self.limits,self.kill,self.audit)
        self.assertEqual(result['status'],'FILLED_PAPER')
        self.assertEqual(self.portfolio.cash,Decimal('9899.50'))
        dup=execute_paper(o,self.portfolio,self.quotes,self.now,self.limits,self.kill,self.audit)
        self.assertEqual(dup['status'],'REJECTED')
        self.assertEqual(self.portfolio.positions['ETF_DEMO_EUR'],1)
        self.assertEqual(len(self.audit.read_text().splitlines()),2)

    def test_idempotency_across_process_restart_with_same_ledger(self):
        o=ProposedOrder('t1','ETF_DEMO_EUR','BUY',1)
        self.assertEqual(execute_paper(o,self.portfolio,self.quotes,self.now,
                        self.limits,self.kill,self.audit)['status'],'FILLED_PAPER')
        restarted_portfolio=PaperPortfolio(cash=Decimal('10000'))
        self.assertEqual(execute_paper(o,restarted_portfolio,self.quotes,self.now,
                        self.limits,self.kill,self.audit)['status'],'REJECTED')
        self.assertEqual(restarted_portfolio.cash,Decimal('10000'))

    def test_daily_order_limit(self):
        self.portfolio.orders_today=3
        self.assertFalse(self.decision().allowed)

    def test_overconcentration(self):
        self.portfolio.positions['ETF_DEMO_EUR']=20 # 2000 de 12000, añadir 5 => 2500 supera 20% =2400
        self.assertFalse(self.decision(qty=5).allowed)

if __name__=='__main__':
    unittest.main()
