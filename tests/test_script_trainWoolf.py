def test_trainWoolf(script_runner):
    ret = script_runner.run('trainWoolf', '--help')
    assert ret.success
    assert ret.stderr == ''
    
