import numpy as np

import vector as V
import dimensions as D

class Line(object):
    center_point = np.array(D.center, dtype=np.float32)
    
    @staticmethod
    def _edge_sum(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return (x2 - x1) * (y2 + y1)
    
    def __init__(self, p1, p2):
        self.p1, self.p2 = np.array(p1, dtype=np.float32), np.array(p2, dtype=np.float32)

        sum_over_edges  = Line._edge_sum(self.p1, Line.center_point)
        sum_over_edges += Line._edge_sum(Line.center_point, self.p2)
        sum_over_edges += Line._edge_sum(self.p2, self.p1)
        if sum_over_edges > 0: # Points are clockwise
            self.p1, self.p2 = self.p2, self.p1 # Swap end points to make them counter-clockwise

        dx, dy = V.normalize(self.p2 - self.p1)
        self.normal = np.array([dy, -dx], dtype=np.float32)
        self.direction = V.normalize(self.p2 - self.p1)
#        print(self.normal)
        
    @staticmethod
    def generate_bezier_curve(arc_points, bezier_ratio=0.1):
        if len(arc_points) != 3:
            raise ValueError('Bezier curve can be generated only using 3 points')
            
        arc_points = [np.array(point, dtype=np.float32) for point in arc_points]
        p0, p1, p2 = arc_points
            
        # Make sure points are counter-clockwise
        sum_over_edges  = Line._edge_sum(p0, p1)
        sum_over_edges += Line._edge_sum(p1, p2)
        sum_over_edges += Line._edge_sum(p2, p0)
        if sum_over_edges < 0: # Points are clockwise
            p0, p2 = p2, p0 # Swap end points to make them counter-clockwise
            
        points = []
        # Generate Bezier
        for ratio in np.arange(0.0, 1.0, D.bezier_ratio):
            distance = (p1 - p0)
            np0 = p0 + distance * ratio
            distance = (p2 - p1)
            np1 = p1 + distance * ratio
            points.append(np0 + (np1 - np0) * ratio)
        points.append(p2)
        
        lines = []
        for i in range(len(points)-1):
            lines.append(Line(points[i], points[i+1]))          
        
        return lines, points
    
    def __repr__(self):
        return str(self.p1) + ' ' + str(self.p2)
        