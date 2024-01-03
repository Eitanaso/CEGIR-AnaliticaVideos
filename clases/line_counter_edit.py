from supervision.detection.line_counter import LineZone, LineZoneAnnotator
from supervision.geometry.core import Point, Rect, Vector
from typing import Dict, Optional

import cv2
import numpy as np

from supervision.detection.core import Detections
from supervision.draw.color import Color

########################################################################################
# Codigo de @maddust en https://github.com/roboflow/supervision/discussions/107
########################################################################################

class Contador_Actualizado(LineZone):
    def __init__(self, name, start: Point, end: Point, grace_period: int = 30):
        self.name = name
        self.vector = Vector(start=start, end=end)
        self.tracker_state: Dict[str, bool] = {} # Flag for each tracker_id
        self.already_counted: Dict[str, bool] = {} # Flag for each tracker_id
        self.frame_last_seen: Dict[str, int] = {} # Last frame each tracker_id was encountered
        self.current_frame: int = 0 # Current frame counter
        self.in_count: int = 0
        self.out_count: int = 0
        self.grace_period = grace_period # Number of frames to wait before resetting
    
    def is_within_line_segment(self, point: Point, margin: float = 5) -> bool:
        """
        Check if a point is within the line segment.
        Attributes:
        point (Point): The point to be checked.
        margin (float): Additional margin added to the line segment boundaries.

        Returns:
            bool: True if the point is within the line segment, False otherwise.
        """
        x_within = min(self.vector.start.x, self.vector.end.x) - margin <= point.x <= max(self.vector.start.x, self.vector.end.x) + margin
        y_within = min(self.vector.start.y, self.vector.end.y) - margin <= point.y <= max(self.vector.start.y, self.vector.end.y) + margin

        return x_within and y_within
    
    def trigger(self, detections: Detections):
        self.current_frame += 1  # Increment frame counter

        for xyxy, _, confidence, class_id, tracker_id in detections:
            # handle detections with no tracker_id
            if tracker_id is None:
                continue

            # we check if the bottom center anchor of bbox is on the same side of vector
            x1, y1, x2, y2 = xyxy
            anchor = Point(x=(x1+x2)/2, y=y2)  # Bottom center point of bounding box

            # Check if anchor is within the line segment
            if not self.is_within_line_segment(anchor):
                continue

            tracker_state = self.vector.is_in(point=anchor)

            # handle new detection
            if tracker_id not in self.tracker_state:
                self.tracker_state[tracker_id] = tracker_state
                self.already_counted[tracker_id] = False  # When the object appears, it has not been counted yet
                self.frame_last_seen[tracker_id] = self.current_frame  # Update last seen frame
                continue

            # handle detection on the same side of the line
            if self.tracker_state.get(tracker_id) == tracker_state:
                continue

            # check if this crossing has already been counted
            if self.already_counted.get(tracker_id, False):  # If it has been counted, we skip this
                # Check if grace period has passed since last encounter
                if self.current_frame - self.frame_last_seen.get(tracker_id, 0) > self.grace_period:
                    self.already_counted[tracker_id] = False  # Reset after grace period
                else:
                    continue

            self.tracker_state[tracker_id] = tracker_state
            self.already_counted[tracker_id] = True  # After counting, we mark this crossing as already counted
            self.frame_last_seen[tracker_id] = self.current_frame  # Update last seen frame

            if tracker_state:
                self.in_count += 1
            else:
                self.out_count += 1