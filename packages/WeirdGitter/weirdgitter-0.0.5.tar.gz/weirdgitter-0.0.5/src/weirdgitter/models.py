class WeirdGitterResult:
    """
    Result of a WeirdGitter run
    Attributes:
        repo_path (str): Path to the repo
        name (str): Name of the WeirdGitter instance
        branch (str): Branch of the repo
        repo_url (str): URL of the repo
        result_status (str): Status of the result (None if no updates, Failed, OK, generic)
        error (str): Error message if result_status is Failed
        test_result (str): Result of running wg_test.sh
        build_result (str): Result of running wg_build.sh
        deploy_result (str): Result of running wg_deploy.sh
        updates (list): List of updates made to the repo
    """
    def __init__(self, **kwargs):
        self.__dict__ = {
            'repo_path': None,
            'name': None,
            'branch': None,
            'repo_url': None,
            'result_status': None, # Failed, OK, or generic, None if no updates
            'error': None, # Error message (str) or None
            'test_result': None,
            'build_result': None,
            'deploy_result': None, # All of the results are text, containing full stdout/stderr of running stages
            'updates': []
        }
        self.__dict__.update(kwargs)
        self.result_status = kwargs.get('result_status', None)
        
    @staticmethod
    def print(wgr: 'WeirdGitterResult'):
        if wgr.result_status is None:
            print(f" {wgr.dt} - {wgr.name} | Nothing changed ".center(100, '-'))
            return
        print(f"{wgr.name}".center(100, '-'))
        for k in wgr.updates:
            print(f"Update in `{k}`:\n\t{wgr.__dict__[k]}")
        print('='*100)