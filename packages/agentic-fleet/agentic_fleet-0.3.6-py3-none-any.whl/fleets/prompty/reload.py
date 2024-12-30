"""
Hot reloading functionality for prompts.
"""

import time
from typing import Dict, Any, Optional, Callable
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging


class PromptReloader(FileSystemEventHandler):
    """Handler for prompt file changes"""
    
    def __init__(
        self,
        prompts_dir: str,
        on_reload: Optional[Callable[[str], None]] = None,
        patterns: Optional[list] = None
    ):
        """Initialize prompt reloader
        
        Args:
            prompts_dir: Directory to watch for changes
            on_reload: Optional callback for reload events
            patterns: Optional list of file patterns to watch
        """
        self.prompts_dir = prompts_dir
        self.on_reload = on_reload or (lambda x: None)
        self.patterns = patterns or ["*.prompty"]
        self.logger = logging.getLogger(__name__)
        
    def on_modified(self, event):
        """Handle file modification events
        
        Args:
            event: File system event
        """
        if not event.is_directory:
            file_path = Path(event.src_path)
            if any(file_path.match(pattern) for pattern in self.patterns):
                self.logger.info(f"Detected changes in {file_path}")
                try:
                    self.on_reload(str(file_path))
                except Exception as e:
                    self.logger.error(f"Failed to reload {file_path}: {str(e)}")


class HotReloader:
    """Manager for hot reloading prompts"""
    
    def __init__(
        self,
        prompts_dir: Optional[str] = None,
        patterns: Optional[list] = None,
        recursive: bool = True
    ):
        """Initialize hot reloader
        
        Args:
            prompts_dir: Optional custom prompts directory path
            patterns: Optional list of file patterns to watch
            recursive: Whether to watch subdirectories
        """
        self.prompts_dir = prompts_dir or str(Path(__file__).parent / "prompts")
        self.patterns = patterns or ["*.prompty"]
        self.recursive = recursive
        self.observer = Observer()
        self.reload_handlers: Dict[str, Callable[[str], None]] = {}
        self.logger = logging.getLogger(__name__)
        
    def add_reload_handler(self, name: str, handler: Callable[[str], None]) -> None:
        """Add a reload handler
        
        Args:
            name: Handler name
            handler: Callback function
        """
        self.reload_handlers[name] = handler
        
    def remove_reload_handler(self, name: str) -> None:
        """Remove a reload handler
        
        Args:
            name: Handler name
        """
        self.reload_handlers.pop(name, None)
        
    def _on_reload(self, file_path: str) -> None:
        """Handle reload events
        
        Args:
            file_path: Path of changed file
        """
        for name, handler in self.reload_handlers.items():
            try:
                handler(file_path)
            except Exception as e:
                self.logger.error(f"Handler {name} failed: {str(e)}")
                
    def start(self) -> None:
        """Start watching for changes"""
        event_handler = PromptReloader(
            prompts_dir=self.prompts_dir,
            on_reload=self._on_reload,
            patterns=self.patterns
        )
        
        self.observer.schedule(
            event_handler,
            self.prompts_dir,
            recursive=self.recursive
        )
        self.observer.start()
        self.logger.info(f"Started watching {self.prompts_dir}")
        
    def stop(self) -> None:
        """Stop watching for changes"""
        self.observer.stop()
        self.observer.join()
        self.logger.info("Stopped watching for changes")
        
    def __enter__(self):
        """Start watching on context enter"""
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop watching on context exit"""
        self.stop() 