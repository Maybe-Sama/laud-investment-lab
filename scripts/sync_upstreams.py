"""Descarga opcional de repositorios ajenos, sin instalarlos ni ejecutarlos."""
from pathlib import Path
import argparse
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
REPOS=json.loads((ROOT/'catalog'/'repos.json').read_text(encoding='utf-8'))['repositories']
BY_ID={repo['id']:repo for repo in REPOS}
DEST=ROOT/'upstreams'

def main():
    parser=argparse.ArgumentParser(description='Catálogo y clonación opcional de repos Git externos. NO ejecuta su código.')
    parser.add_argument('action', choices=['list','clone'])
    parser.add_argument('ids', nargs='*')
    parser.add_argument('--all',action='store_true',help='Descargar TODOS (puede ocupar varios GB).')
    args=parser.parse_args()
    if args.action=='list':
        for r in REPOS:
            status='descargado' if (DEST/r['id']/'.git').is_dir() else 'pendiente'
            print(f"{r['id']:22} {r['priority']:13} {status:11} {r['url']}")
        return 0
    if args.all and args.ids:
        parser.error('Usa ids o --all, no ambos.')
    ids=list(BY_ID) if args.all else args.ids
    if not ids:
        parser.error('Indica ids o --all. Recomendado: clone tradingagents openbb')
    missing=[i for i in ids if i not in BY_ID]
    if missing:
        parser.error(f'IDs desconocidos: {", ".join(missing)}')
    if shutil.which('git') is None:
        parser.error('Git no instalado o fuera del PATH')
    DEST.mkdir(exist_ok=True)
    if args.all:
        print('Aviso: el conjunto puede ocupar bastante disco. Nada se instalará ni ejecutará.')
    failures=[]
    for id_ in ids:
        repo=BY_ID[id_]
        target=DEST/id_
        if target.exists():
            print(f'SALTAR {id_}: ya existe {target} (no se modifica ni se hace pull automático).')
            continue
        print(f'DESCARGAR {id_}: {repo["url"]}',flush=True)
        result=subprocess.run(['git','clone','--depth','1','--',repo['url'],str(target)],check=False)
        if result.returncode:
            failures.append(id_)
            if target.exists():
                print(f'Revisar clonación parcial: {target}',file=sys.stderr)
    if failures:
        print('Fallaron: '+', '.join(failures),file=sys.stderr)
        return 1
    print('Listo. Los upstreams no se han instalado ni ejecutado.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
