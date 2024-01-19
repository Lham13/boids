import numpy as np
from copy import deepcopy

from tools import *


class Fish:

    def __init__(
        self,
        id,
        pos,
        velocity
    ):
        self.id = id
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.attention_range = 3
        self.history = [deepcopy(self.pos)] # position history
        self.model = None

    def neighbors(self):
        result = []
        for id in self.model.library:
            if id != self.id:
                pos_other = self.model.library[id].pos
                d = distance(self.pos, pos_other)
                if d < self.attention_range:
                    result.append(id)
        return result
    
    def center(self, ids):
        positions = []
        for id in ids:
            fish = self.model.get(id)
            positions.append(fish.pos)
        return np.mean(positions, axis=0)
    
    def group_velocity(self, ids):
        velocities = []
        for id in ids:
            fish = self.model.get(id)
            velocities.append(fish.velocity)
        return np.mean(velocities, axis=0)

    def update_velocity(self):
        neighbors = self.neighbors()
        if len(neighbors) != 0:
            alignment_strength = 0.1
            cohesion_strength = 0.1
            separation_strength = 0.1
            separation_distance = 1.0  # Minimum distance for separation

            # Alignment
            avg_group_velocity = self.group_velocity(neighbors).astype(float)  # Ensure float type
            alignment = (avg_group_velocity - self.velocity) * alignment_strength

            # Cohesion
            group_center = self.center(neighbors).astype(float)  # Ensure float type
            cohesion = (group_center - self.pos) * cohesion_strength

            # Separation
            separation = np.array([0.0, 0.0], dtype=float)  # Ensure float type
            for id in neighbors:
                neighbor = self.model.get(id)
                distance_to_neighbor = distance(self.pos, neighbor.pos)
                if distance_to_neighbor < separation_distance:
                    separation -= (neighbor.pos - self.pos) / distance_to_neighbor

            separation *= separation_strength

            # Update velocity
            self.velocity += alignment + cohesion + separation

            # Optional: Limit the speed to prevent too fast movement
            #max_speed = 2.0
            #if np.linalg.norm(self.velocity) > max_speed:
            #    self.velocity = self.velocity / np.linalg.norm(self.velocity) * max_speed

    def update_pos(self, step_size):
        self.pos += step_size * self.velocity
        # Boundary check
        if self.pos[0] < self.model.x_lim[0]:
            # Change position
            offset = self.model.x_lim[0] - self.pos[0]
            self.pos[0] += 2 * offset
            # Change velocity
            vx = self.velocity[0]
            vy = self.velocity[1]
            self.velocity = np.array([-vx, vy])
        if self.pos[0] > self.model.x_lim[1]:
            # Change position
            offset = self.pos[0] - self.model.x_lim[1]
            self.pos[0] -= 2 * offset
            # Change velocity
            vx = self.velocity[0]
            vy = self.velocity[1]
            self.velocity = np.array([-vx, vy])
        if self.pos[1] < self.model.y_lim[0]:
            # Change position
            offset = self.model.y_lim[0] - self.pos[1]
            self.pos[1] += 2 * offset
            # Change velocity
            vx = self.velocity[0]
            vy = self.velocity[1]
            self.velocity = np.array([vx, -vy])
        if self.pos[1] > self.model.y_lim[1]:
            # Change position
            offset = self.pos[1] - self.model.y_lim[1]
            self.pos[1] -= 2 * offset
            # Change velocity
            vx = self.velocity[0]
            vy = self.velocity[1]
            self.velocity = np.array([vx, -vy])

    def update(self, step_size):
        self.update_pos(step_size)
        self.update_velocity()
        self.history.append(deepcopy(self.pos))