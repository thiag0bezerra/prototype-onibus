import json
import requests
from bs4 import BeautifulSoup


def fetch_geojson(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Falha ao carregar os horários."
    return response.text


def fetch_schedule(url):
    response = requests.get(url)
    if response.status_code != 200:
        return "Falha ao carregar os horários."

    soup = BeautifulSoup(response.text, "html.parser")
    schedule_sections = soup.find_all(
        "div", class_="col-xl-4 col-lg-6 col-md-6 col-sm-12 mb-3"
    )
    schedules = {}

    for section in schedule_sections:
        period = section.find("strong").text.strip()
        times = [
            span.text
            for span in section.find_all(
                "span", class_="badge badge-secondary badge-legenda-a"
            )
        ]
        schedules[period] = times

    return schedules


def fetch_bus_data(base_url, start_page=1):
    page = start_page
    results = []
    while True:
        url = f"{base_url}/linhas-de-onibus?page={page}&codigo=&nome="
        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Verifica se é a última página
        if soup.find("li", class_="page-item active").find("a").text.strip() != str(
            page
        ):
            break

        # Encontra a tabela e extrai os dados de cada linha
        table = soup.find("table")
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if cols:
                linha = cols[0].text.strip()
                itinerario_link = cols[1].find("a")["href"]
                horario_link = cols[2].find("a")["href"]
                horario_data = fetch_schedule(f"{base_url}/{horario_link}")
                results.append(
                    {
                        "linha": linha,
                        "itinerario_link": f"{base_url}/{itinerario_link}",
                        "horario_link": f"{base_url}/{horario_link}",
                        "horarios": horario_data,
                        "geojson": fetch_geojson(
                            f"{base_url}/{itinerario_link}geojson"
                        ),
                    }
                )

        page += 1

    return results


base_url = "https://servicos.semobjp.pb.gov.br"
bus_data = fetch_bus_data(base_url)

# write to json



with open("bus_data.json", "w") as f:
    json.dump(bus_data, f)
