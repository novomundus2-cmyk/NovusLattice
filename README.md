# NovusLattice

**Sutton-Chen Empirical Potential in Sobolev $H^1(\Omega)$ Spaces & Multiscale Industrial Continuum Mechanics**

[![License: PolyForm Noncommercial 1.0.0](https://img.shields.io/badge/License-PolyForm%20Noncommercial-blue.svg)](LICENSE)
[![Academic Citation](https://img.shields.io/badge/Citation-CITATION.cff-emerald.svg)](CITATION.cff)
[![Author: Mikel Irastorza](https://img.shields.io/badge/Author-Mikel%20Irastorza-amber.svg)](https://github.com/novomundus2-cmyk)
[![Entity: Novo Mundus](https://img.shields.io/badge/Entity-Novo%20Mundus%20(Spain)-purple.svg)](https://github.com/novomundus2-cmyk)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](pyproject.toml)

---

## 1. Visión y Fundamento Físico / Vision & Core Physics

**NovusLattice** es un marco matemático y computacional desarrollado por **Mikel Irastorza** (**Novo Mundus**, España). Su objetivo es unificar la física atómica de redes cristalinas (potenciales empíricos de muchos cuerpos tipo Sutton-Chen) con la mecánica de medios continuos elastoplásticos en espacios de Sobolev $H^1(\Omega)$.

### ¿Por qué es fundamental fijarse en las fórmulas atómicas en la industria?
Tradicionalmente, la industria metalúrgica y de fabricación trata a los metales como medios homogéneos continuos gobernados por coeficientes empíricos estáticos. Sin embargo, en procesos reales de **corte**, **plegado**, **cizallado** y **manipulación robótica**, las tolerancias submilimétricas ($\pm 0.2\text{ mm}$) se violan sistemáticamente debido a fenómenos atómicos:
1. **Dislocaciones y planos de deslizamiento**: El corte no es lineal; es la propagación de dislocaciones a lo largo de planos cristalográficos $\{111\}\langle 110\rangle$.
2. **Recuperación elástica (*Springback*)**: Al doblar chapa metálica, los enlaces interatómicos estirados en la fibra exterior y comprimidos en la fibra interior liberan energía elástica acumulada en cuanto se retira el punzón.
3. **Tribología y micro-soldadura en frío (*Galling*)**: En la manipulación robótica, el contacto entre la herramienta/pinza y la chapa ocurre en asperezas nanométricas donde presiones locales superan la tensión de fluencia.
4. **Deriva térmica de taller**: Entre la mañana ($15^\circ\text{C}$) y la tarde ($35^\circ\text{C}$), la constante de red $a(T)$ se dilata y el módulo elástico $E(T)$ se degrada, alterando el ángulo final de doblado en más de medio milímetro en piezas grandes.

---

## 2. Los 4 Casos de Uso Industriales / 4 Industrial Use Cases

```
┌────────────────────────────────────────────────────────────────────────┐
│                   NOVUSLATTICE INDUSTRIAL SUITE                        │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ 1. CORTE &         │ 2. PLEGADO &       │ 3. MANIPULACIÓN ROBÓTICA     │
│    CIZALLADO       │    SPRINGBACK      │    & TRIBOLOGÍA              │
│ Dislocaciones      │ Tolerancia ±0.2 mm │ Presión en asperezas         │
│ Energía de fractura│ Ángulo sobre-doble │ Anti-gripado (anti-galling)  │
├────────────────────┴────────────────────┴──────────────────────────────┤
│ 4. DERIVA TÉRMICA Y AMBIENTAL EN PLANTA DE FABRICACIÓN                 │
│ Dilatación de red a(T) · Degradación E(T) · Compensación CNC en tiempo real │
└────────────────────────────────────────────────────────────────────────┘
```

### Caso 1: Corte y Cizallado Industrial (Shearing & Cutting)
- **Problema Industrial**: Al cizallar o punzonar chapa metálica, una holgura (*clearance*) incorrecta entre cuchillas produce desgarros, rebabas térmicas (*burrs*) y deformación plástica excesiva que arruina el filo de corte.
- **Respuesta Atómica NovusLattice**: Calcula la holgura óptima basada en la energía cohesiva del potencial de Sutton-Chen y el criterio de Von Mises sobre los planos de deslizamiento $\{111\}$:
  $$C_{\text{opt}} \approx 0.006 \cdot \sqrt{\sigma_y} \cdot t$$
- **Resultado en Aluminio 1.5 mm**: Holgura óptima recomendada de **0.139 mm (±5 µm)**, garantizando corte por cizalladura limpia sin rebabas secundarias.

### Caso 2: Plegado de Alta Precisión y Compensación de Springback (Benchmark EPTA France)
- **Problema Industrial**: En el plegado de muebles de refrigeración industrial y chasis en EPTA France, la especificación exige una tolerancia estricta de **$\pm 0.2\text{ mm}$**. El retorno elástico (*springback*) provoca que una chapa doblada a $90^\circ$ se abra hasta $90.93^\circ$, desplazando el ala en **$0.815\text{ mm}$** (¡4 veces por encima de la tolerancia permitida!).
- **Respuesta Atómica NovusLattice**: Modela el equilibrio elasto-plástico en el espacio de Sobolev $H^1(\Omega)$ y determina el sobre-plegado exacto necesario:
  $$\Delta \theta = \theta_0 (1 - K_s), \quad \theta_{\text{punch}} = 90^\circ + \Delta \theta$$
- **Resultado**: Punzón ajustado a **$90.934^\circ$**, reduciendo el error residual final a **$0.025\text{ mm}$** (cumple sobradamente con $\pm 0.20\text{ mm}$).

### Caso 3: Manipulación Robótica, Agarre y Fricción (Robotic Handling & Tribology)
- **Problema Industrial**: Robots móviles y brazos de montaje (como los del Robot Lab de MIRA) que manipulan láminas metálicas pueden rayar o deformar plásticamente las piezas debido a presiones excesivas en las asperezas de contacto, o sufrir deslizamiento catastrófico.
- **Respuesta Atómica NovusLattice**: Determina la fuerza de amarre normal admisible para no superar el límite de fluencia local $\sigma_y$:
  $$F_{\text{clamp}} \le \frac{\sigma_y \cdot A_{\text{pad}}}{\text{FS}}$$
- **Resultado en Cobre**: Límite de carga segura de **$69.3\text{ kN}$** en almohadilla de $400\text{ mm}^2$, con coeficiente de fricción estática de adherencia $\mu_s = 0.35$.

### Caso 4: Fluctuaciones Térmicas y Deriva en Planta (Thermal Drift)
- **Problema Industrial**: Las naves industriales sufren oscilaciones térmicas diarias entre la mañana ($15^\circ\text{C}$) y la tarde ($35^\circ\text{C}$).
- **Respuesta Atómica NovusLattice**: La dilatación de la constante de red $a(T) = a_0(1 + \alpha \Delta T)$ y la variación del módulo de Young $E(T)$ alargan un panel de 1 metro de aluminio en **$0.462\text{ mm}$**, provocando rechazos dimensionales en el control de calidad.
- **Resultado**: El software proporciona la matriz de compensación en tiempo real para topes CNC y cabezales de láser.

---

## 3. Formulación Matemática / Mathematical Formulation

### Potencial Empírico de Sutton-Chen (Redes FCC)
Para un conjunto de átomos con posiciones $\{r_i\}$, la energía potencial total es:
$$U_{\text{tot}} = \sum_{i} U_i = \sum_i \epsilon \left[ \frac{1}{2} \sum_{j \ne i} \left(\frac{a}{r_{ij}}\right)^n - c \sqrt{\sum_{j \ne i} \left(\frac{a}{r_{ij}}\right)^m} \right]$$

Constantes para metales cúbicos centrados en las caras (FCC):
| Metal | Símbolo | $\epsilon$ (eV) | $c$ | $a$ ($\text{\AA}$) | $n$ | $m$ | $\alpha$ ($\text{K}^{-1}$) | $E$ (GPa) |
|---|---|---|---|---|---|---|---|---|
| **Oro** | Au | $1.2793 \times 10^{-2}$ | $34.408$ | $4.078$ | 10 | 8 | $14.2 \times 10^{-6}$ | 78 |
| **Aluminio** | Al | $5.033 \times 10^{-3}$ | $16.399$ | $4.050$ | 7 | 6 | $23.1 \times 10^{-6}$ | 69 |
| **Cobre** | Cu | $1.2382 \times 10^{-2}$ | $39.432$ | $3.615$ | 9 | 6 | $16.5 \times 10^{-6}$ | 117 |
| **Níquel** | Ni | $1.5707 \times 10^{-2}$ | $39.755$ | $3.520$ | 9 | 6 | $13.4 \times 10^{-6}$ | 200 |
| **Plata** | Ag | $2.5410 \times 10^{-3}$ | $144.41$ | $4.086$ | 12 | 6 | $18.9 \times 10^{-6}$ | 83 |

### Funcional de Energía en Espacios de Sobolev $H^1(\Omega)$
$$\mathcal{E}(u) = \int_\Omega \left( \frac{1}{2} C_{ijkl} \varepsilon_{ij}(u) \varepsilon_{kl}(u) + \psi_{\text{pl}}(\bar{\varepsilon}^p) \right) d\Omega - \int_{\partial \Omega_t} t_i u_i \, dS$$

---

## 4. Instalación y Uso Rápido / Quickstart

### Instalación
```bash
git clone https://github.com/novomundus2-cmyk/NovusLattice.git
cd NovusLattice
pip install -e .
```

### Ejecutar los 4 Casos de Uso Industriales
```bash
python3 -m novuslattice.cli cases
```

### Simular Plegado y Recuperación Elástica
```bash
python3 -m novuslattice.cli bend --metal Al --thickness 1.5 --angle 90.0 --flange 50.0 --tolerance 0.20
```

### Evaluar Potencial Atómico de Sutton-Chen
```bash
python3 -m novuslattice.cli potential --metal Au --temp-k 293.15
```

### Ejecutar Suite de Tests
```bash
python3 -m unittest discover tests
```

---

## 5. Documentación y Monografía Científica

- **Monografía Oficial en PDF**: [`docs/NovusLattice_Paper_EN_Mikel_Irastorza.pdf`](docs/NovusLattice_Paper_EN_Mikel_Irastorza.pdf)
- **Versión Web Interactiva**: [`docs/index.html`](docs/index.html)

---

## 6. Citación Académica / How to Cite

Si utilizas este software o sus fórmulas en investigaciones académicas o desarrollos de ingeniería, por favor cita:

```bibtex
@software{irastorza2026novuslattice,
  author = {Irastorza, Mikel},
  title = {NovusLattice: Sutton-Chen Interatomic Potential in Sobolev H¹(Ω) Spaces & Industrial Continuum Mechanics},
  year = {2026},
  publisher = {GitHub},
  journal = {Novo Mundus Research Framework},
  howpublished = {\url{https://github.com/novomundus2-cmyk/NovusLattice}},
  version = {1.0.0}
}
```

---

## 7. Licencia / License

- **Código fuente**: [PolyForm Noncommercial License 1.0.0](LICENSE).
- **Teoría científica y fórmulas**: [Creative Commons CC BY-NC-ND 4.0](LICENSE).
- Consultas comerciales o industriales: `novomundus2@gmail.com`.
