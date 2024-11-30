import pytest
from unittest.mock import MagicMock
import pygame

@pytest.fixture(autouse=True)
def mock_pygame(monkeypatch):
    monkeypatch.setattr(pygame.display, "flip", MagicMock())
    monkeypatch.setattr(pygame.display, "update", MagicMock())
