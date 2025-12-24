from src.core.scrapper import Scrapper

if __name__ == "__main__":
    # link = "https://www.mexx.com.ar/productos-rubro/procesadores/36217-procesador-amd-ryzen-5-3400g-4.2-ghz-vega11-am4.html"
    # link = "https://fullh4rd.com.ar/prod/18168/placa-de-video-geforce-rtx-3060-12gb-msi-ventus-2x-oc"
    link = "https://www.datasoft.com.ar/tienda/computacion/almacenamiento/discos-de-estado-solido/disco-ssd-sata-240gb-hiksemi-wave-blister"
    scrapper = Scrapper(link)
    scrapper.extract_data()