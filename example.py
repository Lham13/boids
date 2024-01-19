import numpy as np

from model import Model
from fish import Fish


model_size = [20, 20]
m = Model(size=model_size, step_size=1)
fish_count = 100
np.random.seed(1)
xs = np.random.uniform(-model_size[0]/2, model_size[0]/2, size=fish_count)
ys = np.random.uniform(-model_size[1]/2, model_size[1]/2, size=fish_count)
vxs = np.random.uniform(-3, 3, size=fish_count)
vys = np.random.uniform(-3, 3, size=fish_count)
school = []
for i in range(fish_count):
    fish = Fish(id=i, pos=[xs[i], ys[i]], velocity=[vxs[i], vys[i]])
    school.append(fish)
m.add(school)
m.run(steps=200)
#m.save()   
m.animate()
