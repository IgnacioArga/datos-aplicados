import time, numpy as np, pandas as pd, polars as pl
def bench(N, reps=3):
    rng=np.random.default_rng(7)
    t=rng.integers(1,51,N); v=rng.gamma(2,50,N)
    pdf=pd.DataFrame({"tienda":t,"ventas":v}); pld=pl.DataFrame({"tienda":t,"ventas":v})
    bp=[];bl=[]
    for _ in range(reps):
        s=time.perf_counter(); pdf.groupby("tienda",as_index=False)["ventas"].sum(); bp.append(time.perf_counter()-s)
        s=time.perf_counter(); pld.group_by("tienda").agg(pl.col("ventas").sum()); bl.append(time.perf_counter()-s)
    return min(bp)*1000, min(bl)*1000
for N in [10_000, 1_000_000, 5_000_000, 20_000_000]:
    p,l=bench(N)
    print(f"{N:>12,} filas | pandas {p:8.1f} ms | polars {l:7.1f} ms | {p/l:5.1f}x")
