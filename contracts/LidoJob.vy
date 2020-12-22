# @version 0.2.8

interface Keep3r:
    def isKeeper(keeper: address) -> bool: view
    def worked(keeper: address): nonpayable

interface Lido:
    def isStopped() -> bool: view
    def getBufferedEther() -> uint256: view
    def depositBufferedEther(max_deposits: uint256): nonpayable


keeper: public(Keep3r)
lido: public(Lido)
DEPOSIT_SIZE: constant(uint256) = 32 * 10 ** 18
MIN_DEPOSITS: constant(uint256) = 16
MAX_DEPOSITS: constant(uint256) = 60
DAO_TIMEOUT: constant(uint256) = 60*60*24
last_key_shortage: public(uint256)


@external
def __init__():
    self.keeper = Keep3r(0x1cEB5cB57C4D4E2b2433641b95Dd330A33185A44)
    self.lido = Lido(0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84)
    last_key_shortage = 0


@view
@internal
def available_deposits() -> uint256:
    if self.lido.isStopped():
        return 0
    if block.timestamp < self.last_key_shortage + 60*60*24:
        return 0
    return min(self.lido.getBufferedEther() / DEPOSIT_SIZE, MAX_DEPOSITS)


@view
@external
def workable() -> bool:
    return self.available_deposits() >= MIN_DEPOSITS


@external
def work():
    assert self.keeper.isKeeper(msg.sender)  # dev: not keeper
    deposits: uint256 = self.available_deposits()
    assert deposits >= MIN_DEPOSITS  # dev: not workable
    buffered: uint256 = self.lido.getBufferedEther()
    self.lido.depositBufferedEther(deposits)
    deposited: uint256 = buffered - self.lido.getBufferedEther()
    if deposited < (deposits * DEPOSIT_SIZE):
        self.last_key_shortage = block.timestamp
     
    self.keeper.worked(msg.sender)
