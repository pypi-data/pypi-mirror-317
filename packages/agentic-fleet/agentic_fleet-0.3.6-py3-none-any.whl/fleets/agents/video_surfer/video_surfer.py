from typing import Any, Dict, List, Optional, Union, Callable
import logging
import cv2
import numpy as np
from pathlib import Path

from ...core.agent import Agent
from ...core.config import AgentConfig

logger = logging.getLogger(__name__)

class VideoSurferAgent(Agent):
    """Agent specialized in video processing and analysis."""
    
    def __init__(
        self,
        config: AgentConfig,
        system_message: Optional[str] = None,
        tools: Optional[Dict[str, Callable]] = None,
        functions: Optional[List[Dict[str, Any]]] = None,
        base_dir: Optional[Union[str, Path]] = None
    ):
        if system_message is None:
            system_message = """You are a video processing expert that can:
1. Extract frames from videos
2. Analyze video content
3. Process video metadata
4. Extract audio from video
5. Handle video operations safely and efficiently"""
            
        super().__init__(config, system_message, tools, functions)
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        
    def _resolve_path(self, path: Union[str, Path]) -> Path:
        """Resolve path relative to base_dir."""
        path = Path(path)
        return path if path.is_absolute() else self.base_dir / path
        
    async def get_video_info(self, video_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """Get video metadata."""
        try:
            video_path = self._resolve_path(video_path)
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                logger.error(f"Failed to open video: {video_path}")
                return None
                
            info = {
                "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                "fps": cap.get(cv2.CAP_PROP_FPS),
                "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "duration": int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
            }
            
            cap.release()
            return info
            
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
            
    async def extract_frames(
        self,
        video_path: Union[str, Path],
        output_dir: Union[str, Path],
        interval: float = 1.0,
        max_frames: Optional[int] = None
    ) -> List[Path]:
        """Extract frames from video at specified interval."""
        try:
            video_path = self._resolve_path(video_path)
            output_dir = self._resolve_path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                logger.error(f"Failed to open video: {video_path}")
                return []
                
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps * interval)
            frame_count = 0
            saved_frames = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                if frame_count % frame_interval == 0:
                    frame_path = output_dir / f"frame_{frame_count:06d}.jpg"
                    cv2.imwrite(str(frame_path), frame)
                    saved_frames.append(frame_path)
                    
                    if max_frames and len(saved_frames) >= max_frames:
                        break
                        
                frame_count += 1
                
            cap.release()
            return saved_frames
            
        except Exception as e:
            logger.error(f"Error extracting frames: {e}")
            return []
            
    async def analyze_motion(
        self,
        video_path: Union[str, Path],
        sample_rate: int = 1
    ) -> Optional[Dict[str, Any]]:
        """Analyze motion in video."""
        try:
            video_path = self._resolve_path(video_path)
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                logger.error(f"Failed to open video: {video_path}")
                return None
                
            ret, prev_frame = cap.read()
            if not ret:
                return None
                
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            frame_count = 1
            motion_scores = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                if frame_count % sample_rate == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    flow = np.zeros_like(prev_gray, dtype=np.float32)
                    flow = cv2.calcOpticalFlowFarneback(
                        prev=prev_gray, next=gray, flow=flow, pyr_scale=0.5, levels=3, winsize=15, iterations=3, poly_n=5, poly_sigma=1.2, flags=0
                    )
                    magnitude = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
                    motion_score = np.mean(magnitude)
                    motion_scores.append(motion_score)
                    prev_gray = gray
                    
                frame_count += 1
                
            cap.release()
            
            return {
                "mean_motion": float(np.mean(motion_scores)),
                "max_motion": float(np.max(motion_scores)),
                "motion_scores": [float(score) for score in motion_scores]
            }
            
        except Exception as e:
            logger.error(f"Error analyzing motion: {e}")
            return None
            
    async def extract_scene_changes(
        self,
        video_path: Union[str, Path],
        threshold: float = 30.0,
        min_scene_length: int = 15
    ) -> List[Dict[str, Any]]:
        """Detect scene changes in video."""
        try:
            video_path = self._resolve_path(video_path)
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                logger.error(f"Failed to open video: {video_path}")
                return []
                
            fps = cap.get(cv2.CAP_PROP_FPS)
            scenes = []
            prev_hist = None
            frame_count = 0
            scene_start = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                hist = cv2.calcHist([frame], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
                hist = cv2.normalize(hist, hist).flatten()
                
                if prev_hist is not None:
                    diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CHISQR)
                    if diff > threshold and (frame_count - scene_start) >= min_scene_length:
                        scenes.append({
                            "start_frame": scene_start,
                            "end_frame": frame_count,
                            "start_time": scene_start / fps,
                            "end_time": frame_count / fps,
                            "duration": (frame_count - scene_start) / fps
                        })
                        scene_start = frame_count
                        
                prev_hist = hist
                frame_count += 1
                
            cap.release()
            
            # Add final scene
            if frame_count - scene_start >= min_scene_length:
                scenes.append({
                    "start_frame": scene_start,
                    "end_frame": frame_count,
                    "start_time": scene_start / fps,
                    "end_time": frame_count / fps,
                    "duration": (frame_count - scene_start) / fps
                })
                
            return scenes
            
        except Exception as e:
            logger.error(f"Error detecting scenes: {e}")
            return [] 