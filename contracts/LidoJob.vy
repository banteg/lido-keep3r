# @version 0.2.8

interface Keep3r:
    def isKeeper(keeper: address) -> bool: view
    def worked(keeper: address): nonpayable

interface Lido:
    def getBufferedEther() -> uint256: view
    def depositBufferedEther(max_deposits: uint256): nonpayable


keeper: public(Keep3r)
lido: public(Lido)
DEPOSIT_SIZE: constant(uint256) = 32 * 10 ** 18
MIN_DEPOSITS: constant(uint256) = 16
MAX_DEPOSITS: constant(uint256) = 60


@external
def __init__():
    self.keeper = Keep3r(0x1cEB5cB57C4D4E2b2433641b95Dd330A33185A44)
    self.lido = Lido(0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84)


@view
@external
def workable() -> bool:
    return self.lido.getBufferedEther() >= MIN_DEPOSITS * DEPOSIT_SIZE


@external
def work():
    assert self.keeper.isKeeper(msg.sender)  # dev: not keeper
    deposits: uint256 = min(self.lido.getBufferedEther() / DEPOSIT_SIZE, MAX_DEPOSITS)
    assert deposits >= MIN_DEPOSITS  # dev: not workable
    self.lido.depositBufferedEther(deposits)
    self.keeper.worked(msg.sender)
