"""
Ejemplos reproducibles de "gráfico equivocado vs correcto" para la Semana Viz.
- Sirve para LUN (tipo de gráfico segun la pregunta) y MAR (malas practicas).
- Datos 100% sinteticos/genericos: NO hay info de cliente ni empleador.

Genera 2 figuras:
  1) eje_truncado.png      -> mala practica: eje Y que no arranca en 0 (exagera diferencias)
  2) pie_vs_barras.png     -> mala practica: torta de 8 porciones vs barras ordenadas

Requiere: matplotlib, pandas
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "."

# ---------------------------------------------------------------
# Ejemplo 1: EJE TRUNCADO (miente) vs EJE DESDE 0 (honesto)
# Mismo dato: ventas de 4 meses, muy parecidas entre si.
# ---------------------------------------------------------------
meses = ["Ene", "Feb", "Mar", "Abr"]
ventas = [102, 104, 103, 106]   # diferencias reales pequenas (~4%)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

# MAL: eje arranca en 100 -> Abr "se ve" varias veces mas alto que Ene
ax1.bar(meses, ventas, color="#d64545")
ax1.set_ylim(100, 107)
ax1.set_title("MAL: eje truncado (arranca en 100)")
ax1.set_ylabel("Ventas (k)")

# BIEN: eje desde 0 -> se ve que las barras son casi iguales
ax2.bar(meses, ventas, color="#2e8b57")
ax2.set_ylim(0, 120)
ax2.set_title("BIEN: eje desde 0 (diferencias reales)")
ax2.set_ylabel("Ventas (k)")

# verificacion numerica: cuanto exagera el eje truncado
delta_real = (ventas[-1] - ventas[0]) / ventas[0] * 100  # ~3.9%
# altura visual en el grafico truncado (base = 100)
alto_ene_trunc = ventas[0] - 100   # 2
alto_abr_trunc = ventas[-1] - 100  # 6
exageracion = alto_abr_trunc / alto_ene_trunc  # 3x

fig.suptitle(
    f"Mismo dato. Crecimiento REAL Ene->Abr: {delta_real:.1f}%  |  "
    f"El eje truncado lo hace parecer {exageracion:.0f}x mas alto",
    fontsize=11,
)
fig.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(f"{OUT}/eje_truncado.png", dpi=130)
plt.close(fig)

# ---------------------------------------------------------------
# Ejemplo 2: TORTA de 8 porciones (ilegible) vs BARRAS ORDENADAS
# Mismo dato: participacion de 8 categorias parecidas entre si.
# ---------------------------------------------------------------
cats = ["A", "B", "C", "D", "E", "F", "G", "H"]
share = [16, 15, 14, 13, 12, 11, 10, 9]  # suma 100, valores cercanos

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

# MAL: torta de 8 porciones -> imposible ordenar/comparar de un vistazo
ax1.pie(share, labels=cats, autopct="%1.0f%%", startangle=90)
ax1.set_title("MAL: torta de 8 porciones\n(¿quien es mayor, B o C?)")

# BIEN: barras ordenadas de mayor a menor -> comparacion inmediata
orden = sorted(zip(cats, share), key=lambda x: x[1], reverse=True)
cats_o = [c for c, _ in orden]
share_o = [s for _, s in orden]
ax2.barh(cats_o[::-1], share_o[::-1], color="#2e8b57")
ax2.set_title("BIEN: barras ordenadas\n(comparas en 1 segundo)")
ax2.set_xlabel("Participacion (%)")
for i, v in enumerate(share_o[::-1]):
    ax2.text(v + 0.2, i, f"{v}%", va="center", fontsize=9)

fig.tight_layout()
fig.savefig(f"{OUT}/pie_vs_barras.png", dpi=130)
plt.close(fig)

# ---------------------------------------------------------------
# Salida verificable por consola
# ---------------------------------------------------------------
print("== EJE TRUNCADO ==")
print(f"Crecimiento real Ene->Abr: {delta_real:.2f}%")
print(f"Exageracion visual del eje truncado: {exageracion:.1f}x")
print()
print("== TORTA vs BARRAS ==")
print("Diferencia entre la categoria mayor y la menor:",
      f"{max(share) - min(share)} puntos ({max(share)}% vs {min(share)}%)")
print("En torta, 8 porciones tan cercanas son indistinguibles a simple vista.")
print()
print("Figuras guardadas en:", OUT)
