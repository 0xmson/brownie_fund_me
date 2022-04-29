from brownie import accounts, config, FundMe, network, MockV3Aggregator
from scripts.helpful_script import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIORNMENTS,
)


def deploy_fund_me():
    account = get_account()
    print(account.balance())
    # pass the price feed address to our fundme contract

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIORNMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # .get() - still ok even forget to add verify
    )
    print(f"Contract deployed to {fund_me.address}")
    print(fund_me)
    return fund_me


def main():
    deploy_fund_me()

    # 1.
    #   fund_me = FundMe.deploy(
    #     "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e",
    #     {"from": account}, publish_source=True
    #   )
    #
    #
    # 2.
    #  if network.show_active() != 'development':
    #     price_feed_address = "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e"
    #     fund_me = FundMe.deploy(
    #         price_feed_address,
    #         {"from": account}, publish_source=True
    #     )
    #
    #
    # 3.
    #   if network.show_active() != "development":
    #      price_feed_address = config["networks"][network.show_active()][
    #         "eth_usd_price_feed"
    #     ]
    #   else:
    #      print(f"The active network is {network.show_active()}")
    #      print("Deploying Mocks...")
    #          mock_aggregator = MockV3Aggregator.deploy(
    #              18, Web3.toWei(2000, "ether"), {"from": account}
    #          )
    #      price_feed_address = mock_aggregator.address
    #      print("Mocks Deployed!")
    #
    #      fund_me = FundMe.deploy(
    #          price_feed_address,
    #          {"from": account},
    #          publish_source=config["networks"][network.show_active].get("verify"),  # .get() - still ok even forget to add verify
    #      )

    # brownie networks add Ethereum ganachi-local host=http://127.0.0.1:8545 chainid=1337 (5:38:00)
    # brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='http://mainnet.infura.io/v3/$WEB3_INFURA_PROJECT_ID' accounts=10 mnemonic=brownie port=8545 (6:00:00)
    # brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='https://eth-mainnet.alchemyapi.io/v2/wxjU_m8cmWZtZErMc1X_JDC8w_miR3Jf' accounts=10 mnemonic=brownie port=8545
