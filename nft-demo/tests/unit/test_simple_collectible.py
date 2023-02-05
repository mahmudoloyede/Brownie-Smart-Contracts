from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network
from scripts.simple_collectible.deploy_and_create import deploy_and_create
import pytest


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    simple_collectibles = deploy_and_create()
    assert simple_collectibles.ownerOf(0) == get_account()
