from ib_insync import *
# util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

## FINDS ETFS WITH HIGH DIVIDEND YIELDS
subscription = ScannerSubscription(instrument='STK',locationCode='STK.US.MAJOR',scanCode='SCAN_currYrETFFYDividendYield_DESC')


scanData = ib.reqScannerData(subscription)

for scan in scanData:
    print(scan)
    print(scan.contractDetails.contract.symbol)