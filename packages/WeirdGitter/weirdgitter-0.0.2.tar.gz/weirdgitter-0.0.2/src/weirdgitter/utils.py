import chardet
import subprocess


def decode_auto(raw: bytes) -> str:
    """
    :param raw: bytes
    :return: str
    
    Automatically detects encoding and returns decoded string
    """
    detector = chardet.universaldetector.UniversalDetector()
    detector.feed(raw)
    detector.close()
    return raw.decode(detector.result['encoding'] or 'utf-8')


def exec_cmd(cmd: str, cwd: str = None) -> dict:
    """
    :param cmd: str Command to execute
    :param cwd: str Directory to run in
    :return: dict {'code': int, 'stdout': str, 'stderr': str}
    
    Run command and return outputs and code
    """
    p = subprocess.run(cmd, shell=True, capture_output=True, cwd=cwd)
    return {
        'stdout': decode_auto(p.stdout),
        'stderr': decode_auto(p.stderr),
        'code': p.returncode
    }
    
    

