# Product Tracker & Price History

Una solución robusta de monitoreo de productos que utiliza técnicas de **Web Scraping** y una arquitectura de **Microservicios/Monorepo** para realizar un seguimiento histórico de precios, calificaciones y promociones.

## 🚀 ¿Qué problema resuelve?

En el comercio electrónico actual, los precios y promociones fluctúan constantemente (Dynamic Pricing). Este sistema resuelve la falta de visibilidad sobre estas variaciones mediante:

1.  **Monitoreo Automatizado:** Extrae datos en tiempo real de múltiples fuentes mediante una URL.
2.  **Registro Histórico:** No solo guarda el estado actual, sino que almacena cada cambio detectado para análisis de tendencias.
3.  **Detección de Cambios:** Implementa lógica de comparación para registrar variaciones únicamente cuando hay cambios reales en precio o rating.
4.  **Normalización de Datos:** Consolida información de diferentes estructuras HTML en un modelo relacional único en PostgreSQL.

---

## 🛠️ Stack Técnico

El proyecto utiliza un enfoque **Polyglot** para aprovechar lo mejor de cada ecosistema:

### **Backend & API**
* **Node.js + TypeScript:** Core de la lógica de negocio.
* **NestJS:** Framework para una arquitectura escalable y modular.
* **Prisma ORM:** Manejo de la base de datos PostgreSQL con tipos fuertes.
* **PostgreSQL:** Almacenamiento relacional de productos e histórico.

### **Scraper Service**
* **Python + FastAPI:** API interna de alto rendimiento para el worker de scraping.
* **Selenium:** Extracción de datos de SPAs y sitios con renderizado de JavaScript complejo.
* **Pydantic:** Validación del contrato de datos entre Python y Node.js.

### **Infraestructura**
* **Docker & Docker Compose:** Containerización y orquestación de servicios.
* **Redis (Opcional):** Para manejo de colas de tareas asíncronas.

---

## 📂 Estructura del Proyecto



```text
├── products_api/      # API Rest en NestJS
├── scraper_api/   # Microservicio de extracción en Python
├── docker/            # Configuración de infraestructura
└── docker-compose.yml # Orquestador de contenedores
```