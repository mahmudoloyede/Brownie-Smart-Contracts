from scripts.helpful_scripts import get_breed, get_account, OPENSEA_URL
from brownie import network, AdvancedCollectible


dog_metadata_dic = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def main():
    print(f"working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    numeber_of_collectibles = advanced_collectible.tokenCounter()
    print(f"you have {numeber_of_collectibles} tokenIds")
    for tokenId in range(numeber_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(tokenId))
        if not advanced_collectible.tokenURI(tokenId).startswith("https://"):
            print("Setting")
            set_tokenURI(tokenId, advanced_collectible, dog_metadata_dic[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(OPENSEA_URL.format(nft_contract.address, token_id))
