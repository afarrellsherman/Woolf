import os
import tempfile
import wget
import zipfile

tut_file_url = 'https://osf.io/gtjfq/download'

def command_filter(line):
    commands = ['trainWoolf', 'featureTable']
    cmd = line.split()[0] # get first item
    return cmd in commands


tmp = tempfile.TemporaryDirectory()
tutorial_file = os.path.normpath(os.path.join(
                        os.path.dirname(__file__),
                        '..', 'docs', 'usermanual.md'
                    ))

tutorial_commands = []
with open(tutorial_file) as tut:
    for line in tut:
        if line.startswith("$ "):
            line = line.lstrip('$ ')
            if command_filter(line):
                tutorial_commands.append(line)

wget.download(tut_file_url, os.path.join(tmp.name, "files.zip"))
zipfile.ZipFile(os.path.join(tmp.name, "files.zip")).extractall(tmp.name)

def test_trainWoolf_help(script_runner):
    ret = script_runner.run('trainWoolf', '--help')
    assert ret.success
    assert ret.stderr == ''

def test_trainWoolf_help(script_runner):
    ret = script_runner.run('featureTable', '--help')
    assert ret.success
    assert ret.stderr == ''

def test_tutorial_commands(script_runner):
    os.chdir(tmp.name)
    for cmd in tutorial_commands:
        args = cmd.split()
        ret = script_runner.run(*args)

        assert ret.success
        assert ret.stderr == ''
