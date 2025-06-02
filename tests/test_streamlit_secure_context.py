import sys
import os
import importlib
import types
import pytest


def _setup_dummy_streamlit(monkeypatch, declare_component_func, isdir_return):
    """
    Insert dummy streamlit modules into sys.modules and patch os.path.isdir.
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
    # Use a simple Exception subclass for testing
    class DummyAPIException(Exception):
        pass
    errors_mod.StreamlitAPIException = DummyAPIException
    streamlit_mod.errors = errors_mod

    # Monkey-patch sys.modules
    monkeypatch.setitem(sys.modules, 'streamlit', streamlit_mod)
    monkeypatch.setitem(sys.modules, 'streamlit.components', comps)
    monkeypatch.setitem(sys.modules, 'streamlit.components.v1', comps_v1)
    monkeypatch.setitem(sys.modules, 'streamlit.errors', errors_mod)

    # Monkey-patch os.path.isdir
    monkeypatch.setattr(os.path, 'isdir', lambda path: isdir_return)
    return DummyAPIException


def test_streamlit_secure_context_registration(monkeypatch):
    # Capture calls to declare_component and the resulting component function
    called = {}

    def dummy_declare_component(name, **init_kwargs):
        # Return a dummy component function that records invocation
        def component_func(**call_kwargs):
            called['name'] = name
            called['init_kwargs'] = init_kwargs
            called['call_kwargs'] = call_kwargs
            return 'dummy_result'
        return component_func

    # Setup dummy streamlit and pretend build dir exists
    _ = _setup_dummy_streamlit(monkeypatch, dummy_declare_component, isdir_return=True)

    # Ensure fresh import of the component module
    if 'streamlit_secure_context' in sys.modules:
        del sys.modules['streamlit_secure_context']
    # Import after stubbing
    module = importlib.import_module('streamlit_secure_context')
    # The wrapper function should be available
    assert hasattr(module, 'streamlit_secure_context')

    # Call the component wrapper with explicit params
    result = module.streamlit_secure_context(
        model_path='model_url',
        security_config={'x': 1},
        inference_params={'y': 2},
        key='k1',
    )
    # Should return our dummy value
    assert result == 'dummy_result'
    # Verify component registration
    assert called['name'] == 'streamlit_secure_context'
    # init_kwargs should include a path key
    assert 'path' in called['init_kwargs']
    # Verify call arguments forwarded correctly
    assert called['call_kwargs'] == {
        'modelPath': 'model_url',
        'securityConfig': {'x': 1},
        'inferenceParams': {'y': 2},
        'key': 'k1',
    }

    # Test defaults: security_config/inference_params default to empty dict
    called.clear()
    result2 = module.streamlit_secure_context('model2', key='k2')
    assert result2 == 'dummy_result'
    assert called['call_kwargs'] == {
        'modelPath': 'model2',
        'securityConfig': {},
        'inferenceParams': {},
        'key': 'k2',
    }


def test_missing_build_dir_raises(monkeypatch):
    # Stub declare_component but it should not be reached
    def dummy_declare_component(name, **kwargs):
        pytest.skip('declare_component should not be called when build dir missing')

    # Setup dummy streamlit and pretend build dir does NOT exist
    DummyAPIException = _setup_dummy_streamlit(monkeypatch, dummy_declare_component, isdir_return=False)

    # Remove module if already imported
    if 'streamlit_secure_context' in sys.modules:
        del sys.modules['streamlit_secure_context']
    # Importing should now raise our DummyAPIException
    with pytest.raises(DummyAPIException) as excinfo:
        importlib.import_module('streamlit_secure_context')
    # Error message should guide user to build frontend
    msg = str(excinfo.value)
    assert 'Could not find component build directory' in msg