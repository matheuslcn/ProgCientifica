import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def readJSON(_filename):
    data = json.load(open(_filename))
    return data



res = readJSON("output.json")
# resc = readJSON("outputc.json")
plt.plot(res["resultado"], label="c2")
# plt.plot(resc["resultado"], label="c")
plt.legend()
plt.show()


