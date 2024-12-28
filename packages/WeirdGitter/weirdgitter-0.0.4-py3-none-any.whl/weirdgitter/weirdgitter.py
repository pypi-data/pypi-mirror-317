import os
from time import sleep
from datetime import datetime
from . import utils
from .models import WeirdGitterResult
import tomllib


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
    :attribute debug: bool whether to callback on startup and sys events
    :attribute debug_empty: bool whether to callback on "empty" runs
    :attribute: wgtoml: path to wgtoml
    """
    def __init__(
        self,
        repo_path: str,
        branch: str = 'master',
        name: str = 'WeirdGitter',
        repo_url: str = None,
        timeout: int = 300,
        callback: callable = None,
        run_on_start: bool = True,
        debug=False,
        debug_empty=False,
        wgtoml='weirdgitter.toml'
    ):
        self.repo_path = repo_path
        self.branch = branch
        self.repo_url = repo_url
        self.name = name
        self.timeout = timeout
        if callable(callback):
            self.callback = callback
        else:
            self.callback = WeirdGitterResult.print
        self.run_on_start = run_on_start
        self.debug = debug
        self.debug_empty = debug_empty
        
        self.config = tomllib.loads(open(os.path.join(self.repo_path,wgtoml), 'r').read())
        
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
        
        if self.debug:
            self.callback(self.__get_result__(status='Repo initialized'))
        
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
        
        stages = self.config['stages']
        
        # Check existence
        res = os.listdir(self.repo_path)
        for i in stages:
            if i not in res:
                self.callback(self.__get_result__(error=f'No {i} in repo', status='ERROR'))
                raise SystemExit('Failure at check existence')
                
        if len(stages) == 0:
            self.callback(self.__get_result__(error='No files to run', status='ERROR'))
        
        logs = {}
        prefix = '/' if not win else ''
        for i in stages:
            res = utils.exec_cmd(f'{prefix}{i}', cwd=self.repo_path)
            if res['code'] != 0:
                self.callback(self.__get_result__(error=res['stderr'], status='ERROR'))
                break
            else:
                logs[i] = res['stdout']
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
            if self.debug_empty:
                self.callback(self.__get_result__(msg='No updates'))
            else:
                pass
        else:
            print(stat['stdout'])
            self.run()
    
    def run_loop(
        self,
        ignore_errors=False
        ):
        """
        While True loop! Loop for infinite git pull and run scripts by self.timeout
        
        :param ignore_errors" bool
        """
        if self.run_on_start:
            self.run()
        
        while True:
            try:
                self.check_updates()
                sleep(self.timeout)
            except Exception as e:
                if not ignore_errors:
                    raise e
                self.callback(self.__get_result__(error=str(e), status='ERROR'))
            