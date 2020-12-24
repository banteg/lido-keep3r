import click
from brownie import LidoJob, accounts, chain


def main():
    user = accounts.load(click.prompt("account", type=click.Choice(accounts.load())))
    job = LidoJob.at("0x1EE5C83C4B43aaEd21613D5cc7835D36078ce03F", owner=user)
    for _ in chain.new_blocks():
        if job.workable():
            job.work()
