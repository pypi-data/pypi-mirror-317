import csv
from dataclasses import asdict
import sys

from rich.console import Console
from rich.table import Table


def write_csv(maker, fields):
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    
    for slot in maker:
        writer.writerow(asdict(slot))


def write_table(maker, fields):
    table = Table(title="Play Booster skeleton")
    for col in fields:
        table.add_column(col)
    
    for slot in maker:
        data = asdict(slot)
        table.add_row(*[data[key] for key in fields])
    
    console = Console()
    console.print(table)
