import click
from brownie import LidoJob, Contract, Wei, accounts, chain


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
