import os
from time import sleep
from datetime import datetime
from . import utils
from .models import WeirdGitterResult


class WeirdGitter:
    """
    Class for git operations
    Checks if repo exists, else clones it. Switches to branch, then with given timeout check if branch is up to date
    If pull - run wg_test.sh, if ["TEST DONE OK"] in res - run wg_build.sh, then wg_deploy.sh
    
    :attribute repo_path: path to repo (it is better to be absolute)
    :attribute branch: name of branch
    :attribute repo_url: url of repo [Optional]
    :attribute timeout: timeout in seconds [Default=300]
    :attribute callback: callback function to call after run
        Callback function should take one arg - wg_result. See WeirdGitterResult for info
    :attribute run_on_start: bool whether to run on start or on pull only
    """
    def __init__(
        self,
        repo_path: str,
        branch: str = 'master',
        name: str = 'WeirdGitter',
        repo_url: str = None,
        timeout: int = 300,
        callback: callable = None,
        run_on_start: bool = True
    ):
        self.repo_path = repo_path
        self.branch = branch
        self.repo_url = repo_url
        self.name = name
        self.timeout = timeout
        if callback is callable:
            self.callback = callback
        else:
            self.callback = WeirdGitterResult.print
        self.__init_repo__()
        
    def __init_repo__(self):
        # Check for path or create
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
            
        # Check if repo exists else clone
        status = utils.exec_cmd('git status', cwd=self.repo_path)
        if status['code'] != 0:
            self.callback(self.__get_result__(status='Failed to init repo', error=status['stderr'], msg=status['stdout'] + "\nCloning..."))
            
            #Cloning
            if not self.repo_url:
                raise ValueError('No repo url provided and no git repo in repo path')
            stat = utils.exec_cmd(f'git clone {self.repo_url} .', cwd=self.repo_path)
            if stat['code'] != 0:
                self.callback(self.__get_result__(status='Failed to clone repo', error=stat['stderr'], msg=stat['stdout']))
                raise SystemExit('Failure at clone')
            raise SystemExit('Failure at init_repo')
        
        # Switch to branch
        stat = utils.exec_cmd(f'git checkout -f {self.branch}', cwd=self.repo_path)
        if stat['code'] != 0:
            self.callback(self.__get_result__(status='Failed to switch to branch', error=stat['stderr'], msg=stat['stdout']))
            raise SystemExit('Failure at switch')
        
        self.callback(self.__get_result__(status='Repo initialized'))
        self.run()
        
    def __get_result__(
        self,
        status=None,
        error=None,
        test_result=None,
        build_result=None,
        deploy_result=None,
        **kwargs
    ):
        kwargs['result_status'] = status
        kwargs['error'] = error
        kwargs['test_result'] = test_result
        kwargs['build_result'] = build_result
        kwargs['deploy_result'] = deploy_result
        
        updates = [k for k in kwargs.keys() if kwargs[k]]
        
        kwargs['repo_path'] = self.repo_path
        kwargs['name'] = self.name
        kwargs['branch'] = self.branch
        kwargs['repo_url'] = self.repo_url
        kwargs['dt'] = datetime.now().strftime('%c')
        kwargs['updates'] = updates
        
        return WeirdGitterResult(**kwargs)
    
    def run(self):
        """
        Run scripts in root folder
        """
        win = os.name == 'nt'
        if not win and os.name != 'posix':
            raise NotImplementedError(f'OS {os.name} not supported')
        
        TEST_FILE = 'wg_test.bat' if win else 'wg_test.sh'
        BUILD_FILE = 'wg_build.bat' if win else 'wg_build.sh'
        DEPLOY_FILE = 'wg_deploy.bat' if win else 'wg_deploy.sh'
        
        # Check existence
        res = os.listdir(self.repo_path)
        run_files = []
        for i in res:
            if i == TEST_FILE:
                run_files.append(i)
            elif i == BUILD_FILE:
                run_files.append(i)
            elif i == DEPLOY_FILE:
                run_files.append(i)
        
        warns = []
        for i in (TEST_FILE, BUILD_FILE, DEPLOY_FILE):
            if i not in run_files:
                warns.append(f'No {i} in repo')
                
        if len(warns) > 0 and len(run_files) > 0:
            self.callback(self.__get_result__(WARNING='\n\t'.join(warns), status='WARNING'))
        elif len(run_files) == 0:
            self.callback(self.__get_result__(error='No files to run', status='ERROR'))
        
        logs = {}
        prefix = '/' if not win else ''
        for i in run_files:
            res = utils.exec_cmd(f'{prefix}{i}', cwd=self.repo_path)
            if res['code'] != 0:
                self.callback(self.__get_result__(error=res['stderr'], status='ERROR'))
                break
            else:
                if i == TEST_FILE:
                    logs['test_result'] = res['stdout']
                elif i == BUILD_FILE:
                    logs['build_result'] = res['stdout']
                elif i == DEPLOY_FILE:
                    logs['deploy_result'] = res['stdout']
        if len(logs) > 0:
            self.callback(self.__get_result__(**logs, status='SUCCESS'))
        else:
            self.callback(self.__get_result__(status='NO DATA', msg='Run done but no data was output by scripts'))
    
    def check_updates(self):
        """
        Git pull, then run scripts if any changes were pulled
        """
        stat = utils.exec_cmd(f'git pull -f', cwd=self.repo_path)
        if stat['code'] != 0:
            self.callback(self.__get_result__(status='Failed to pull repo', error=stat['stderr'], msg=stat['stdout']))
            raise SystemExit('Failure at check_updates')
        if 'Already up to date' in stat['stdout']:
            self.callback(self.__get_result__(msg='No updates'))
        else:
            self.run()
    
    def run_loop(self):
        """
        While True loop! Loop for infinite git pull and run scripts by self.timeout
        """
        while True:
            self.check_updates()
            sleep(self.timeout)
            