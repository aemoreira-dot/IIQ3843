📐 3. Ecuaciones de Balance de Energía para Tanque TES de Lecho Empacado

Este documento detalla el modelo acoplado de transferencia de calor utilizado para simular el comportamiento térmico de un tanque de Almacenamiento de Energía Térmica (TES) de lecho empacado (Packed Bed TES), implementado y resuelto numéricamente con OpenTerrace.

Se utiliza la alúmina como material de referencia para las partículas sólidas, y todos los materiales se comparan bajo un conjunto de condiciones idénticas de operación.

🔥 3.1. Balance de Energía del Fluido (Fase de Carga)

El fluido (agua) fluye en la dirección axial ($z$) e intercambia calor con las partículas sólidas. El modelo considera la convección, la transferencia de calor convectiva con el sólido y la dispersión/difusión axial.

Ecuación Diferencial Parcial

$$\varepsilon \,\rho_f c_{p,f}\,\frac{\partial T_f}{\partial t}
+\varepsilon \,\rho_f c_{p,f}\,u\,\frac{\partial T_f}{\partial z}
=
\frac{\partial}{\partial z}\left( k_{\mathrm{ax}} \frac{\partial T_f}{\partial z} \right)
- a_s\, h \left(T_f - T_s^{\mathrm{surf}}\right)$$

Donde:

Símbolo

Descripción

Unidad

$\varepsilon$

Porosidad del lecho

-

$\rho_f c_{p,f}$

Capacidad calorífica volumétrica del fluido

$\mathrm{J/(m^3\,K)}$

$u$

Velocidad superficial del fluido

$\mathrm{m/s}$

$k_{\mathrm{ax}}$

Conductividad/dispersión axial efectiva

$\mathrm{W/(m\,K)}$

$a_s$

Área específica sólido–fluido por volumen de lecho

$\mathrm{m^2/m^3}$

$h$

Coeficiente convectivo fluido–sólido

$\mathrm{W/(m^2\,K)}$

$T_f$

Temperatura del fluido

$\mathrm{^\circ C}$

$T_s^{\mathrm{surf}}$

Temperatura de la superficie de la partícula sólida

$\mathrm{^\circ C}$

Condiciones de Borde (Boundary Conditions, BCs)

El tanque opera bajo condiciones de temperatura de entrada constante y flujo de calor nulo en la salida ($z=H$).

$$T_f(0,t)=80^\circ\mathrm{C}$$

$$\left.\frac{\partial T_f}{\partial z}\right|_{z=H}=0$$

Condición Inicial (Initial Condition, IC)

La temperatura inicial uniforme del fluido es:

$$T_f(z,0)=20^\circ\mathrm{C}$$

🪨 3.2. Balance de Energía del Sólido (Partícula Esférica Hueca)

El sólido se modela como una partícula esférica hueca, y su transferencia de calor es dominada por la conducción radial transitoria. Esta aproximación permite un cálculo más preciso del gradiente de temperatura dentro de la partícula, crucial para evaluar el almacenamiento interno de energía.

Ecuación Diferencial Parcial

$$\rho_s c_{p,s}\,\frac{\partial T_s}{\partial t}
=
\frac{1}{r^2}
\frac{\partial}{\partial r}
\left( k_s r^2 \frac{\partial T_s}{\partial r} \right)$$

Condiciones de Borde (BCs)

Radio interno ($R_{\mathrm{in}}$, Aislado): Se asume una condición de simetría térmica (flujo de calor nulo) en el centro de la cavidad hueca.

$$\left.\frac{\partial T_s}{\partial r}\right|_{r=R_{\mathrm{in}}}=0$$

Superficie externa ($R_{\mathrm{out}}$, Interfaz Fluido–Sólido): El calor convectivo transferido desde el fluido se iguala al flujo de calor conductivo que entra a la partícula (Tercer tipo de BC, o Robin).

$$-k_s 
\left.\frac{\partial T_s}{\partial r}\right|_{r=R_{\mathrm{out}}}
=
h \left(T_s(R_{\mathrm{out}},t) - T_f(z,t)\right)$$

Condición Inicial (IC)

La temperatura inicial uniforme del sólido es:

$$T_s(r,0)=20^\circ\mathrm{C}$$

🔗 3.3. Acoplamiento Fluido–Sólido

El acoplamiento entre las dos ecuaciones se realiza mediante el término de intercambio de calor convectivo en la interfaz ($q''$).

Este flujo de calor por unidad de área es:

$$q'' = h\,(T_f - T_s^{\mathrm{surf}})$$

En la ecuación del fluido, el término $- a_s\, h \left(T_f - T_s^{\mathrm{surf}}\right)$ representa la pérdida de energía debido a la transferencia de calor hacia las partículas sólidas.

En la condición de borde de la superficie externa del sólido, este mismo flujo representa la ganancia de energía que impulsa la conducción radial dentro de la partícula.

🧮 3.4. Métodos Numéricos Utilizados

La implementación de OpenTerrace utiliza discretización espacial y temporal específica para cada término del balance.

Esquema Numérico

Aplicación

Término Específico

Upwind 1D

Fluido

Convección ($\varepsilon \,\rho_f c_{p,f}\,u\,\frac{\partial T_f}{\partial z}$)

Diferencia Central 1D

Fluido y Sólido

Difusión/Conducción (e.g., $\frac{\partial}{\partial z}\left( k_{\mathrm{ax}} \frac{\partial T_f}{\partial z} \right)$)

Integración Explícita

Fluido y Sólido

Avance Temporal

El paso de tiempo utilizado en la simulación es constante, asegurando estabilidad a través de restricciones tipo CFL/Fourier manejadas internamente por el solver:

$$\Delta t = 0.05\ \mathrm{s}$$

