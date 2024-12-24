from bqSQLrunner.__init__ import initBqSQLrunner

def main(project_id, dataset_id, sqldir_, workdir_, variables_, service_account_, bucket_name_):
    project = f"{project_id}"
    dataset = f"{dataset_id}"
    sqldir = f"{sqldir_}"
    workdir = f"{workdir_}"  # Optional: You can specify your own working directory if needed
    variables = variables_  # Optional: Dictionary of variables
    bucket_name=f"{bucket_name_}"
 
    fromstep = None  # Optional: Specify if needed
    tostep = None  # Optional: Specify if needed
    jsonvars = None  # Optional: Specify if needed
    dryrun = False  # Optional: Set to True for dry run
    fromScratch = False  # Optional: Set to True if you want to clean working directory
    service_account = f"{service_account_}"  # Optional: Specify service account

    # Initialize BqSQLrunner instance
    bqSQLrunner = initBqSQLrunner(
        project=project,
        dataset=dataset,
        sqldir=sqldir,
        workdir=workdir,
        variables=variables,
        fromstep=fromstep,
        tostep=tostep,
        jsonvars=jsonvars,
        dryrun=dryrun,
        fromScratch=fromScratch,
        service_account=service_account,
        bucket_name=bucket_name,
    )

    # Run the process
    bqSQLrunner.run()
 