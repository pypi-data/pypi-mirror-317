from scan_utils.pkg.utils.shell import SHELL

shell1 = SHELL(local=True)

ret = shell1.exec_shell("env | grep test; pwd; ls .", env={"test1": "haha"}, cwd="/tmp/")
print(ret)