from brownie import Wei


def test_job(kpr, lido, job, kpr_whale, user, keeper):
    target = Wei("2500 ether")
    buffered = lido.getBufferedEther()
    if buffered < target:
        lido.submit(lido, {"from": user, "amount": target - buffered})
    buffered = lido.getBufferedEther()
    kpr.addJob(job)
    kpr.approve(kpr, "100 ether", {"from": kpr_whale})
    kpr.addCredit(kpr, job, "100 ether", {"from": kpr_whale})
    credits = kpr.credits(job, kpr)
    assert job.workable()
    tx = job.work({"from": keeper})
    print("deposited ether:", (buffered - lido.getBufferedEther()).to("ether"))
    print("credits used:", (credits - kpr.credits(job, kpr)).to("ether"))
    print("deposits processed:", len(tx.events["DepositEvent"]))
    print("gas used:", tx.gas_used)
