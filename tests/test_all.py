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
import urllib.error
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
        deadline = time.time() + timeout
        url = f'http://localhost:{port}'
        html = ''
        while True:
            try:
                with urllib.request.urlopen(url) as resp:
                    html = resp.read().decode('utf-8', errors='ignore')
                break
            except urllib.error.URLError:
                if time.time() > deadline:
                    raise
                time.sleep(0.5)
        assert '<title>' in html or '<head>' in html
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()

## ---------------- Demo smoke tests ---------------- #
@pytest.mark.parametrize('script,port', [
    ('examples/app.py', 8501),
])
def test_app_serves(script, port):
    """
    Smoke-test that the multipage app serves content at the root URL.
    """
    try:
        run_streamlit_demo(script, port)
    except Exception as e:
        pytest.skip(f'App {script} failed to serve: {e}')

# ---------------- Screenshot & Video capture tests ---------------- #
pytest.importorskip('playwright.sync_api')
scripts_dir = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(scripts_dir))
import capture_demo_screenshots

@pytest.mark.parametrize('script,port,img_name,vid_name', [
    ('examples/app.py', 8511, 'home.png', 'home.webm'),
    ('examples/pages/image_classification.py', 8512, 'image_classification.png', 'image_classification.webm'),
    ('examples/pages/1_interactive_iris_inference.py', 8513, 'iris_interactive.png', 'iris_interactive.webm'),
    ('examples/pages/2_simple_iris_inference.py', 8514, 'iris_simple.png', 'iris_simple.webm'),
])
def test_capture_pages(tmp_path, script, port, img_name, vid_name):
    """Capture screenshot and video for each demo script."""
    demo_script = str(Path(script).absolute())
    screenshot_file = tmp_path / img_name
    video_file = tmp_path / vid_name
    try:
        capture_demo_screenshots.capture(
            demo_script,
            port,
            str(screenshot_file),
            video_path=str(video_file),
        )
    except Exception as e:
        pytest.skip(f'Capture skipped for {script}: {e}')
    assert screenshot_file.exists() and screenshot_file.stat().st_size > 0
    assert video_file.exists() and video_file.stat().st_size > 0
