
# ==================================================
# File: __init__.py
# ==================================================


# ==================================================
# File: conftest.py
# ==================================================
# conftest.py

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch


def pytest_configure(config):
    """Configure test environment"""
    # Set up CI mode if TEST_MODE environment variable is set to 'ci'
    pytest.is_ci = os.environ.get('TEST_MODE') == 'ci'

@pytest.fixture
def temp_home():
    """Fixture to provide a temporary home directory"""
    original_home = os.environ.get('HOME')
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ['HOME'] = temp_dir
        yield Path(temp_dir)
        if original_home:
            os.environ['HOME'] = original_home

@pytest.fixture
def mock_provider_cache(temp_home):
    """Fixture to provide a clean provider cache"""
    from quickquestion.cache import ProviderCache
    cache = ProviderCache()
    cache.clear()
    return cache

# Modified AsyncContextManagerMock with proper sync/async support
class AsyncContextManagerMock:
    """Mock for async context managers"""
    def __init__(self):
        self.status = 200
        self.headers = {}
        self._response_data = {
            "choices": [{"message": {"content": '["test command 1", "test command 2", "test command 3"]'}}],
            "models": [{"id": "test-model-1"}, {"id": "test-model-2"}],
            "data": [{"id": "test-model"}]
        }

    # Sync context manager methods
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    # Async context manager methods
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    # Methods that can be both sync and async
    def json(self):
        return self._response_data

    async def ajson(self):
        return self._response_data

    def text(self):
        return '{"status": "ok"}'

    async def atext(self):
        return '{"status": "ok"}'

    def raise_for_status(self):
        if self.status >= 400:
            raise Exception(f"HTTP {self.status}")

class AsyncClientSessionMock:
    """Mock for aiohttp.ClientSession with both sync and async support"""
    def __init__(self, *args, **kwargs):
        self.response = AsyncContextManagerMock()
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def get(self, *args, **kwargs):
        return self.response

    async def aget(self, *args, **kwargs):
        return self.response

    def post(self, *args, **kwargs):
        return self.response

    async def apost(self, *args, **kwargs):
        return self.response

@pytest.fixture
def mock_api_clients(monkeypatch):
    """Mock API clients for both sync and async use"""
    if not pytest.is_ci:
        yield
        return

    # Mock response data
    mock_response_data = {
        "choices": [{"message": {"content": '["test command 1", "test command 2", "test command 3"]'}}],
        "models": [{"id": "test-model-1"}, {"id": "test-model-2"}],
        "data": [{"id": "test-model"}]
    }

    # Mock synchronous requests
    mock_response = Mock()
    mock_response.status_code = 200
    # Set headers as a real dict instead of Mock
    mock_response.headers = {
        "content-type": "application/json",
        "server": "test-server"
    }
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status.return_value = None

    import requests
    monkeypatch.setattr(requests, 'post', Mock(return_value=mock_response))
    monkeypatch.setattr(requests, 'get', Mock(return_value=mock_response))

    # Create session mock instance
    session_mock = AsyncClientSessionMock()

    # Mock asynchronous aiohttp
    import aiohttp
    monkeypatch.setattr(aiohttp, 'ClientSession', lambda *args, **kwargs: session_mock)

    yield session_mock

@pytest.fixture(autouse=True)
def auto_mock_api_clients(mock_api_clients):
    """Automatically apply API client mocks"""
    pass

@pytest.fixture
def mock_provider():
    """Fixture to provide a mock LLM provider"""
    provider = Mock()
    provider.get_available_models.return_value = ["test-model"]
    provider.check_status.return_value = True
    provider.current_model = "test-model"
    provider.generate_response.return_value = ["test command 1", "test command 2", "test command 3"]
    return provider

# ==================================================
# File: test_cache.py
# ==================================================
# tests/test_cache.py
import pytest
from pathlib import Path
from quickquestion.cache import ProviderCache


def test_cache_singleton():
    """Test that ProviderCache is a singleton"""
    cache1 = ProviderCache()
    cache2 = ProviderCache()
    assert cache1 is cache2


def test_cache_operations():
    """Test basic cache operations"""
    cache = ProviderCache()
    
    # Test setting and getting
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"
    
    # Test non-existent key
    assert cache.get("nonexistent") is None
    
    # Test clearing
    cache.clear()
    assert cache.get("test_key") is None


def test_cache_ttl():
    """Test time-to-live functionality"""
    cache = ProviderCache()
    import time
    
    # Set with default TTL (30 seconds)
    cache.set("quick_expire", "value")
    assert cache.get("quick_expire") == "value"
    
    # Set with providers TTL (1 hour)
    cache.set("providers_test", "value")
    assert cache.get("providers_test") == "value"


def test_cache_info():
    """Test cache info retrieval"""
    cache = ProviderCache()
    cache.set("test_key", "test_value")
    
    info = cache.get_cache_info()
    assert "test_key" in info
    assert "age_seconds" in info["test_key"]
    assert "expires_in_seconds" in info["test_key"]
    assert "ttl" in info["test_key"]

# ==================================================
# File: test_providers.py
# ==================================================
# tests/test_providers.py
import pytest
from quickquestion.llm_provider import (
    LMStudioProvider,
    OllamaProvider,
    OpenAIProvider,
    AnthropicProvider,
    GroqProvider,
    GrokProvider
)


def test_provider_initialization():
    """Test that providers can be initialized"""
    providers = [
        LMStudioProvider(),
        OllamaProvider(),
        OpenAIProvider(),
        AnthropicProvider(),
        GroqProvider(),
        GrokProvider()
    ]
    for provider in providers:
        assert provider is not None
        assert hasattr(provider, 'debug')


def test_provider_model_selection():
    """Test model selection logic"""
    provider = LMStudioProvider()
    test_models = ["mistral-7b", "llama2-7b", "neural-chat-7b", "unknown-model"]
    selected = provider.select_best_model(test_models)
    assert selected == "mistral-7b"  # Should select mistral as it's first in PREFERRED_MODELS


def test_empty_model_list():
    """Test behavior with empty model list"""
    provider = LMStudioProvider()
    selected = provider.select_best_model([])
    assert selected is None


def test_parse_llm_response():
    """Test response parsing"""
    provider = LMStudioProvider()
    
    # Test JSON array response
    json_response = '["command1", "command2", "command3"]'
    parsed = provider._parse_llm_response(json_response)
    assert len(parsed) == 3
    assert parsed == ["command1", "command2", "command3"]
    
    # Test markdown wrapped response
    markdown_response = '```json\n["command1", "command2"]\n```'
    parsed = provider._parse_llm_response(markdown_response)
    assert len(parsed) == 2
    assert parsed == ["command1", "command2"]

# ==================================================
# File: test_qq.py
# ==================================================
# tests/test_qq.py

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
from quickquestion.qq import QuickQuestion
from quickquestion.ui_library import UIOptionDisplay
import subprocess


@pytest.fixture
def mock_ui():
    """Mock UI components"""
    with patch('quickquestion.qq.UIOptionDisplay') as mock_ui:
        ui_instance = Mock()
        mock_ui.return_value = ui_instance
        yield ui_instance


@pytest.fixture
def mock_clipboard():
    """Mock clipboard operations"""
    with patch('quickquestion.qq.copy_to_clipboard') as mock_copy:
        yield mock_copy


@pytest.fixture
def qq_instance(temp_home, mock_provider_cache):
    """Create a QuickQuestion instance with mocked components"""
    settings = {
        "default_provider": "LM Studio",
        "command_action": "Run Command",
        "default_model": "test-model"
    }
    with patch('quickquestion.qq.get_settings', return_value=settings):
        qq = QuickQuestion(debug=True, settings=settings)
        yield qq


def test_display_suggestions_basic(qq_instance, mock_ui):
    """Test basic command suggestion display"""
    # Setup mock UI responses
    mock_ui.display_options.return_value = (0, 'select')  # Select first option
    
    suggestions = ["find . -type f -size +100M", "du -sh * | sort -hr", "ls -lS"]
    question = "how to find large files"
    
    # Execute display_suggestions
    qq_instance.display_suggestions(suggestions, question)
    
    # Verify UI interactions
    mock_ui.display_banner.assert_called_once()
    mock_ui.display_options.assert_called_once()
    
    # Verify header panels were created correctly
    call_args = mock_ui.display_options.call_args[1]
    header_panels = call_args.get('header_panels', [])
    assert len(header_panels) == 2
    assert "Provider Info" in header_panels[0]['title']
    assert question in header_panels[1]['content']


def test_display_suggestions_copy_command(qq_instance, mock_ui, mock_clipboard):
    """Test copy command functionality"""
    # Setup settings for copy command
    qq_instance.settings['command_action'] = 'Copy Command'
    
    # Setup mock UI responses
    mock_ui.display_options.return_value = (0, 'select')  # Select first option
    
    suggestions = ["find . -type f -size +100M"]
    
    # Execute display_suggestions and expect SystemExit
    with pytest.raises(SystemExit) as exc_info:
        qq_instance.display_suggestions(suggestions, "test")
    
    # Verify exit was successful (code 0)
    assert exc_info.value.code == 0
    
    # Verify clipboard operation
    mock_clipboard.assert_called_once_with(suggestions[0])
    
    # Verify success message
    mock_ui.display_message.assert_called_once()
    assert "copied to clipboard" in mock_ui.display_message.call_args[0][0].lower()


def test_banner_display(qq_instance, mock_ui):
    """Test banner display formatting"""
    qq_instance.print_banner()
    
    mock_ui.display_banner.assert_called_once()
    call_args = mock_ui.display_banner.call_args[0]  # Get positional arguments
    
    # Verify banner content (first arg should be title)
    assert "Quick Question" in call_args[0]
    
    # Check keyword arguments for subtitle and website
    kwargs = mock_ui.display_banner.call_args[1]
    assert 'subtitle' in kwargs
    assert 'website' in kwargs
    
    # Verify subtitle content
    subtitle = kwargs['subtitle']
    assert any("Provider:" in line for line in subtitle)
    assert any("Command Action:" in line for line in subtitle)
    
    # Verify website
    assert "southbrucke.com" in kwargs['website'].lower()


def test_get_command_suggestions(qq_instance, mock_ui):
    """Test command suggestion generation"""
    with patch.object(qq_instance, 'print_banner'), \
         patch.object(qq_instance.provider, 'generate_response', 
                     return_value=["cmd1", "cmd2", "cmd3"]):
        
        suggestions = qq_instance.get_command_suggestions("test question")
        
        # Verify suggestions format
        assert isinstance(suggestions, list)
        assert len(suggestions) == 3
        assert all(isinstance(cmd, str) for cmd in suggestions)

def test_display_suggestions_execute_command(qq_instance, mock_ui):
    """Test command execution"""
    # Setup mock UI responses
    mock_ui.display_options.return_value = (0, 'select')  # Select first option
    
    with patch('subprocess.run') as mock_run:
        suggestions = ["echo 'test'"]
        qq_instance.display_suggestions(suggestions, "test")
        
        # Verify command execution
        mock_run.assert_called_once_with(suggestions[0], shell=True)


def test_display_suggestions_navigation(qq_instance, mock_ui):
    """Test navigation through suggestions"""
    suggestions = ["cmd1", "cmd2", "cmd3"]
    
    # Simulate different navigation scenarios
    navigation_scenarios = [
        (0, 'quit'),    # Test quit
        (1, 'select'),  # Test selecting second option
        (2, 'cancel')   # Test cancel
    ]
    
    for selected, action in navigation_scenarios:
        mock_ui.display_options.return_value = (selected, action)
        
        with pytest.raises(SystemExit) if action in ('quit', 'cancel') else patch('subprocess.run'):
            qq_instance.display_suggestions(suggestions, "test")


def test_display_suggestions_cloud_provider(qq_instance, mock_ui):
    """Test display with cloud provider"""
    # Mock cloud provider
    with patch.object(qq_instance, 'is_cloud_provider', return_value=True):
        mock_ui.display_options.return_value = (0, 'quit')
        
        suggestions = ["test command"]
        
        with pytest.raises(SystemExit):
            qq_instance.display_suggestions(suggestions, "test")
        
        # Verify cloud provider indication
        call_args = mock_ui.display_options.call_args[1]
        header_panels = call_args.get('header_panels', [])
        provider_info = header_panels[0]['content']
        assert "Cloud Based Provider" in provider_info
        assert "[red]" in provider_info


def test_display_suggestions_error_handling(qq_instance, mock_ui, mock_clipboard):
    """Test error handling in suggestions display"""
    # Test clipboard error
    qq_instance.settings['command_action'] = 'Copy Command'
    mock_clipboard.side_effect = Exception("Clipboard error")
    mock_ui.display_options.return_value = (0, 'select')
    
    suggestions = ["test command"]
    
    with pytest.raises(SystemExit) as exc_info:
        qq_instance.display_suggestions(suggestions, "test")
    
    # Verify error message
    mock_ui.display_message.assert_called_once()
    error_message = mock_ui.display_message.call_args[0][0]
    assert "error" in error_message.lower()
    assert exc_info.value.code == 1

def test_command_history_integration(qq_instance, mock_ui, temp_home):
    """Test command history integration"""
    mock_ui.display_options.return_value = (0, 'select')
    
    suggestions = ["test command"]
    question = "test question"
    
    # Execute a command
    with patch('subprocess.run'):
        qq_instance.display_suggestions(suggestions, question)
    
    # Verify command was saved to history
    history_file = temp_home / '.qq_history.json'
    assert history_file.exists()
    
    import json
    with open(history_file) as f:
        history = json.load(f)
        assert len(history) > 0
        assert history[-1]['command'] == suggestions[0]
        assert history[-1]['question'] == question

# ==================================================
# File: test_utils.py
# ==================================================
# tests/test_utils.py
import pytest
from quickquestion.utils import clear_screen, enable_debug_printing, disable_debug_printing


def test_debug_printing():
    """Test debug printing functions"""
    # Test enabling debug printing
    enable_debug_printing()
    
    # Test disabling debug printing
    disable_debug_printing()
    
    # Verify no errors occur
    assert True


def test_clear_screen():
    """Test clear screen functionality"""
    # Just verify it doesn't raise an exception
    try:
        clear_screen()
        assert True
    except Exception as e:
        pytest.fail(f"clear_screen raised an exception: {e}")