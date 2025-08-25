from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from datetime import datetime

console = Console()

def painel_local(cidade, admin1, pais, lat, lon):
    titulo = f"{cidade}, {admin1 or ''}, {pais} ({lat:.2f}, {lon:.2f})".strip()
    console.print(Panel(titulo, title="Local", expand=False))

def tabela_atual(atual: dict):
    t = Table(title="agora", show_header=True, header_style="bold")
    t.add_column("Quando")
    t.add_column("Condição")
    t.add_column("Temp (°C)", justify="right")
    t.add_column("Umidade (%)", justify="right")
    t.add_column("Precipitação (mm)", justify="right")

    quando = datetime.fromisoformat(atual["time"].replace("z", "+00:00")).strftime("%d/%m %H:%M")
    t.add_row(
        quando,
        atual["description"],
        f"{atual['temperature']:.1f}",
        f"{atual['humidity']}",
        f"{atual['precipitation']:.1f}",
    )
    console.print(t)

def tabela_proximos_dias(dias: list):
    t = Table(title="Próximos 3 dias", show_header=True, header_style="bold")
    t.add_column("Data")
    t.add_column("Condição")
    t.add_column("Mín (°C)", justify="right")
    t.add_column("Máx (°C)", justify="right")
    t.add_column("Chuva (mm)", justify="right")

    for d in dias:
        data_fmt = datetime.fromisoformat(d["date"]).strptime("%a, %d/%m")
        t.add_row(
            data_fmt,
            d["wdesc"],
            f"{d['tmin']:.1f}",
            f"{d['tmax']:.1f}",
            f"{d['rain']:.1f}",
        )
    console.print(t)