import sys
import re
import os
import pathlib
import datetime
import pkg_resources
from google.cloud import bigquery, storage
import google.auth
from google.auth import impersonated_credentials

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
        self.storage_client = storage.Client(project=self.project)
        if self.serviceAccount != None:
            default_creds = self.get_default_credentials()
            sa_credentials = self.impersonate_service_account(self.serviceAccount, default_creds)
            self.GCPclient = bigquery.Client(project=self.project, credentials=sa_credentials)
            self.storage_client = storage.Client(project=self.project, credentials=sa_credentials)

    def prepare(self):
        runDirName = os.path.basename(self.SQLsrcDirName)                                                 ### vmtl erst slashes wegdonnern
        self.workDirName = os.path.join(self.workDirBase, self.VariableDefs['${project_id}'], self.VariableDefs['${dataset_id}'], runDirName)

        # Create work directory in GCS
        bucket = self.storage_client.get_bucket(self.bucket_name)
        blob = bucket.blob(self.workDirName)
        if not blob.exists():
            blob.upload_from_string('')  # Create an empty blob if the directory doesn't exist

        numSQL_files = 0
        numDone_files = 0
        numError_files = 0

        if self.fromScratch:
            self.cleanWorkDir()

        # List files in workdir from GCS bucket
        blobs = list(bucket.list_blobs(prefix=self.workDirName))
        for blob in blobs:
            if blob.name.endswith('.sql'):
                numSQL_files += 1
                file_name_with_extension = os.path.basename(blob.name)
                SqlbaseFileName = os.path.splitext(file_name_with_extension)[0] 
                errELemName = SqlbaseFileName + '.ERROR'
                if self.check_blob_exists(bucket, os.path.join(self.workDirName, errELemName)):
                    numError_files += 1
                    self.isRestart = True
                    self.RunFileList.clear()
                    self.delete_blob(bucket, os.path.join(self.workDirName, errELemName))
                self.RunFileList.append(blob.name)

                doneELemName = SqlbaseFileName + '.Done'
                if self.check_blob_exists(bucket, os.path.join(self.workDirName,doneELemName)):
                    numDone_files += 1

        # Process files from the source directory in GCS
        blobs = list(bucket.list_blobs(prefix=self.SQLsrcDirName))
        blobs.sort(key=lambda blob: blob.name) 

        if self.fromStep:
            self.fromIdx = self.getStepIdx(blobs, self.fromStep)
        if self.toStep:
            if self.fromStep == -1:
                raise RuntimeError("\n>\n>to-step given without from-step\n>")
            else:
                self.toIdx = self.getStepIdx(blobs, self.toStep)
        if self.toIdx < self.fromIdx and self.toIdx > -1:
            raise RuntimeError("\n>\n>to-step before from-step\n>")

        if self.isRestart:
            pass
        else:
            self.cleanWorkDir()
            self.RunFileList.clear()
            blobs.sort(key=lambda blob: blob.name)
            for i in range(0, len(blobs)):
                blob = blobs[i]
                if blob.name.endswith('.sql'):
                    numSQL_files += 1
                    if self.fromIdx > -1 and i == self.fromIdx:
                        self.RunFileList.append(blob.name)
                        self.fromStepFileName = blob.name
                        if self.toIdx == -1:
                            break
                    elif i > self.fromIdx and self.toIdx > self.fromIdx:
                        self.RunFileList.append(blob.name)
                    elif self.fromIdx == -1 and self.toIdx == -1:
                        self.RunFileList.append(blob.name)
                    if self.toIdx > -1 and i >= self.toIdx:
                        self.toStepFileName = blob.name
                        break

        # Read SQL files from GCS, replace variables, and write back to GCS
        self.RunFileList.sort()
        for RunElem in self.RunFileList:
            blob = bucket.blob(RunElem) 
            GCP_Code = blob.download_as_text()
            Run_Code = GCP_Code
            for VarName in self.VariableDefs.keys():
                Run_Code = Run_Code.replace(VarName, self.VariableDefs[VarName])
            file_name = os.path.basename(RunElem)
            new_blob = bucket.blob(os.path.join(self.workDirName, file_name)) 
            new_blob.upload_from_string(Run_Code)

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

        # Run SQL queries from GCS
        for RunElem in self.RunFileList:
            file_name = os.path.basename(RunElem)
            GCPbaseFileName = os.path.splitext(file_name)[0]
            blob = self.storage_client.get_bucket(self.bucket_name).blob(os.path.join(self.workDirName, file_name)) 
            GCP_Code = blob.download_as_text() 

            StepNo += 1
            print("{0:50s}".format(RunElem), end='')
            if self.dryrun:
                dryRunConfig = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
                query_job = self.GCPclient.query(GCP_Code, location="EU", job_config=dryRunConfig)
                print(" {0:8.2f}    {1:>15s} {2:20,d}".format(0, "dry-run", query_job.total_bytes_processed))
                continue
            else:
                query_job = self.GCPclient.query(GCP_Code, location="EU")

            try:
                results = query_job.result()
            except Exception as E:
                print('\n')
                print(E)
                print(query_job.query) 
                # Upload error file directly to GCS
                GCPerrFileContent = f"""Error Msg.....: {E.message}
                                        Error response: {E._response}
                                        Error errors...: {E._errors}
                                        {'-' * 100}
                                        {query_job.query}
                                    """
                error_blob = self.storage_client.get_bucket(self.bucket_name).blob(os.path.join(self.workDirName, GCPbaseFileName + '.ERROR'))
                error_blob.upload_from_string(GCPerrFileContent)
                raise
            if query_job.state == 'DONE':
                stepTime = query_job.ended - query_job.started
                # Upload done file directly to GCS
                GCPDoneFileContent = f"""Run Element {RunElem} Done.
                                            job_id.................................................: {query_job.job_id}
                                            created................................................: {query_job.created}
                                            started................................................: {query_job.started}
                                            ended, StepTime........................................: {query_job.ended}
                                            StepTime ..............................................: {stepTime.total_seconds()}
                                            slot_millis............................................: {query_job.slot_millis}
                                            num_dml_affected_rows .................................: {query_job.num_dml_affected_rows}
                                            total_bytes_processed .................................: {query_job.total_bytes_processed}
                                            destination............................................: {query_job.destination}
                                            referenced_tables......................................: {query_job.referenced_tables}
                                            {'-' * 80}
                                        """
                done_blob = self.storage_client.get_bucket(self.bucket_name).blob(os.path.join(self.workDirName, GCPbaseFileName + '.Done'))
                done_blob.upload_from_string(GCPDoneFileContent)

                dmlRows = 0
                if query_job.num_dml_affected_rows is not None:
                    dmlRows = int(query_job.num_dml_affected_rows)
                stepBytes = 0
                if query_job.total_bytes_processed is not None:
                    stepBytes = int(query_job.total_bytes_processed)
                runDir_total_Bytes_processed += stepBytes
                print(" {0:8.2f}    {1:15d} {2:20,d}".format(stepTime.total_seconds(), dmlRows, stepBytes))

        nowStr = datetime.datetime.now().isoformat(' ')
        print("\n\n>")
        print("> FINISHED JOB           : {0:80s}".format(self.SQLsrcDirName))
        print("> TIME                   : {0}".format(nowStr))
        print("> Total Byte processed   : {0:15,d}".format(runDir_total_Bytes_processed))
        print("-" * 80)

    def getStepIdx(self, DirList, stepIdent):
        numFound = 0
        StepFileName = None
        stepIdx = -1
        for i in range(0, len(DirList)):
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
        bucket = self.storage_client.get_bucket(self.bucket_name)
        blobs = list(bucket.list_blobs(prefix=self.workDirName))
        for blob in blobs:
            if blob.name.endswith('.sql') or blob.name.endswith('.Done'):
                blob.delete()

    def check_blob_exists(self, bucket, blob_name):
        blob = bucket.blob(blob_name)
        return blob.exists()

    def delete_blob(self, bucket, blob_name):
        blob = bucket.blob(blob_name)
        blob.delete()

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

        impersonated_credentials = google.auth.impersonated_credentials.Credentials(
            source_credentials=default_credentials,
            target_principal=service_account,
            target_scopes=target_scopes,
            lifetime=3600  # 1 hour
        )

        # workaround for version compatibility issue
        if self.google_auth_version >= pkg_resources.parse_version('1.6.0') and self.google_auth_version < pkg_resources.parse_version('2.0.0'):
            impersonated_credentials._source_credentials._scopes = default_credentials.scopes
        return impersonated_credentials
