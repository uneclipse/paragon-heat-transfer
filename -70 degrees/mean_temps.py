import numpy as np


with open('n70_temperatures_apres_etape_4.npy', 'rb') as f:
    last_temp_profile = np.load(f)


print(np.mean(last_temp_profile[1500:2290])-273)