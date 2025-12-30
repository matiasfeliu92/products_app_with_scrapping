from src.core.scrapper import Scrapper

if __name__ == "__main__":
    links = [
        # "https://www.mexx.com.ar/productos-rubro/procesadores/40369-procesador-amd-ryzen-7-5700g-4.6-ghz-am4.html",
        # "https://fullh4rd.com.ar/prod/20304/micro-amd-ryzen-7-5700g-c-video-c-cooler-am4-mejor-q-5600gt",
        # "https://datasoft.com.ar/tienda/computacion/componentes/microprocesadores/micro-amd-ryzen-7-5700g-46ghz-radeon-graphics-38ghz-16mb-am4",
        # "https://www.armytech.com.ar/procesadores/605-procesador-amd-ryzen-7-5700g-am4-730143313377.html",
        # "https://compragamer.com/producto/Procesador_AMD_Ryzen_7_5700G_4_6GHz_Turbo_AM4_Wraith_Stealth_Cooler_12369?cate=27"

        "https://www.mexx.com.ar/productos-rubro/motherboards/49432-motherboard-am4-msi-a520m-pro.html",
        "https://fullh4rd.com.ar/prod/17632/mother-msi-a520m-a-pro-ddr4-am4",
        "https://datasoft.com.ar/tienda/computacion/componentes/motherboard/motherboard-gigabyte-a520m-k-v2-ddr4-am4",
        "https://www.armytech.com.ar/motherboards/5719-mother-msi-a520m-a-pro-am4.html",
        "https://compragamer.com/producto/Mother_MSI_A520M_A_PRO_DDR4_AM4_10900?cate=26&filtros=200:AMD%20A520"
    ]
    for link in links:
        scrapper = Scrapper(link)
        scrapper.extract_data()