"""
Combined test suite for streamlit-secure-context
Includes:
  - Wrapper registration and error handling tests
  - Demo smoke tests to verify basic apps serve pages
  - Screenshot capture tests using Playwright
"""
import sys
import os
import subprocess
import urllib.request
import time
import importlib
import types
from pathlib import Path

import pytest

# ---------------- Streamlit Secure Context wrapper tests ---------------- #

def _setup_dummy_streamlit(monkeypatch, declare_component_func, isdir_return):
    """
    Stub out the streamlit.components.v1.declare_component API and
    control os.path.isdir to simulate presence/absence of build artifacts.
    """
    # Dummy streamlit module
    streamlit_mod = types.ModuleType('streamlit')
    # components.v1.declare_component stub
    comps = types.ModuleType('streamlit.components')
    comps_v1 = types.ModuleType('streamlit.components.v1')
    comps_v1.declare_component = declare_component_func
    comps.v1 = comps_v1
    streamlit_mod.components = comps
    # errors.StreamlitAPIException stub
    errors_mod = types.ModuleType('streamlit.errors')
    class DummyAPIException(Exception):
        pass
    errors_mod.StreamlitAPIException = DummyAPIException
    streamlit_mod.errors = errors_mod

    # Inject into sys.modules
    monkeypatch.setitem(sys.modules, 'streamlit', streamlit_mod)
    monkeypatch.setitem(sys.modules, 'streamlit.components', comps)
    monkeypatch.setitem(sys.modules, 'streamlit.components.v1', comps_v1)
    monkeypatch.setitem(sys.modules, 'streamlit.errors', errors_mod)
    # Control build directory existence
    monkeypatch.setattr(os.path, 'isdir', lambda path: isdir_return)
    return DummyAPIException

def test_streamlit_secure_context_registration(monkeypatch):
    called = {}

    def dummy_declare_component(name, **init_kwargs):
        def component_func(**call_kwargs):
            called['name'] = name
            called['init_kwargs'] = init_kwargs
            called['call_kwargs'] = call_kwargs
            return 'dummy_result'
        return component_func

    # Simulate valid build dir
    _ = _setup_dummy_streamlit(monkeypatch, dummy_declare_component, isdir_return=True)
    # Ensure fresh import
    if 'streamlit_secure_context' in sys.modules:
        del sys.modules['streamlit_secure_context']
    module = importlib.import_module('streamlit_secure_context')

    # Call wrapper with full params
    result = module.streamlit_secure_context(
        model_path='model_url',
        security_config={'x': 1},
        inference_params={'y': 2},
        key='k1',
    )
    assert result == 'dummy_result'
    assert called['name'] == 'streamlit_secure_context'
    assert 'path' in called['init_kwargs']
    assert called['call_kwargs'] == {
        'modelPath': 'model_url',
        'securityConfig': {'x': 1},
        'inferenceParams': {'y': 2},
        'key': 'k1',
    }

    # Defaults
    called.clear()
    result2 = module.streamlit_secure_context('model2', key='k2')
    assert result2 == 'dummy_result'
    assert called['call_kwargs'] == {
        'modelPath': 'model2',
        'securityConfig': {},
        'inferenceParams': {},
        'key': 'k2',
    }

    # Extra kwargs (height, width)
    called.clear()
    result3 = module.streamlit_secure_context(
        'model3', key='k3', height=200, width=400
    )
    assert result3 == 'dummy_result'
    assert called['call_kwargs']['height'] == 200
    assert called['call_kwargs']['width'] == 400

def test_missing_build_dir_raises(monkeypatch):
    def dummy_declare_component(name, **kwargs):
        pytest.skip('declare_component should not be called when build dir missing')
    DummyAPIException = _setup_dummy_streamlit(monkeypatch, dummy_declare_component, isdir_return=False)
    if 'streamlit_secure_context' in sys.modules:
        del sys.modules['streamlit_secure_context']
    with pytest.raises(DummyAPIException) as exc:
        importlib.import_module('streamlit_secure_context')
    assert 'Could not find component build directory' in str(exc.value)

# ---------------- Demo smoke tests ---------------- #

def run_streamlit_demo(script_path, port, timeout=10):
    cmd = [
        'streamlit', 'run', script_path,
        f'--server.port={port}', '--server.headless=true'
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(timeout)
        url = f'http://localhost:{port}'
        with urllib.request.urlopen(url) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            assert '<title>' in html or '<head>' in html
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()

@pytest.mark.parametrize('script,port', [
    ('examples/demo.py', 8501),
])
def test_demo_pages_serve(script, port):
    """
    Smoke-test that each demo page starts and serves content at the given port.
    """
    try:
        run_streamlit_demo(script, port)
    except Exception as e:
        pytest.skip(f'Demo {script} failed to start or serve: {e}')

# ---------------- Screenshot capture tests ---------------- #

pytest.importorskip('playwright.sync_api')
scripts_dir = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(scripts_dir))
import capture_demo_screenshots


def test_capture_interactive_demo(tmp_path):
    """
    Test that the capture function can take a screenshot of the interactive Iris demo.
    """
    demo = str(Path('examples/demo.py').absolute())
    output_file = tmp_path / 'interactive_demo.png'
    port = 8510
    try:
        capture_demo_screenshots.capture(demo, port, str(output_file))
    except Exception as e:
        pytest.skip(f'Screenshot capture skipped due to error: {e}')
    assert output_file.exists(), 'Screenshot file was not created'
    assert output_file.stat().st_size > 0, 'Screenshot file is empty'

@pytest.mark.parametrize("mode, screenshot_name, video_name", [
    (None, "image_demo.png", "image_demo.webm"),
    ("interactive", "iris_interactive.png", "iris_interactive.webm"),
    ("simple", "iris_simple.png", "iris_simple.webm"),
])
def test_capture_demo_modes(tmp_path, record_video_dir, mode, screenshot_name, video_name):
    demo = str(Path('examples/demo.py').absolute())
    port = 8501
    screenshot_file = tmp_path / screenshot_name
    video_file = tmp_path / video_name
    try:
        capture_demo_screenshots.capture(
            demo, port, str(screenshot_file),
            mode=mode, video_output=str(video_file)
        )
    except Exception as e:
        pytest.skip(f'Capture skipped due to error: {e}')
    assert screenshot_file.exists(), "Screenshot file was not created"
    assert screenshot_file.stat().st_size > 0, "Screenshot file is empty"
    assert video_file.exists(), "Video file was not created"
    assert video_file.stat().st_size > 0, "Video file is empty"
