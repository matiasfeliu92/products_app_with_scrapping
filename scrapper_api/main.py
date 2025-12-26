from src.core.scrapper import Scrapper

if __name__ == "__main__":
    links = [
        "https://www.mexx.com.ar/productos-rubro/monitores/48994-monitor-gamer-24-x-micro-full-hd-ips-180hz-1ms-hdmi-x24f-kq1e.html",
        "https://fullh4rd.com.ar/prod/17972/auricular-gamer-razer-blackshark-v2-x-wired-rz04-03240100-r3u1",
        "https://www.datasoft.com.ar/tienda/computacion/componentes/memorias-ram/memoria-ddr4-32gb-3200-mushkin"
    ]
    for link in links:
        scrapper = Scrapper(link)
        scrapper.extract_data()