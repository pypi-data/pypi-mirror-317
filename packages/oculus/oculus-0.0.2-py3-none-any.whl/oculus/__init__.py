import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class Vector3:
    x: float
    y: float
    z: float
    
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def normalize(self):
        magnitude = (self.x**2 + self.y**2 + self.z**2)**0.5
        if magnitude == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x/magnitude, self.y/magnitude, self.z/magnitude)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

@dataclass
class Color:
    r: float  # Red (0-1)
    g: float  # Green (0-1)
    b: float  # Blue (0-1)
    a: float = 1.0  # Alpha (0-1)
    
    def __mul__(self, scalar):
        return Color(
            min(1.0, self.r * scalar),
            min(1.0, self.g * scalar),
            min(1.0, self.b * scalar),
            self.a
        )
    
    def blend(self, other):
        """Blend this color with another color using alpha compositing"""
        a_out = self.a + other.a * (1 - self.a)
        if a_out == 0:
            return Color(0, 0, 0, 0)
        
        r = (self.r * self.a + other.r * other.a * (1 - self.a)) / a_out
        g = (self.g * self.a + other.g * other.a * (1 - self.a)) / a_out
        b = (self.b * self.a + other.b * other.a * (1 - self.a)) / a_out
        
        return Color(r, g, b, a_out)

class Light:
    def __init__(self, position: Vector3, color: Color, intensity: float = 1.0):
        self.position = position
        self.color = color
        self.intensity = intensity
    
    def calculate_illumination(self, point: Vector3, normal: Vector3) -> Color:
        """Calculate illumination at a point given its normal vector"""
        light_dir = (self.position - point).normalize()
        
        # Calculate diffuse lighting using Lambert's cosine law
        cos_angle = max(0, normal.dot(light_dir))
        illumination = cos_angle * self.intensity
        
        return self.color * illumination

class Scene:
    def __init__(self, ambient_light: Color = Color(0.1, 0.1, 0.1)):
        self.lights: List[Light] = []
        self.ambient_light = ambient_light
    
    def add_light(self, light: Light):
        self.lights.append(light)
    
    def calculate_lighting(self, point: Vector3, normal: Vector3) -> Color:
        """Calculate total lighting at a point including all lights and ambient light"""
        total_color = self.ambient_light
        
        for light in self.lights:
            light_color = light.calculate_illumination(point, normal)
            total_color = total_color.blend(light_color)
            
        return total_color

class Vision:
    @staticmethod
    def calculate_visibility(
        observer: Vector3,
        target: Vector3,
        obstacles: List[Tuple[Vector3, float]]  # List of (center, radius) tuples
    ) -> float:
        """
        Calculate visibility between observer and target with obstacles
        Returns value between 0 (fully occluded) and 1 (fully visible)
        """
        direction = (target - observer).normalize()
        distance = ((target.x - observer.x)**2 + 
                   (target.y - observer.y)**2 + 
                   (target.z - observer.z)**2)**0.5
        
        visibility = 1.0
        
        for obstacle_center, obstacle_radius in obstacles:
            # Calculate closest point on line to obstacle center
            t = direction.dot(obstacle_center - observer)
            if t < 0 or t > distance:
                continue
                
            closest_point = observer + direction * t
            
            # Calculate distance from closest point to obstacle center
            obstacle_distance = ((closest_point.x - obstacle_center.x)**2 +
                               (closest_point.y - obstacle_center.y)**2 +
                               (closest_point.z - obstacle_center.z)**2)**0.5
            
            if obstacle_distance < obstacle_radius:
                # Simple occlusion model - could be made more sophisticated
                occlusion = min(1.0, (obstacle_radius - obstacle_distance) / obstacle_radius)
                visibility *= (1 - occlusion)
        
        return visibility