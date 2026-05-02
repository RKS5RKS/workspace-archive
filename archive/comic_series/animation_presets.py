#!/usr/bin/env python3
"""
Animation Preset Library
Defines reusable animation sequences for characters
"""
import os
from PIL import Image, ImageDraw

# Base configuration
ASSETS_DIR = "/home/openclaw/.openclaw/workspace/comic_series/assets"
OUTPUT_DIR = f"{ASSETS_DIR}/output"

class AnimationPreset:
    """Base class for animation presets"""
    def __init__(self, name, frame_count, fps=12):
        self.name = name
        self.frame_count = frame_count
        self.fps = fps
    
    def get_frame(self, frame_index):
        """Get the offset/delta for this frame"""
        raise NotImplementedError
    
    def get_duration(self):
        """Get total duration in seconds"""
        return self.frame_count / self.fps

class WalkCycle(AnimationPreset):
    """Basic walk cycle animation"""
    def __init__(self):
        super().__init__("walk", frame_count=8, fps=8)
    
    def get_frame(self, frame_index):
        """Walk cycle keyframes"""
        frames = [
            {'left_leg': (0, 0), 'right_leg': (20, 0), 'torso': (0, 2), 'left_arm': (10, 0), 'right_arm': (-10, 0)},
            {'left_leg': (-5, 0), 'right_leg': (15, 0), 'torso': (0, 3), 'left_arm': (8, 0), 'right_arm': (-8, 0)},
            {'left_leg': (-10, 0), 'right_leg': (10, 0), 'torso': (0, 4), 'left_arm': (5, 0), 'right_arm': (-5, 0)},
            {'left_leg': (-15, 0), 'right_leg': (5, 0), 'torso': (0, 3), 'left_arm': (3, 0), 'right_arm': (-3, 0)},
            {'left_leg': (-20, 0), 'right_leg': (0, 0), 'torso': (0, 2), 'left_arm': (0, 0), 'right_arm': (0, 0)},
            {'left_leg': (-15, 0), 'right_leg': (5, 0), 'torso': (0, 1), 'left_arm': (-3, 0), 'right_arm': (3, 0)},
            {'left_leg': (-10, 0), 'right_leg': (10, 0), 'torso': (0, 0), 'left_arm': (-5, 0), 'right_arm': (5, 0)},
            {'left_leg': (-5, 0), 'right_leg': (15, 0), 'torso': (0, 1), 'left_arm': (-8, 0), 'right_arm': (8, 0)},
        ]
        return frames[frame_index % len(frames)]

class Idle(AnimationPreset):
    """Idle breathing animation"""
    def __init__(self):
        super().__init__("idle", frame_count=4, fps=4)
    
    def get_frame(self, frame_index):
        """Idle breathing keyframes"""
        frames = [
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (0, 0), 'head': (0, 0), 'left_arm': (0, 0), 'right_arm': (0, 0)},
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (0, -1), 'head': (0, -1), 'left_arm': (0, -1), 'right_arm': (0, -1)},
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (0, -2), 'head': (0, -2), 'left_arm': (0, -2), 'right_arm': (0, -2)},
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (0, -1), 'head': (0, -1), 'left_arm': (0, -1), 'right_arm': (0, -1)},
        ]
        return frames[frame_index % len(frames)]

class Talk(AnimationPreset):
    """Talking animation (mouth movement implied)"""
    def __init__(self):
        super().__init__("talk", frame_count=6, fps=12)
    
    def get_frame(self, frame_index):
        """Talk keyframes"""
        frames = [
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (0, 0), 'head': (0, 0), 'left_arm': (0, 0), 'right_arm': (0, 0)},
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (1, 0), 'head': (2, 0), 'left_arm': (0, 0), 'right_arm': (0, 0)},
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (0, 0), 'head': (0, 0), 'left_arm': (0, 0), 'right_arm': (0, 0)},
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (-1, 0), 'head': (-2, 0), 'left_arm': (0, 0), 'right_arm': (0, 0)},
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (0, 0), 'head': (0, 0), 'left_arm': (0, 0), 'right_arm': (0, 0)},
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (1, 0), 'head': (1, 0), 'left_arm': (0, 0), 'right_arm': (0, 0)},
        ]
        return frames[frame_index % len(frames)]

class Punch(AnimationPreset):
    """Punching animation"""
    def __init__(self):
        super().__init__("punch", frame_count=6, fps=12)
    
    def get_frame(self, frame_index):
        """Punch keyframes"""
        frames = [
            {'left_leg': (0, 0), 'right_leg': (10, 0), 'torso': (5, 0), 'head': (0, 0), 'left_arm': (0, 0), 'right_arm': (0, 0)},
            {'left_leg': (-10, 0), 'right_leg': (20, 0), 'torso': (10, 0), 'head': (5, 0), 'left_arm': (-20, 0), 'right_arm': (50, -20)},
            {'left_leg': (-20, 0), 'right_leg': (30, 0), 'torso': (15, 0), 'head': (10, 0), 'left_arm': (-30, 0), 'right_arm': (120, -40)},
            {'left_leg': (-10, 0), 'right_leg': (20, 0), 'torso': (10, 0), 'head': (5, 0), 'left_arm': (-20, 0), 'right_arm': (80, -30)},
            {'left_leg': (0, 0), 'right_leg': (10, 0), 'torso': (5, 0), 'head': (0, 0), 'left_arm': (-10, 0), 'right_arm': (20, -10)},
            {'left_leg': (0, 0), 'right_leg': (0, 0), 'torso': (0, 0), 'head': (0, 0), 'left_arm': (0, 0), 'right_arm': (0, 0)},
        ]
        return frames[frame_index % len(frames)]

# Preset library
PRESETS = {
    'walk': WalkCycle,
    'idle': Idle,
    'talk': Talk,
    'punch': Punch,
}

def get_preset(name):
    """Get animation preset by name"""
    if name in PRESETS:
        return PRESETS[name]()
    raise ValueError(f"Unknown preset: {name}")

def list_presets():
    """List all available presets"""
    return list(PRESETS.keys())

if __name__ == "__main__":
    print("Animation Presets:")
    for name in list_presets():
        preset = get_preset(name)
        print(f"  - {name}: {preset.frame_count} frames at {preset.fps} fps ({preset.get_duration():.2f}s)")