#!/usr/bin/env python3


from include.model import WFModel
from share.config import positiveAddress, negativeAddress


if __name__ == "__main__":
    pos = WFModel(positiveAddress)
    neg = WFModel(negativeAddress)
    print(pos.communicate(">DON?\n"))
    print(neg.communicate(">DON?\n"))
    pos.disconnect()
    neg.disconnect()
