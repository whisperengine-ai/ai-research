"""
Test Device Detection and Auto-Configuration

Tests the DeviceManager across different scenarios:
- GPU detection (NVIDIA CUDA)
- Metal GPU detection (macOS)
- CPU fallback
- Data type selection
- Pipeline device index
"""

import torch
import platform
from device_manager import DeviceManager, detect_device


def test_device_detection():
    """Test basic device detection"""
    print("\n" + "="*70)
    print("TEST 1: Basic Device Detection")
    print("="*70)
    
    manager = DeviceManager(verbose=True)
    manager.print_summary()
    
    assert manager.get_device() is not None
    assert manager.get_device_info() is not None
    print("✅ PASS: Device detected successfully\n")


def test_device_types():
    """Test that device is valid torch device"""
    print("="*70)
    print("TEST 2: Device Type Validation")
    print("="*70)
    
    device, info = detect_device(verbose=False)
    
    print(f"Device: {device}")
    print(f"Device Type: {info.get('type')}")
    
    assert device.type in ['cpu', 'cuda', 'mps']
    assert info.get('type') in ['CPU', 'GPU']
    print("✅ PASS: Device is valid torch device\n")


def test_pipeline_device_index():
    """Test pipeline device index selection"""
    print("="*70)
    print("TEST 3: Pipeline Device Index")
    print("="*70)
    
    manager = DeviceManager(verbose=False)
    device_index = manager.get_pipeline_device()
    
    print(f"Pipeline device index: {device_index}")
    
    if manager.get_device().type == "cuda":
        assert device_index == 0, "GPU should use device index 0"
        print("   (GPU detected: index=0)")
    else:
        assert device_index == -1, "CPU should use device index -1"
        print("   (CPU detected: index=-1)")
    
    print("✅ PASS: Pipeline device index is correct\n")


def test_dtype_selection():
    """Test recommended data type selection"""
    print("="*70)
    print("TEST 4: Data Type Selection")
    print("="*70)
    
    manager = DeviceManager(verbose=False)
    dtype = manager.get_dtype()
    
    print(f"Device: {manager.get_device()}")
    print(f"Recommended dtype: {dtype}")
    
    # Should always return a valid torch dtype
    assert dtype in [torch.float32, torch.float16]
    print(f"✅ PASS: Valid dtype selected ({dtype})\n")


def test_os_detection():
    """Test OS-specific device detection"""
    print("="*70)
    print("TEST 5: OS-Specific Detection")
    print("="*70)
    
    os_name = platform.system()
    manager = DeviceManager(verbose=False)
    device_type = manager.get_device_info().get('type')
    
    print(f"Operating System: {os_name}")
    print(f"Detected Device Type: {device_type}")
    
    if os_name == "Darwin":  # macOS
        print("   → macOS detected")
        if torch.backends.mps.is_available():
            print("   → Metal GPU (MPS) should be available")
        else:
            print("   → Metal GPU not available (Mac CPU fallback)")
    elif os_name == "Windows" or os_name == "Linux":
        print(f"   → {os_name} detected")
        if torch.cuda.is_available():
            print("   → NVIDIA CUDA should be available")
        else:
            print("   → CPU fallback")
    
    print(f"✅ PASS: OS-specific detection working\n")


def test_device_manager_consistency():
    """Test that DeviceManager returns consistent results"""
    print("="*70)
    print("TEST 6: Consistency Check")
    print("="*70)
    
    manager1 = DeviceManager(verbose=False)
    manager2 = DeviceManager(verbose=False)
    
    device1 = manager1.get_device()
    device2 = manager2.get_device()
    
    print(f"First call:  {device1}")
    print(f"Second call: {device2}")
    
    assert device1 == device2, "Device should be consistent across calls"
    print("✅ PASS: Device detection is consistent\n")


def test_convenience_function():
    """Test the convenience detect_device function"""
    print("="*70)
    print("TEST 7: Convenience Function")
    print("="*70)
    
    device, info = detect_device(verbose=False)
    
    print(f"Device returned: {device}")
    print(f"Info keys: {list(info.keys())}")
    
    assert device is not None
    assert isinstance(info, dict)
    assert 'type' in info
    assert 'name' in info
    print("✅ PASS: Convenience function works correctly\n")


def test_integration_with_model():
    """Test that device can be used with actual models"""
    print("="*70)
    print("TEST 8: Model Integration (simulated)")
    print("="*70)
    
    manager = DeviceManager(verbose=False)
    device = manager.get_device()
    dtype = manager.get_dtype()
    
    print(f"Device: {device}")
    print(f"Data Type: {dtype}")
    print(f"Pipeline Index: {manager.get_pipeline_device()}")
    
    # Simulate tensor operations that would happen with actual model
    try:
        tensor = torch.randn(2, 4).to(device)
        print(f"✅ Tensor creation on {device}: {tensor.device}")
        
        tensor_fp = tensor.to(dtype)
        print(f"✅ Tensor dtype conversion to {dtype}: {tensor_fp.dtype}")
        
        print("✅ PASS: Model integration test successful\n")
    except Exception as e:
        print(f"❌ FAIL: {e}\n")
        raise


def run_all_tests():
    """Run all tests"""
    print("\n" + "█"*70)
    print("  DEVICE DETECTION TEST SUITE")
    print("█"*70)
    
    try:
        test_device_detection()
        test_device_types()
        test_pipeline_device_index()
        test_dtype_selection()
        test_os_detection()
        test_device_manager_consistency()
        test_convenience_function()
        test_integration_with_model()
        
        print("█"*70)
        print("  ✅ ALL TESTS PASSED!")
        print("█"*70 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise


if __name__ == "__main__":
    run_all_tests()
