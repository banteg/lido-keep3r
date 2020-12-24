import pytest


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture()
def user(accounts):
    return accounts[0]


@pytest.fixture()
def kpr(Contract, accounts):
    kpr = Contract("0x1ceb5cb57c4d4e2b2433641b95dd330a33185a44")
    gov = accounts.at(kpr.governance(), force=True)
    return Contract(kpr, owner=gov)


@pytest.fixture()
def keeper(kpr, accounts):
    return accounts.at(kpr.keeperList(0), force=True)


@pytest.fixture()
def kpr_whale(accounts):
    return accounts.at("0xF7Aa325404f81cf34268657DdF2d046763a8C4Ed", force=True)


@pytest.fixture()
def lido(Contract):
    return Contract("0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84")


@pytest.fixture()
def job(LidoJob, user):
    return LidoJob.deploy({"from": user})
