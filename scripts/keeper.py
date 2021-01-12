import click
from brownie import LidoJob, Contract, Wei, accounts, chain, network
from brownie.network.gas.strategies import GasNowScalingStrategy

network.gas_price(GasNowScalingStrategy())


def get_account():
    return accounts.load(click.prompt("account", type=click.Choice(accounts.load())))


def get_job(user=None):
    return LidoJob.at("0x1EE5C83C4B43aaEd21613D5cc7835D36078ce03F", owner=user)


def main():
    user = get_account()
    job = get_job(user)
    for _ in chain.new_blocks():
        if job.workable():
            job.work()


def add_credit():
    user = get_account()
    job = get_job(user)
    keep3r = Contract("0x1cEB5cB57C4D4E2b2433641b95Dd330A33185A44", owner=user)
    job = LidoJob.at("0x1EE5C83C4B43aaEd21613D5cc7835D36078ce03F", owner=user)

    print("job credits:", keep3r.credits(job, keep3r).to("ether"))
    print("kp3r balance:", keep3r.balanceOf(user).to("ether"))
    amount = click.prompt("top up amount")
    amount = min(keep3r.balanceOf(user), Wei(f"{amount} ether"))
    assert amount > 0, "cannot top up zero amount"

    print("topping up with", amount.to("ether"), "k3pr")
    if keep3r.allowance(user, keep3r) < amount:
        keep3r.approve(keep3r, 2 ** 256 - 1)
    keep3r.addCredit(keep3r, job, amount)
    print("job credits:", keep3r.credits(job, keep3r).to("ether"))


def add_lp_credit():
    """
    1. run to add liquidity to job
    2. wait 3 days
    3. run again to apply credit to job
    """
    user = get_account()
    job = get_job(user)
    keep3r = Contract("0x1cEB5cB57C4D4E2b2433641b95Dd330A33185A44", owner=user)
    lp = Contract("0x79e0d4858af8071349469b6589a3c23c1fe1586e", owner=user)

    click.secho(f"job credits: {keep3r.credits(job, keep3r).to('ether')}", fg="green")
    assert keep3r.liquidityAccepted(lp), "liquidity not accepted"

    bonded = keep3r.liquidityApplied(user, lp, job)
    now = chain[-1].timestamp
    if bonded > 0:
        when = f"in {bonded - now}s" if now < bonded else "now"
        click.secho(f"found bonded liquidity, it can be finalized {when}", fg="yellow")
        if bonded < now:
            keep3r.applyCreditToJob(user, lp, job)
            click.secho(
                f"job credits: {keep3r.credits(job, keep3r).to('ether')}", fg="green"
            )
        return

    print("sushi ldo/kp3r lp balance:", lp.balanceOf(user).to("ether"))
    amount = click.prompt("top up amount", default=lp.balanceOf(user).to("ether"))
    amount = Wei(f"{amount} ether")

    if lp.allowance(user, keep3r) < amount:
        lp.approve(keep3r, 2 ** 256 - 1)

    keep3r.addLiquidityToJob(lp, job, amount)
