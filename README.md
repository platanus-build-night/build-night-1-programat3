
# 🌿 Encuentra tu Flora Nativa

[![Made with Flask](https://img.shields.io/badge/Made%20with-Flask-blue)](https://flask.palletsprojects.com/)

Una aplicación web minimalista para encontrar, explorar y seleccionar especies de flora nativa según tu ubicación.

---

## 🚀 Tecnologías utilizadas

- **Flask** — Framework web en Python.
- **Jinja2** — Motor de plantillas para HTML dinámico.
- **HTML5** — Estructura de páginas.
- **CSS3** — Estilo minimalista y responsivo.
- **JavaScript** — Interactividad en el navegador.
- **Hammer.js** — Reconocimiento de gestos (swipes).

---

## 📂 Estructura del Proyecto

```
/data/            # Data del proyecto utilizada
    -   RasgosCL_aggregatedspp.csv     #Data utilizada para obtener razgos de cada planta, por su nombre científico, obtenida desde [rasgos.cl](https://rasgos.cl/)
    -   especies_zona.json             #Data generada utilizando la investigación de [Rodolfo Gajardo](https://fundacionphilippi.cl/wp-content/uploads/2024/05/La-Vegetaci%C3%B3n-Natural-de-Chile-Rodolfo-Gajardo.pdf)
    -   coordinates_zonas.json          #Data generada desde la misma [investigación](https://fundacionphilippi.cl/wp-content/uploads/2024/05/La-Vegetaci%C3%B3n-Natural-de-Chile-Rodolfo-Gajardo.pdf), para encontrar las coordenadas del centroide de las sub-zonas.

/templates/       # Plantillas HTML
    ._formhelpers.html  # Página que formatea el formulario de forma óptima para su posterior uso en index.html
    - index.html        # Página para ingresar dirección
    - coordinates.html  # Página de swipe de flora
app.py            # Código principal de la aplicación Flask
functions_varias.py #Sección que contiene las funciones y consultas a Gemini
README.md         # Documentación del proyecto
```

---

## ⚙️ Funcionalidades principales

- **Pantalla de carga** al enviar formularios.
- **Swipe** a la derecha para aceptar y a la izquierda para descartar especies.
- **Listado final** de tus especies aceptadas.
- **Navegación fácil** entre búsqueda y resultados.

---

## ✨ Mejoras futuras

- Integración con API de mapas/geolocalización.
- Persistencia de datos para usuarios registrados.
- Mejoras visuales en animaciones de tarjetas.

---

## 🖼️ Capturas de pantalla

> ![Demo](./images/demo.gif)

---

## 🧑‍💻 Autor

- **Nombre:** Lía Da Silva Rojas
- **GitHub:** [@programat3](https://github.com/programat3)

