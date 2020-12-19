import os
import json
import pandas as pd
import numpy as np
from os import walk
from pathlib import Path


# 1.0
path_root = Path(__file__).parent.parent
static_folder = os.path.join(path_root, 'data', 'hsi')


# 2.0
file2 = os.path.join(static_folder, 'hsi-pe-2.csv')
df2 = pd.read_csv(file2)
df2.index = df2['date']
df2.drop(columns=['date'], inplace=True)
names = df2.columns.values.tolist()


# 3.0

