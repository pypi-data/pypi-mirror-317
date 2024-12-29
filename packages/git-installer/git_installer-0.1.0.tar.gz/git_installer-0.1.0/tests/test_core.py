import pytest
from git_installer.core import GitInstaller


def test_check_git_installed():
    # Simulácia testovania dostupnosti Gitu
    assert isinstance(GitInstaller.check_git_installed(), bool)