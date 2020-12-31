# shop bought at is ebay, calculates profit depending on platform sold on.
def ebay(price, deliv, sell, postage, shop2, fee, shippingcharge):
    sell = sell + shippingcharge
    if shop2.lower() == "ebay":
        profit = (sell * (0.971 - (fee / 100))) - (price + deliv) - postage - 0.30
    elif shop2.lower() == "bank transfer":
        profit = sell - (price + deliv) - postage

    return profit


def paypalfee(sell, shippingcharge):
    paypalfee = (sell + shippingcharge) * 0.029 + 0.30
    return paypalfee

def ebayfee(sell, shippingcharge, fee):
    ebayfee = (sell + shippingcharge) * (fee / 100)
    return ebayfee

# shop bought at is Shpock, calculates profit depending on platform sold on.
def shpock(price, deliv, sell, postage, shop2, fee):
    if shop2.lower() == "ebay":
        profit = (sell * (0.971 - (fee / 100))) - (price + deliv + (0.05 * price)) - postage - 0.30
    elif shop2.lower() == "bank transfer":
        profit = sell - (price + deliv + (0.05 * price)) - postage

    return profit