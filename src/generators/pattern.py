"""
Pattern Generator - Visual grid-based pattern passwords.
"""

import secrets
from typing import List, Tuple
from .base import BaseGenerator, GeneratorResult


class PatternGenerator(BaseGenerator):
    """Generate pattern-style passwords with visual grid representation."""
    
    @property
    def generator_type(self) -> str:
        return "pattern"
    
    def generate(
        self,
        grid_size: int = 3,
        path_length: int = 5
    ) -> GeneratorResult:
        """
        Generate a pattern password.
        
        Args:
            grid_size: Grid dimensions (3x3, 4x4, or 5x5)
            path_length: Number of points in the path
            
        Returns:
            GeneratorResult with pattern representation
        """
        if grid_size not in [3, 4, 5]:
            raise ValueError("Grid size must be 3, 4, or 5")
        if path_length < 4:
            raise ValueError("Path length must be at least 4")
        if path_length > grid_size * grid_size:
            raise ValueError(f"Path length cannot exceed {grid_size * grid_size}")
        
        # Number points 1-9 (3x3), 1-16 (4x4), or 1-25 (5x5)
        total_points = grid_size * grid_size
        available = list(range(1, total_points + 1))
        
        # Generate random path (no repeats)
        path: List[int] = []
        for _ in range(path_length):
            point = secrets.choice(available)
            path.append(point)
            available.remove(point)
        
        # Create visual grid representation
        grid_lines = []
        for row in range(grid_size):
            line = []
            for col in range(grid_size):
                point_num = row * grid_size + col + 1
                if point_num in path:
                    order = path.index(point_num) + 1
                    line.append(f"[{order}]")
                else:
                    line.append("[ ]")
            grid_lines.append(" ".join(line))
        
        visual_grid = "\n".join(grid_lines)
        
        # String representation of path
        path_str = "-".join(str(p) for p in path)
        
        # Full output includes both grid and sequence
        password = f"{path_str}\n\n{visual_grid}"
        
        # Entropy: permutations of path_length from total_points
        # P(n, r) = n! / (n-r)!
        import math
        permutations = math.perm(total_points, path_length)
        entropy_bits = math.log2(permutations)
        
        parameters = {
            "grid_size": grid_size,
            "path_length": path_length,
            "path": path,
            "visual_grid": visual_grid,
            "pool_size": permutations
        }
        
        return GeneratorResult(
            password=path_str,
            entropy_bits=entropy_bits,
            generator_type=self.generator_type,
            parameters=parameters
        )
