import os
import glob
import shutil
import subprocess
from typing import List, Tuple, Dict, Optional
from PIL import Image


class SceneComposer:
    """Utility class to compose scenes from character assets and backgrounds.

    The class provides methods to:
    * Load character PNGs (supports multiple frames for animation)
    * Load background images
    * Composite characters onto a background at given positions
    * Apply simple camera movements (pan, zoom)
    * Export generated frames to a video using FFmpeg
    """

    def __init__(self, assets_root: str = "assets"):
        self.assets_root = assets_root
        self.characters_path = os.path.join(self.assets_root, "characters")
        self.locations_path = os.path.join(self.assets_root, "locations")
        self.tmp_dir = "tmp_frames"
        os.makedirs(self.tmp_dir, exist_ok=True)

    # ---------------------------------------------------------------------
    # Asset loading helpers
    # ---------------------------------------------------------------------
    def _load_background(self, name: str) -> Image.Image:
        """Load a background image by name.

        Parameters
        ----------
        name: str
            Filename (without extension) located under assets/locations/.
        """
        pattern = os.path.join(self.locations_path, f"{name}.*")
        candidates = glob.glob(pattern)
        if not candidates:
            raise FileNotFoundError(f"Background '{name}' not found in {self.locations_path}")
        return Image.open(candidates[0]).convert("RGBA")

    def _load_character_frames(self, character: str, action: str = "idle") -> List[Image.Image]:
        """Load a list of frames for a given character and action.

        The directory structure is expected to be:
        assets/characters/<character>/parts_detailed/<action>_*.png
        e.g. walk_0.png, walk_1.png, ...
        """
        base_dir = os.path.join(self.characters_path, character, "parts_detailed")
        pattern = os.path.join(base_dir, f"{action}_*.png")
        files = sorted(glob.glob(pattern))
        if not files:
            # Fallback: try a single image named <action>.png
            fallback = os.path.join(base_dir, f"{action}.png")
            if os.path.isfile(fallback):
                return [Image.open(fallback).convert("RGBA")]
            raise FileNotFoundError(f"No frames found for {character}/{action} in {base_dir}")
        frames = [Image.open(p).convert("RGBA") for p in files]
        return frames

    # ---------------------------------------------------------------------
    # Composition helpers
    # ---------------------------------------------------------------------
    def compose_frame(
        self,
        background: Image.Image,
        characters: List[Dict],
        camera: Optional[Dict] = None,
    ) -> Image.Image:
        """Compose a single frame.

        Parameters
        ----------
        background: Image.Image
            The background image.
        characters: list of dicts
            Each dict should contain:
                "frames": List[Image.Image] – list of animation frames for this character
                "position": Tuple[int, int] – top‑left corner where the character is placed
                "frame_index": int – which frame of the animation to use for this composition
        camera: dict (optional)
            Simple camera transformation: ``{"pan": (dx, dy), "zoom": factor}``
        """
        canvas = background.copy()
        # Apply camera pan/zoom on a copy of background first
        if camera:
            dx, dy = camera.get("pan", (0, 0))
            zoom = camera.get("zoom", 1.0)
            # Zoom (scale) the background
            if zoom != 1.0:
                w, h = canvas.size
                canvas = canvas.resize((int(w * zoom), int(h * zoom)), Image.LANCZOS)
            # Pan by cropping/offsetting
            canvas = canvas.crop((dx, dy, dx + background.width, dy + background.height))
        # Paste each character
        for char in characters:
            frame = char["frames"][char["frame_index"] % len(char["frames"])]
            pos = char["position"]
            canvas.paste(frame, pos, frame)
        return canvas

    # ---------------------------------------------------------------------
    # High‑level scene rendering
    # ---------------------------------------------------------------------
    def render_scene(
        self,
        background_name: str,
        character_specs: List[Dict],
        duration_seconds: float = 5,
        fps: int = 30,
        camera_path: Optional[List[Dict]] = None,
        output_dir: Optional[str] = None,
    ) -> List[str]:
        """Render a full scene to a series of image files.

        Returns a list of file paths for the generated frames.
        """
        bg = self._load_background(background_name)
        total_frames = int(duration_seconds * fps)
        frames_paths = []
        # Prepare character animation frames ahead of time
        characters = []
        for spec in character_specs:
            frames = self._load_character_frames(spec["character"], spec.get("action", "idle"))
            characters.append({
                "character": spec["character"],
                "frames": frames,
                "position": spec.get("position", (0, 0)),
                "animation_speed": spec.get("animation_speed", 1),  # frames per output frame
                "frame_counter": 0,
            })
        for i in range(total_frames):
            # Determine camera for this frame if a path is supplied
            cam = None
            if camera_path:
                cam = camera_path[i % len(camera_path)]
            # Build per‑character dict for compose_frame
            char_draw = []
            for ch in characters:
                index = int(ch["frame_counter"])
                char_draw.append({
                    "frames": ch["frames"],
                    "position": ch["position"],
                    "frame_index": index,
                })
                ch["frame_counter"] += ch["animation_speed"]
            frame_img = self.compose_frame(bg, char_draw, cam)
            out_path = os.path.join(self.tmp_dir, f"frame_{i:04d}.png")
            frame_img.save(out_path)
            frames_paths.append(out_path)
        return frames_paths

    # ---------------------------------------------------------------------
    # Export to video using FFmpeg
    # ---------------------------------------------------------------------
    def export_video(self, frames_pattern: str, output_path: str, fps: int = 30) -> None:
        """Run FFmpeg to stitch frames into a video.

        Parameters
        ----------
        frames_pattern: str
            Glob pattern for the input frames, e.g. "tmp_frames/frame_%04d.png".
        output_path: str
            Desired video file path.
        fps: int
            Frame rate for the video.
        """
        cmd = [
            "ffmpeg",
            "-y",
            "-framerate",
            str(fps),
            "-i",
            frames_pattern,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            output_path,
        ]
        subprocess.run(cmd, check=True)

    # ---------------------------------------------------------------------
    # Convenience wrapper
    # ---------------------------------------------------------------------
    def create_scene_video(
        self,
        background_name: str,
        character_specs: List[Dict],
        output_path: str,
        duration_seconds: float = 5,
        fps: int = 30,
        camera_path: Optional[List[Dict]] = None,
    ) -> None:
        """High‑level helper: render frames and encode video in one call."""
        self.render_scene(
            background_name,
            character_specs,
            duration_seconds=duration_seconds,
            fps=fps,
            camera_path=camera_path,
        )
        pattern = os.path.join(self.tmp_dir, "frame_%04d.png")
        self.export_video(pattern, output_path, fps=fps)
        # Cleanup temporary frames
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

# Example usage (if run as a script)
if __name__ == "__main__":
    composer = SceneComposer()
    # Simple example – expects assets to exist under the workspace.
    composer.create_scene_video(
        background_name="scene1",
        character_specs=[
            {"character": "hero", "action": "walk", "position": (100, 200), "animation_speed": 1},
        ],
        output_path="output.mp4",
        duration_seconds=3,
        fps=24,
    )
    print("Video written to output.mp4")
