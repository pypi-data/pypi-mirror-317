import argparse
import os
import json
from json.decoder import JSONDecodeError
from __init__ import initBqSQLrunner

def parse_arguments():
    bqStepcliParser = argparse.ArgumentParser()
    bqStepcliParser.add_argument('-P', '--project', action='store', type=str, nargs=1, required=True)
    bqStepcliParser.add_argument('-D', '--dataset', action='store', type=str, nargs=1, required=True)
    bqStepcliParser.add_argument('-S', '--sqldir',  action='store', type=str, nargs=1, required=True)
    bqStepcliParser.add_argument('-W', '--workdir', action='store', type=str, nargs=1, default="/tmp")
    bqStepcliParser.add_argument('-V', '--variables', action='store', type=str, nargs=1)
    bqStepcliParser.add_argument('-F', '--fromstep', action='store', type=str, nargs=1)
    bqStepcliParser.add_argument('-T', '--tostep', action='store', type=str, nargs=1)
    bqStepcliParser.add_argument('-J', '--jsonvars', action='store', type=str, nargs=1)
    bqStepcliParser.add_argument('-X', '--dry-run', action='store_true')
    bqStepcliParser.add_argument('-Z', '--from-scratch', action='store_true')
    bqStepcliParser.add_argument('-A', '--service-account', action='store', type=str, nargs=1)

    return bqStepcliParser.parse_args()

def run_bq_sql_runner(args):
    jsonVars = None
    jsonVarsFileName = None
    if args.jsonvars:
        jsonVarsFileName =  args.jsonvars[0]
        if os.path.isfile(jsonVarsFileName) and os.access(jsonVarsFileName, os.R_OK):
            with open(jsonVarsFileName, 'r') as jsonFile:
                try:
                    jsonVars = json.load(jsonFile)
                except JSONDecodeError as jsonE:
                    raise RuntimeError(f"\n>\n>-J/--jsonvars >{jsonVarsFileName}< not readable or malformatted json\n>")
        else:
            raise RuntimeError(f"--jsonvars >{jsonVarsFileName}< either not a file or not readable")

    varsDict = None
    if jsonVars:
        varsDict = jsonVars
    if args.variables:
        varstring = args.variables[0]
        try:
            varsDict = dict(x.split(':') for x in varstring.split(','))
        except ValueError as VE:
            raise RuntimeError(f"--variables values >{varstring}< malformed")

    fromStep = args.fromstep[0] if args.fromstep else None
    toStep = args.tostep[0] if args.tostep else None
    serviceAccount = args.service_account[0] if args.service_account else None

    bqSQLrunner = initBqSQLrunner(project=args.project[0], dataset=args.dataset[0],
                                  sqldir=args.sqldir[0], workdir=args.workdir[0],
                                  variables=varsDict, fromstep=fromStep, tostep=toStep,
                                  jsonvars=jsonVarsFileName, dryrun=args.dry_run,
                                  fromScratch=args.from_scratch, service_account=serviceAccount)
    bqSQLrunner.run()

def main():
    args = parse_arguments()
    run_bq_sql_runner(args)

if __name__ == '__main__':
    main()
