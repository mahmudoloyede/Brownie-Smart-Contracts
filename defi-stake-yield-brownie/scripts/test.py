from scripts.deploy import deploy_token_farm_and_dapp_token


def main():
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    print(token_farm.tokenIsAllowed(dapp_token.address))
