import argparse
import os

from Driver import Driver

parser = argparse.ArgumentParser(description='Home AI Command Line Tool')
parser.add_argument("--install", dest="install")
parser.add_argument("--author", dest="author")
parser.add_argument("--uninstall", dest="uninstall")
parser.add_argument("--createtask", dest="createtask")
args = parser.parse_args()

driver = Driver()

if args.install:
    driver.install(args.install)
elif args.uninstall:
    driver.uninstall(args.uninstall)
elif args.createtask:
    driver.create(args.createtask)
else:
    driver.run()
