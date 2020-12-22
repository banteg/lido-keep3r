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
DEPOSITS_PER_CALL: constant(uint256) = 16


@external
def __init__():
    self.keeper = Keep3r(0x1cEB5cB57C4D4E2b2433641b95Dd330A33185A44)
    self.lido = Lido(0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84)


@view
@internal
def _workable() -> bool:
    return self.lido.getBufferedEther() >= DEPOSITS_PER_CALL * DEPOSIT_SIZE


@view
@external
def workable() -> bool:
    return self._workable()


@external
def work():
    assert self.keeper.isKeeper(msg.sender)  # dev: not keeper
    assert self._workable()  # dev: not workable
    self.lido.depositBufferedEther(DEPOSITS_PER_CALL)
    self.keeper.worked(msg.sender)
