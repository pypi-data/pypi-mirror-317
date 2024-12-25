import pytest
from mm_btc.cli.cmd.mnemonic_cmd import get_derivation_path_prefix
from mm_std import run_command


def test_get_derivation_path_prefix():
    assert get_derivation_path_prefix("m/11'/0'/0'/0", testnet=True) == "m/11'/0'/0'/0"
    assert get_derivation_path_prefix("bip44", False) == "m/44'/0'/0'/0"
    assert get_derivation_path_prefix("bip44", True) == "m/44'/1'/0'/0"
    assert get_derivation_path_prefix("bip84", False) == "m/84'/0'/0'/0"
    assert get_derivation_path_prefix("bip84", True) == "m/84'/1'/0'/0"

    with pytest.raises(ValueError):
        get_derivation_path_prefix("bip", True)


def test_mnemonic_cmd(mnemonic, passphrase):
    cmd = f"mm-btc mnemonic -m '{mnemonic}' --passphrase '{passphrase}'"
    res = run_command(cmd)
    assert res.code == 0
    assert "m/44'/0'/0'/0/7 1AJNF13C4xVvduE3D9pdtdDNFbL5Bm7T3u L3QF5FHUtX2a1ucGgVfrdhdvLHBSxsRQoGsv7tyY8P5Jt7UV9LZv"
