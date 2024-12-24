#
# BigQuery SQL Runner: 
# runs all files named '.sql' in alphabetical order 
#
import sys
import re
import os
import pathlib
import datetime
import pkg_resources
from google.cloud import bigquery, storage
import google.auth
from google.auth import impersonated_credentials as impersonated_credentials_v1


class bqSQLrunner():
    def __init__(self, sqldir=None, workdir=None, project=None, dataset=None, variables=None,
                 fromstep=None, tostep=None, jsonvars=None, dryrun=False, fromScratch=False,
                 service_account=None, bucket_name=None):
        self.version = "3.0.057"
        self.VariableDefs = {}
        if variables != None:
            for keyVal in variables:
                self.VariableDefs['${' + keyVal + '}'] = variables[keyVal]
        self.VariableDefs['${project_id}'] = project
        self.VariableDefs['${dataset_id}'] = dataset
        self.project = project
        self.dataset = dataset
        self.workDirBase = workdir
        self.SQLsrcDirName = sqldir
        self.fromStep = fromstep
        self.fromIdx = -1
        self.fromStepFileName = ''
        self.toStep = tostep
        self.toIdx = -1
        self.toStepFileName = ''
        self.dryrun = dryrun
        self.fromScratch = fromScratch
        self.serviceAccount = service_account
        self.bucket_name = bucket_name

        self.RunFileList = []
        self.isRestart = False
        self.google_auth_version = pkg_resources.get_distribution("google-auth").parsed_version

        self.GCPclient = bigquery.Client(project=self.project)
        if self.serviceAccount != None:
            default_creds = self.get_default_credentials()
            sa_credentials = self.impersonate_service_account(self.serviceAccount, default_creds)
            self.GCPclient = bigquery.Client(project=self.project, credentials=sa_credentials)

        self.storage_client = storage.Client()

    #
    #------------------------------------------------------------------------------
    # prepare part here
    #------------------------------------------------------------------------------
    #
    def prepare(self):
        bucket = self.storage_client.bucket(self.bucket_name)
        runDirName = os.path.basename(self.SQLsrcDirName)
        self.workDirName = os.path.join(self.workDirBase, self.VariableDefs['${project_id}'], self.VariableDefs['${dataset_id}'], runDirName)
        pathlib.Path(self.workDirName).mkdir(parents=True, exist_ok=True)

        sql_blobs = list(bucket.list_blobs(prefix=self.SQLsrcDirName))
        sql_files = [blob for blob in sql_blobs if blob.name.endswith('.sql')]
        sql_files.sort(key=lambda x: x.name)

        for blob in sql_files:
            local_path = os.path.join(self.workDirName, os.path.basename(blob.name))
            blob.download_to_filename(local_path)

        DirList = os.listdir(self.workDirName)
        DirList.sort()

        numSQL_files = 0
        numError_files = 0
        numDone_files = 0

        for DirElem in DirList:
            if DirElem.endswith('.sql'):
                numSQL_files += 1
                SqlbaseFileName, sqlextension = os.path.splitext(DirElem)
                errELemName = SqlbaseFileName + '.ERROR'
                if os.path.exists(os.path.join(self.workDirName, errELemName)):
                    numError_files += 1
                    self.isRestart = True
                    self.RunFileList.clear()
                    os.remove(os.path.join(self.workDirName, errELemName))
                self.RunFileList.append(DirElem)

                doneELemName = SqlbaseFileName + '.Done'
                if os.path.exists(os.path.join(self.workDirName, doneELemName)):
                    numDone_files += 1

        if self.fromStep:
            self.fromIdx = self.getStepIdx(DirList, self.fromStep)
        if self.toStep:
            if self.fromIdx == -1:
                raise RuntimeError("\n>\n>to-step given without from-step\n>")
            else:
                self.toIdx = self.getStepIdx(DirList, self.toStep)
        if self.toIdx < self.fromIdx and self.toIdx > -1:
            raise RuntimeError("\n>\n>to-step before from-step\n>")

        self.cleanWorkDir()
        self.RunFileList.clear()
        for i, DirElem in enumerate(DirList):
            if DirElem.endswith('.sql'):
                if self.fromIdx > -1 and i == self.fromIdx:
                    self.RunFileList.append(DirElem)
                    self.fromStepFileName = DirElem
                    if self.toIdx == -1:
                        break
                elif i > self.fromIdx and self.toIdx > self.fromIdx:
                    self.RunFileList.append(DirElem)
                elif self.fromIdx == -1 and self.toIdx == -1:
                    self.RunFileList.append(DirElem)
                if self.toIdx > -1 and i >= self.toIdx:
                    self.toStepFileName = DirElem
                    break

        for RunElem in self.RunFileList:
            with open(os.path.join(self.workDirName, RunElem), 'r') as f:
                content = f.read()
            for VarName in self.VariableDefs.keys():
                content = content.replace(VarName, self.VariableDefs[VarName])
            with open(os.path.join(self.workDirName, RunElem), 'w') as f:
                f.write(content)

    #------------------------------------------------------------------------------
    # run part here
    #------------------------------------------------------------------------------

    def run(self):
        self.prepare()

        print("--- Bq Sql Runner Version: {}".format(self.version))
        print("--- project              : {}".format(self.VariableDefs['${project_id}'] ))
        print("--- dataset_id           : {}".format(self.VariableDefs['${dataset_id}'] ))
        print("--- sql dir              : {}".format(self.SQLsrcDirName ))
        print("--- work dir             : {}".format(self.workDirName ))
        print("--- from step            : {}".format(self.fromStepFileName ))
        print("--- to step              : {}".format(self.toStepFileName ))
        if self.isRestart:
            print("--- Restart mode         : #> in effect <#")
        for VarName in sorted(self.VariableDefs.keys()):
            print("--- variable             : {0} = {1}".format(VarName, self.VariableDefs[VarName] ))
        if self.serviceAccount:
            print("--- impersonated sa      : {}".format(self.serviceAccount))
        print("\n")
        nowStr = datetime.datetime.now().isoformat(' ')
        print("> STARTING JOB           : {0:80s}".format(self.SQLsrcDirName))
        print("> TIME                   : {0}".format(nowStr ))
        print("\n")
        print("{0:50s} {1:11s} {2:>15s} {3:>20s}".format("RunFile", "Duration", "DML-rows", "Bytes proc."))

        StepNo = 0
        runDir_total_Bytes_processed = 0

        for RunElem in self.RunFileList:
            GCPbaseFileName, sqlextension = os.path.splitext(RunElem)
            GCPrunFile = os.path.join(self.workDirName,RunElem)
            GCP_File = open(GCPrunFile,'r')
            GCP_Code = GCP_File.read()
            GCP_File.close()
            Run_Code = GCP_Code

            StepNo += 1
            print("{0:50s}".format(RunElem), end='')
            if self.dryrun:
                dryRunConfig = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
                query_job = self.GCPclient.query(Run_Code,location="EU", job_config=dryRunConfig )
                print(" {0:8.2f}    {1:>15s} {2:20,d}".format(0 , "dry-run", query_job.total_bytes_processed))
                continue
            else:
                query_job = self.GCPclient.query(Run_Code,location="EU")
            try:
                results = query_job.result()
            except Exception as E:
                print('\n')
                print(E)
                print(query_job.query)
                GCPerrFile = open(os.path.join(self.workDirName, GCPbaseFileName + '.ERROR'), 'w')
                GCPerrFile.write("Error Msg.....: {}\n".format(E.message))
                GCPerrFile.write("Error response: {}\n".format(E._response))
                GCPerrFile.write("Error erros...: {}\n".format(E._errors))
                GCPerrFile.write("-" * 100)
                GCPerrFile.write('\n' + query_job.query + '\n')
                GCPerrFile.close()
                raise
            if query_job.state == 'DONE':
                stepTime = query_job.ended - query_job.started
                GCPDoneFile = open(os.path.join(self.workDirName, GCPbaseFileName + '.Done'), 'w')
                GCPDoneFile.write("Run Element {} Done.\n".format(RunElem))
                GCPDoneFile.write("job_id.................................................: {}\n".format( query_job.job_id))
                GCPDoneFile.write("created................................................: {}\n".format( query_job.created))
                GCPDoneFile.write("started................................................: {}\n".format( query_job.started))
                GCPDoneFile.write("ended, StepTime........................................: {}\n".format( query_job.ended ))
                GCPDoneFile.write("StepTime ..............................................: {}\n".format( stepTime.total_seconds() ))
                GCPDoneFile.write("slot_millis............................................: {}\n".format( query_job.slot_millis))
                GCPDoneFile.write("num_dml_affected_rows .................................: {}\n".format( query_job.num_dml_affected_rows))
                GCPDoneFile.write("total_bytes_processed .................................: {}\n".format( query_job.total_bytes_processed))
                GCPDoneFile.write("destination............................................: {}\n".format( query_job.destination))
                GCPDoneFile.write("referenced_tables......................................: {}\n".format( query_job.referenced_tables))
                GCPDoneFile.write("-" * 80)
                GCPDoneFile.close()
                #
                dmlRows = 0
                if query_job.num_dml_affected_rows != None:
                    dmlRows = int(query_job.num_dml_affected_rows)
                stepBytes = 0
                if query_job.total_bytes_processed != None:
                    stepBytes = int(query_job.total_bytes_processed)
                runDir_total_Bytes_processed += stepBytes
                print(" {0:8.2f}    {1:15d} {2:20,d}".format(stepTime.total_seconds(),dmlRows,stepBytes))
                #

        nowStr = datetime.datetime.now().isoformat(' ')
        print("\n\n>")
        print("> FINISHED JOB           : {0:80s}".format(self.SQLsrcDirName))
        print("> TIME                   : {0}".format(nowStr ))
        print("> Total Byte processed   : {0:15,d}".format(runDir_total_Bytes_processed ))
        print("-" * 80)

    def getStepIdx(self, DirList, stepIdent):
        numFound = 0
        StepFileName = None
        stepIdx = -1
        for i in range(0,len(DirList)):
            DirElem = DirList[i]
            if DirElem.startswith(stepIdent):
                StepFileName = DirElem
                numFound += 1
                stepIdx = i
        if numFound > 1:
            raise RuntimeError("\n>\n>step >{}< not unique\n>".format(stepIdent))
        if numFound == 0:
            raise RuntimeError("\n>\n>step >{}< not found\n>".format(stepIdent))
        return stepIdx


    def cleanWorkDir(self):
        DirList = os.listdir(self.workDirName)
        for dirElem in DirList:
            if dirElem.endswith('.sql') or dirElem.endswith('.Done'):
                os.remove(os.path.join(self.workDirName, dirElem))

    def get_default_credentials(self):
        credentials, _ = google.auth.default()
        return credentials

    def impersonate_service_account(self, service_account, default_credentials):
        target_scopes = [
            "https://www.googleapis.com/auth/iam",
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/bigquery.insertdata",
            "https://www.googleapis.com/auth/cloud-platform"
        ]

        impersonated_credentials = impersonated_credentials_v1.Credentials(
            source_credentials=default_credentials,
            target_principal=service_account,
            target_scopes=target_scopes,
            lifetime=3600
        )

        if self.google_auth_version >= pkg_resources.parse_version('1.6.0') and self.google_auth_version < pkg_resources.parse_version('2.0.0'):
            impersonated_credentials._source_credentials._scopes = default_credentials.scopes
        return impersonated_credentials
