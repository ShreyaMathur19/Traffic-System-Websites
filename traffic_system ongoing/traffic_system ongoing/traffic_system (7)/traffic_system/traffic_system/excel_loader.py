# excel_loader.py

import pandas as pd
import random
from config import EXCEL_FILE

def load_referrers(shuffle=True):
    df = pd.read_excel(EXCEL_FILE)

    if "referrer" not in df.columns:
        raise ValueError("Excel must contain a column named 'referrer'")

    refs = df["referrer"].dropna().tolist()

    if shuffle:
        random.shuffle(refs)
        print("[SHUFFLE] Referrers shuffled")

    return refs
