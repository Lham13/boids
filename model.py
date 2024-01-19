import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from fish import Fish
from tools import *


class Model:

    def __init__(
        self,
        size,
        step_size=1,
    ):
        self.x_lim = [-size[0]/2, size[0]/2]
        self.y_lim = [-size[1]/2, size[1]/2]
        self.step_size = step_size

        self.library = {}

    def get(self, id):
        return self.library[id]

    def add(self, fish):
        """
        Add new fish instance to the model
        """
        if isinstance(fish, Fish):
            fish.model = self
            self.library[fish.id] = fish
        elif isinstance(fish, list):
            for element in fish:
                self.add(element)

    def update(self):
        """
        Update model for one step
        """
        for id in self.library:
            fish = self.get(id)
            fish.update(self.step_size)

    def run(self, steps=1):
        """
        Run simulation
        """
        for _ in range(steps):
            self.update()

    def create_animation(self):
        """
        Animate the simulation result
        """
        # Read the simulation history
        x_positions = []
        y_positions = []
        for id in self.library:
            fish = self.get(id)
            history = np.array(fish.history)
            history = history.T
            x_positions.append(history[0])
            y_positions.append(history[1])

        x_positions = np.array(x_positions)
        y_positions = np.array(y_positions)
        num_steps = len(x_positions[0])

        # Setup the plot
        fig, ax = plt.subplots()
        points, = plt.plot([], [], 'bo')  # Points object for updating the positions
        ax.set_xlim(self.x_lim)
        ax.set_ylim(self.y_lim)

        # Initialize the points
        def init():
            points.set_data([], [])
            return points,

        # Update function for animation
        def update(frame):
            x = x_positions[:, frame]
            y = y_positions[:, frame]
            points.set_data(x, y)
            return points,

        # Create the animation
        ani = FuncAnimation(fig, update, frames=num_steps, init_func=init, blit=True, interval=50)
        return ani

    def animate(self):
        """
        Animate the simulation result
        """
        ani = self.create_animation()
        plt.show()

    def save(self, name="sample.mp4"):
        ani = self.create_animation()
        ani.save(name, writer="ffmpeg")