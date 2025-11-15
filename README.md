# IIQ3843
# TES en Lecho Empacado: Benchmark de Materiales con Alúmina como Referencia

**Objetivo.** Evaluar el desempeño térmico de distintos **sólidos locales** en un **tanque de almacenamiento térmico (TES) de lecho empacado**, usando **alúmina (Al₂O₃)** como **material de referencia** y comparador base. El estudio cuantifica cómo cada material transfiere y almacena calor cuando un **fluido (agua)** circula a través del lecho.

**Brecha que aborda.** En Chile, la mayoría de medios para TES son **importados** (p. ej., alúmina). Este proyecto crea una **metodología reproducible** para comparar **materiales locales** (granito, basalto, escoria de cobre, etc.) bajo **idénticas condiciones**, entregando evidencia para sustituir materiales importados cuando sea viable.

---

## 1. Metodología (resumen)

Se utiliza **[OpenTerrace]** para resolver, en 1D axial, el **acoplamiento fluido–sólido** en un lecho empacado:

- **Fase fluido (agua):** advección + difusión/disp. axial + intercambio convectivo con el sólido.  
- **Fase sólida (partícula esférica hueca):** conducción radial transitoria + condición convectiva en la superficie.

**Caso de referencia:** Alúmina.  
Sobre esa base, se modifican **únicamente** las propiedades del sólido para cada material comparado.

---

## 2. Ecuaciones de energía

### 2.1. Fluido (eje axial \(z\))
\[
\underbrace{\varepsilon\,\rho_f c_{p,f}\,\frac{\partial T_f}{\partial t}}_{\text{almacenamiento}}
+\underbrace{\varepsilon\,\rho_f c_{p,f}\,u\,\frac{\partial T_f}{\partial z}}_{\text{convección}}
=
\underbrace{\frac{\partial}{\partial z}\!\left(k_{\mathrm{ax}}\frac{\partial T_f}{\partial z}\right)}_{\text{difusión/disp. axial}}
-\underbrace{a_s\,h\,(T_f - T_s^{\mathrm{surf}})}_{\text{intercambio fluido–sólido}}
\]

- \(\varepsilon\): porosidad del lecho.  
- \(u\): velocidad superficial (definida por el caudal másico y la sección).  
- \(k_{\mathrm{ax}}\): conductividad/dispersion axial efectiva del fluido.  
- \(a_s\): área específica sólido/volumen de lecho (p.ej. esferas: \(a_s \approx 6(1-\varepsilon)/d_p\)).  
- \(h\): coeficiente convectivo fluido–sólido.  
- \(T_s^{\mathrm{surf}}\): temperatura del sólido en la superficie de la partícula.

**Condiciones (caso base):**  
Entrada \(z=0\): \(T_f=80^\circ\mathrm{C}\).  
Salida \(z=H\): \(\partial T_f/\partial z=0\).  
Inicial: \(T_f(z,0)=20^\circ\mathrm{C}\).

### 2.2. Sólido (radio \(r\) en partícula esférica hueca)
\[
\rho_s c_{p,s}\,\frac{\partial T_s}{\partial t}
=
\frac{1}{r^2}\frac{\partial}{\partial r}\left(k_s\,r^2\,\frac{\partial T_s}{\partial r}\right)
\]

- Borde interno \(r=R_{\text{in}}\): \(\partial T_s/\partial r = 0\) (aislado).  
- Superficie \(r=R_{\text{out}}\) (interfaz con fluido):
\[
-\,k_s\,\left.\frac{\partial T_s}{\partial r}\right|_{R_{\text{out}}}
=
h\left(T_s(R_{\text{out}},t)-T_f(z,t)\right)
\]

Inicial: \(T_s(r,0)=20^\circ\mathrm{C}\).

### 2.3. Esquemas numéricos
- **Convección (fluido):** *upwind* 1D.  
- **Difusión (fluido y sólido):** diferencia central 1D.  
- **Temporal:** integración transitoria con \(\Delta t\) fijo.

> Estas ecuaciones se implementan vía configuraciones de OpenTerrace en `src/sim_alumina.py`.

---

## 3. Parámetros del caso base (Alúmina)

- **Geometría del tanque:** cilindro 1D, \(D=0.30\ \mathrm{m}\), \(H=3.0\ \mathrm{m}\).  
- **Fluido:** agua; \( \dot m = 0.04\ \mathrm{kg/s}\).  
- **Porosidad del lecho:** \(\varepsilon = 0.40\).  
- **Condiciones T:** entrada \(80^\circ\mathrm{C}\), inicial \(20^\circ\mathrm{C}\).  
- **Partícula sólida:** esfera hueca, \(R_\mathrm{in}=5\ \mathrm{mm}\), \(R_\mathrm{out}=25\ \mathrm{mm}\).  
- **Acoplamiento:** \(h=200\ \mathrm{W/m^2K}\) (constante).  
- **Tiempo simulado:** \(t_\mathrm{end}=100\ \mathrm{min}\), \(\Delta t=0.05\ \mathrm{s}\).

> Para otros materiales, se cambian **propiedades del sólido** ( \(k_s, \rho_s, c_{p,s}\) ) manteniendo el resto igual, para un **benchmark justo** comparado con alúmina.

---

## 4. Cómo reproducir

### 4.1. Instalación
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

