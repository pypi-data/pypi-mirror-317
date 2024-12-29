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