import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from app.api import geocodificar_cidade, obter_previsao, extrair_atual, montar_resumo_diario
from app.formatters import painel_local, tabela_atual, tabela_proximos_dias

console = Console()

def escolher_local(resultados):
    if not resultados:
        return None
    if len(resultados) == 1:
        return resultados[0]

    console.print(Panel("Foram encontrados vários locais. Escolha um:", title="Atenção"))
    for i, r in enumerate(resultados, start=1):
        console.print(f"[{i}] {r['name']} - {r.get('admin1', '')} - {r.get('country', '')}")
    while True:
        try:
            idx = int(Prompt.ask("Número do local")) - 1
            if 0 <= idx < len(resultados):
                return resultados[idx]
        except Exception:
            pass
        console.print("[red]Opção inválida. Tente novamente.[/red]")

def main():
    console.print(Panel("Previsão do Tempo - Open-Meteo", title="🌦️  CLI", expand=False))

    if len(sys.argv) > 1:
        consulta = " ".join(sys.argv[1:])
    else:
        consulta = Prompt.ask("Digite o nome da cidade (Ex.: Belém, Manaus, São Paulo)")

    resultados = geocodificar_cidade(consulta, count=5, lang="pt")
    if not resultados:
        console.print("[red]Nenhum local encontrado.[/red]")
        sys.exit(1)

    local = escolher_local(resultados)

    lat = local["latitude"]
    lon = local["longitude"]
    cidade = local["name"]
    admin1 = local.get("admin1")
    pais = local.get("country")

    painel_local(cidade, admin1, pais, lat, lon)

    previsao = obter_previsao(lat, lon, dias=3, tz_auto=True)

    atual = extrair_atual(previsao["hourly"], previsao["timezone"])
    tabela_atual(atual)

    dias = montar_resumo_diario(previsao["daily"])
    tabela_proximos_dias(dias)

    console.print("[green]✓ Concluído[/green]")

if __name__ == "__main__":
    main()