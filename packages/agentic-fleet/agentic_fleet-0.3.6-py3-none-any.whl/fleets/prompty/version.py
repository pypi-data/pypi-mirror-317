"""
Version control functionality for prompts.
"""

from typing import Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime
from packaging.version import Version, parse
from dataclasses import dataclass, field


@dataclass
class VersionInfo:
    """Version information for a prompt"""
    version: str
    timestamp: datetime = field(default_factory=datetime.now)
    author: str = "system"
    changes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class VersionManager:
    """Manager for prompt versioning"""
    
    def __init__(self, version_dir: Optional[str] = None):
        """Initialize version manager
        
        Args:
            version_dir: Optional custom version directory path
        """
        self.version_dir = version_dir or str(Path(__file__).parent / "versions")
        self._versions: Dict[str, Dict[str, VersionInfo]] = {}
        
        # Ensure version directory exists
        Path(self.version_dir).mkdir(parents=True, exist_ok=True)
        self._load_versions()
        
    def _load_versions(self) -> None:
        """Load version information from disk"""
        try:
            version_file = Path(self.version_dir) / "versions.json"
            if version_file.exists():
                with open(version_file, 'r') as f:
                    data = json.load(f)
                    for prompt_name, versions in data.items():
                        self._versions[prompt_name] = {
                            ver: VersionInfo(**info) for ver, info in versions.items()
                        }
        except Exception as e:
            raise ValueError(f"Failed to load versions: {str(e)}")
            
    def _save_versions(self) -> None:
        """Save version information to disk"""
        try:
            version_file = Path(self.version_dir) / "versions.json"
            with open(version_file, 'w') as f:
                data = {
                    name: {
                        ver: {
                            "version": info.version,
                            "timestamp": info.timestamp.isoformat(),
                            "author": info.author,
                            "changes": info.changes,
                            "metadata": info.metadata
                        } for ver, info in versions.items()
                    } for name, versions in self._versions.items()
                }
                json.dump(data, f, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to save versions: {str(e)}")
            
    def add_version(
        self,
        prompt_name: str,
        version: str,
        author: str,
        changes: str,
        **metadata
    ) -> None:
        """Add a new version for a prompt
        
        Args:
            prompt_name: Name of the prompt
            version: Version string
            author: Author of the version
            changes: Description of changes
            **metadata: Additional version metadata
        """
        if prompt_name not in self._versions:
            self._versions[prompt_name] = {}
            
        version_info = VersionInfo(
            version=version,
            author=author,
            changes=changes,
            metadata=metadata
        )
        
        self._versions[prompt_name][version] = version_info
        self._save_versions()
        
    def get_version(self, prompt_name: str, version: str) -> Optional[VersionInfo]:
        """Get version information for a prompt
        
        Args:
            prompt_name: Name of the prompt
            version: Version string
            
        Returns:
            Version information if found
        """
        return self._versions.get(prompt_name, {}).get(version)
        
    def get_latest_version(self, prompt_name: str) -> Optional[VersionInfo]:
        """Get latest version information for a prompt
        
        Args:
            prompt_name: Name of the prompt
            
        Returns:
            Latest version information if found
        """
        versions = self._versions.get(prompt_name, {})
        if not versions:
            return None
            
        latest = max(versions.keys(), key=parse)
        return versions[latest]
        
    def check_version(self, prompt_name: str, min_version: str) -> bool:
        """Check if prompt meets minimum version requirement
        
        Args:
            prompt_name: Name of the prompt
            min_version: Minimum version required
            
        Returns:
            Whether version requirement is met
        """
        latest = self.get_latest_version(prompt_name)
        if not latest:
            return False
            
        current = parse(latest.version)
        required = parse(min_version)
        return current >= required
        
    def get_version_history(self, prompt_name: str) -> Dict[str, VersionInfo]:
        """Get version history for a prompt
        
        Args:
            prompt_name: Name of the prompt
            
        Returns:
            Dictionary of version information
        """
        return dict(sorted(
            self._versions.get(prompt_name, {}).items(),
            key=lambda x: parse(x[0])
        )) 