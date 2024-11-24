import pandas as pd
diagnosa = input()
obat = input()
Data = pd.DataFrame({
    'diagnosa ' : diagnosa,
    'obat'      : obat
})
