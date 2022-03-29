import argparse
from  WALeadApp import gui
parser = argparse.ArgumentParser(description='WALeadApp Help')
parser.add_argument('--paid',help='purchase mode',action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
    paid = False
    if args.paid:
        paid=True
    gui.main(paid)