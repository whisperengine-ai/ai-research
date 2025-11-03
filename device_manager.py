"""
Device Detection and Optimization Module

Automatically detects and configures optimal hardware for model inference:
- GPU/CUDA detection (NVIDIA)
- Metal Performance Shaders (MPS) detection (macOS)
- CPU fallback with optimization
- Cross-platform (macOS, Windows, Linux)
"""

import torch
import platform
import logging
from typing import Tuple, Dict, Optional

logger = logging.getLogger(__name__)


class DeviceManager:
    """Manages device detection and configuration for model inference"""
    
    def __init__(self, verbose: bool = True):
        """
        Initialize device manager
        
        Args:
            verbose: Print device detection information
        """
        self.verbose = verbose
        self.device = None
        self.device_info = {}
        self._detect_device()
    
    def _detect_device(self):
        """Detect available hardware and select optimal device"""
        
        os_name = platform.system()
        
        if self.verbose:
            print(f"🔍 Detecting device on {os_name}...")
            print(f"   PyTorch version: {torch.__version__}")
            print(f"   CUDA available: {torch.cuda.is_available()}")
        
        # Try GPU first (NVIDIA with CUDA)
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            self.device_info = {
                'type': 'GPU',
                'name': torch.cuda.get_device_name(0),
                'compute_capability': torch.cuda.get_device_capability(0),
                'total_memory': torch.cuda.get_device_properties(0).total_memory / 1e9,  # GB
                'pytorch_version': torch.__version__,
                'cuda_available': True,
            }
            if self.verbose:
                print(f"\n✅ NVIDIA GPU detected: {self.device_info['name']}")
                print(f"   Compute Capability: {self.device_info['compute_capability']}")
                print(f"   Total Memory: {self.device_info['total_memory']:.2f} GB")
        
        # macOS: Try Metal Performance Shaders (MPS)
        elif os_name == "Darwin":
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                self.device = torch.device("mps")
                self.device_info = {
                    'type': 'GPU',
                    'name': 'Apple Metal Performance Shaders (MPS)',
                    'os': 'macOS',
                    'pytorch_version': torch.__version__,
                }
                if self.verbose:
                    print(f"\n✅ Apple Metal GPU (MPS) detected")
                    print(f"   macOS will use GPU acceleration for inference")
            else:
                self.device = torch.device("cpu")
                self.device_info = {
                    'type': 'CPU',
                    'name': platform.processor(),
                    'os': 'macOS',
                    'pytorch_version': torch.__version__,
                }
                if self.verbose:
                    print(f"\n📌 Using CPU (Metal GPU not available)")
                    print(f"   Processor: {self.device_info['name']}")
        
        # Linux or Windows with CPU
        else:
            self.device = torch.device("cpu")
            self.device_info = {
                'type': 'CPU',
                'name': platform.processor(),
                'os': os_name,
                'pytorch_version': torch.__version__,
            }
            if self.verbose:
                print(f"\n📌 Using CPU")
                print(f"   OS: {os_name}")
                print(f"   Processor: {self.device_info['name']}")
        
        if self.verbose:
            print(f"   Selected Device: {self.device}\n")
    
    def get_device(self) -> torch.device:
        """Get the selected device"""
        return self.device
    
    def get_device_info(self) -> Dict:
        """Get device information dictionary"""
        return self.device_info
    
    def get_pipeline_device(self) -> int:
        """
        Get device index for HuggingFace pipelines
        Returns: 0 for first GPU, -1 for CPU
        """
        if self.device.type == "cuda":
            return 0
        else:
            return -1  # CPU
    
    def get_dtype(self) -> torch.dtype:
        """
        Get recommended data type for inference
        Returns: float32 for CPU, float16 for GPU (if supported)
        """
        if self.device.type == "cuda":
            # Check if GPU supports float16
            capability = torch.cuda.get_device_capability(0)
            if capability[0] >= 5:  # Compute capability 5.0+
                return torch.float16
        
        # Default to float32 for CPU and older GPUs
        return torch.float32
    
    def print_summary(self):
        """Print device configuration summary"""
        print("=" * 70)
        print("🖥️  DEVICE CONFIGURATION")
        print("=" * 70)
        print(f"Device Type:     {self.device_info.get('type', 'Unknown')}")
        print(f"Device Name:     {self.device_info.get('name', 'Unknown')}")
        print(f"PyTorch Device:  {self.device}")
        
        if self.device_info.get('type') == 'GPU' and 'total_memory' in self.device_info:
            print(f"Memory:          {self.device_info['total_memory']:.2f} GB")
        
        if 'os' in self.device_info:
            print(f"OS:              {self.device_info['os']}")
        
        print(f"PyTorch:         {self.device_info.get('pytorch_version', 'Unknown')}")
        print("=" * 70)


def detect_device(verbose: bool = True) -> Tuple[torch.device, Dict]:
    """
    Convenience function to detect device
    
    Args:
        verbose: Print device detection information
        
    Returns:
        Tuple of (torch.device, device_info_dict)
    """
    manager = DeviceManager(verbose=verbose)
    return manager.get_device(), manager.get_device_info()


# Test function
if __name__ == "__main__":
    print("\n" + "="*70)
    print("Testing Device Detection")
    print("="*70 + "\n")
    
    manager = DeviceManager(verbose=True)
    manager.print_summary()
    
    print(f"\nDevice: {manager.get_device()}")
    print(f"Pipeline device index: {manager.get_pipeline_device()}")
    print(f"Recommended dtype: {manager.get_dtype()}")
    
    # Show full info
    print("\nFull device info:")
    for key, value in manager.get_device_info().items():
        print(f"  {key}: {value}")
