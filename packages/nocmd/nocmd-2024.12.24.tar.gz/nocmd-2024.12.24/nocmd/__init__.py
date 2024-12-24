import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Union

from funnylog2 import logger


class ShellExecutionFailed(Exception):

    def __init__(self, msg):
        err = f"Shell执行失败: {msg}"
        logger.error(err)
        Exception.__init__(self, err)


class _Config:
    PASSWORD: str = os.environ.get("YOUQU_PASSWORD") or "1"


config = _Config()


class Cmd:

    @staticmethod
    def _run(command, _input=None, timeout=None, check=False, executable=None, **kwargs):
        with subprocess.Popen(command, executable=executable, **kwargs) as process:
            try:
                stdout, stderr = process.communicate(_input, timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                raise subprocess.TimeoutExpired(process.args, timeout, output=stdout,
                                     stderr=stderr)
            except:
                process.kill()
                raise
            retcode = process.poll()
            if check and retcode:
                raise subprocess.CalledProcessError(
                    retcode, process.args, output=stdout, stderr=stderr
                )
        return subprocess.CompletedProcess(process.args, retcode, stdout, stderr)

    @classmethod
    def _getstatusoutput(cls, command, timeout, executable):
        kwargs = {
            "shell": True,
            "stderr": subprocess.STDOUT,
            "stdout": subprocess.PIPE,
            "timeout": timeout,
            "executable": executable,
        }
        try:
            if sys.version_info >= (3, 7):
                kwargs["text"] = True
            result = cls._run(command, **kwargs)
            data = result.stdout
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            exitcode = result.returncode
        except subprocess.CalledProcessError as ex:
            data = ex.output
            exitcode = ex.returncode
        except subprocess.TimeoutExpired as ex:
            data = ex.__str__()
            exitcode = -1
        if data[-1:] == "\n":
            data = data[:-1]
        return exitcode, data

    @classmethod
    def run(
            cls,
            command: str,
            workdir: Union[str, Path] = None,
            interrupt: bool = False,
            timeout: Union[None, int] = 25,
            print_log: bool = True,
            command_log: bool = True,
            return_code: bool = False,
            executable: str = "/bin/bash",
    ):
        wd = ""
        if workdir:
            workdir = os.path.expanduser(workdir)
            if not os.path.exists(workdir):
                raise FileNotFoundError
            wd = f"cd {workdir} && "
        exitcode, stdout = cls._getstatusoutput(wd + command, timeout=timeout, executable=executable)
        if command_log:
            logger.info(command)
        if exitcode != 0 and interrupt:
            raise ShellExecutionFailed(stdout)
        if print_log and stdout:
            logger.info(stdout)
        if return_code:
            return stdout, exitcode
        return stdout

    @staticmethod
    def expect_run(
            cmd: str,
            events: dict,
            return_code=False,
            timeout: int = 30,
            log_cmd: bool = True,
    ):
        """
        expect_run(
            "ssh username@machine_ip 'ls -l'",
            events={'password':'secret\n'}
        )
        如果 return_code=True，返回 (stdout, return_code)
        """
        import pexpect
        if log_cmd:
            logger.debug(cmd)
        res = pexpect.run(
            cmd,
            events=events,
            withexitstatus=return_code,
            timeout=timeout
        )
        if return_code is False:
            stdout = res.decode("utf-8")
            logger.debug(stdout)
            return stdout
        stdout, return_code = res
        stdout = stdout.decode("utf-8")
        logger.debug(stdout)
        return stdout, return_code

    @classmethod
    def sudo_run(
            cls,
            command,
            password: str = None,
            workdir: Union[str, Path] = None,
            interrupt: bool = False,
            timeout: int = 25,
            print_log: bool = True,
            command_log: bool = True,
            return_code: bool = False
    ):
        if password is None:
            password = config.PASSWORD
        wd = ""
        if workdir:
            workdir = os.path.expanduser(workdir)
            if not os.path.exists(workdir):
                raise FileNotFoundError
            wd = f"cd {workdir} && "
        res = cls.run(
            f"{wd}echo '{password}' | sudo -S {command}",
            interrupt=interrupt,
            timeout=timeout,
            print_log=print_log,
            command_log=command_log,
            return_code=return_code
        )
        if return_code is False:
            return res.lstrip("请输入密码●")
        res = list(res)
        res[0] = res[0].lstrip("请输入密码●")
        return res


class RemoteCmd:

    def __init__(self, user: str, ip: str, password: str):
        self.user = user
        self.ip = ip
        self.password = password

    def remote_run(
            self,
            cmd: str,
            return_code: bool = False,
            timeout: int = None,
            use_sshpass: bool = False,
            log_cmd: bool = True,
    ):
        remote_cmd = f'ssh -o StrictHostKeyChecking=no {self.user}@{self.ip} "{cmd}"'
        if use_sshpass:
            if log_cmd:
                logger.debug(remote_cmd)
            if os.popen("command -v sshpass").read().strip() == "":
                pkg = "apt"
                check_pkg = os.popen("command -v apt").read().strip()
                if check_pkg == "":
                    pkg = "yum"
                stdout, statuscode = Cmd.sudo_run(f"{pkg} install sshpass -y", return_code=True, timeout=30)
                if statuscode != 0:
                    raise EnvironmentError(
                        f"sshpass 安装失败，请尝试添加环境变量export YOUQU_PASSWORD=<PASSWORD>或手动安装:sudo {pkg} install sshpass 后再次执行。"
                    )
            res = os.system(f"sshpass -p '{self.password}' {remote_cmd}")
        else:
            res = Cmd.expect_run(
                remote_cmd,
                events={'password': f'{self.password}\n'},
                return_code=return_code,
                timeout=timeout,
                log_cmd=log_cmd,
            )
        return res

    def remote_sudo_run(
            self,
            cmd: str,
            workdir: str = None,
            timeout: int = None,
            return_code: bool = False,
            use_sshpass: bool = False,
            log_cmd: bool = True,
    ):
        wd = ""
        if workdir is not None:
            _, code = self.remote_run(f"ls {workdir}", return_code=True)
            if code == 0:
                wd = workdir
            else:
                raise FileNotFoundError(workdir)
        return self.remote_run(
            f"{wd}echo '{self.password}' | sudo -S {cmd}",
            return_code=return_code,
            timeout=timeout,
            use_sshpass=use_sshpass,
            log_cmd=log_cmd,
        )


def copy(source, dest):
    return Cmd.run(f"cp -rf {source} {dest}")


def move(source, dest):
    return Cmd.run(f"move -rf {source} {dest}")


def scp(user, ip, password, source, dest):
    Cmd.expect_run(
        f"/bin/bash -c 'scp {source} {user}@{ip}:{dest}'",
        events={'password': f'{password}\n'},
        timeout=220,
    )


def apt_policy(package_name):
    stdout = Cmd.run(f"apt policy {package_name}")
    res = re.search("已安装：(.*)", stdout).group(1)
    return res


def apt_install(package_name):
    check_installed: bool = Cmd.run(f"dpkg -s {package_name}").read().strip() == ""
    if check_installed:
        Cmd.sudo_run(f"apt install {package_name} -y")
