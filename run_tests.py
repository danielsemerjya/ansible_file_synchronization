import subprocess
import docker
import unittest

import threading
import datetime

class DockerContainerHost(object):
    def __init__(self):
        self._client = docker.DockerClient()
        self._container = None

    def __enter__(self):
        image = self._client.images.build(path='.')
        self._container = self._client.containers.run(image[0].id, detach=True, auto_remove=True, entrypoint='tail -f /dev/null')
        return self
        

    def execute(self, command) -> None:
        command_result = self._container.exec_run(command)
        assert command_result.exit_code == 0

    def __exit__(self, exc_type, exc_val, exc_tb):# TODO get rid of container teardown lag
        current_date = datetime.datetime.now()
        threading.Thread(target=self._stop_container).start()
        print("Removing lag..", (datetime.datetime.now() - current_date).total_seconds(), "[s]")
        self._container = None

    def name(self) -> str:
        return self._container.name

    def _stop_container(self) -> None:
        self._container.stop()

    def check_is_file_exists(self, path: str) -> bool:
        error_message = "No such file or directory"
        stat = self._container.exec_run(f'stat {path}')
        if error_message not in stat.output.decode('utf-8'):
            return True
        return False

def run_playbook(hosts, filePath) -> None:
    inlineInventory = ''.join([host.name() + ',' for host in hosts])
    cmd = 'ansible-playbook -i %s -c docker synchronize_file.yml -efileToSync=%s' % (inlineInventory, filePath)
    subprocess.check_call(cmd, shell=True)

class Tester(unittest.TestCase):
    # TODO add more tests, for each path in the synchronize_file.yml
    def test_two_hosts_one_file(self):
        with DockerContainerHost() as host1, DockerContainerHost() as host2:
            host1.execute('/bin/sh -c "echo content > /tmp/foo"')
            run_playbook([host1, host2], '/tmp/foo')
            # TODO write checks that verify playbook synchronized file
            assert host1.check_is_file_exists('/tmp/foo') == True
            assert host2.check_is_file_exists('/tmp/foo') == True
    
    def test_two_hosts_two_files(self):
        with DockerContainerHost() as host1, DockerContainerHost() as host2:
            host1.execute('/bin/sh -c "echo content > /tmp/foo"')
            host2.execute('/bin/sh -c "echo content > /tmp/foo"')
            run_playbook([host1, host2], '/tmp/foo')
            assert host1.check_is_file_exists('/tmp/foo') == True
            assert host2.check_is_file_exists('/tmp/foo') == True

    def test_two_hosts_no_file(self):
        with DockerContainerHost() as host1, DockerContainerHost() as host2:
            try:
                run_playbook([host1, host2], '/tmp/foo')
            except:
                pass
            else:
                raise Exception("Playbook should fail if file does not exist")

    def test_two_hosts_one_file_without_playbook(self):
        with DockerContainerHost() as host1, DockerContainerHost() as host2:
            host1.execute('/bin/sh -c "echo content > /tmp/foo"')
            assert host1.check_is_file_exists('/tmp/foo') == True
            assert host2.check_is_file_exists('/tmp/foo') == False

    def test_four_hosts_one_file(self):
        with DockerContainerHost() as host1, DockerContainerHost() as host2, DockerContainerHost() as host3, DockerContainerHost() as host4:
            host3.execute('/bin/sh -c "echo content > /tmp/foo"')
            run_playbook([host1, host2, host3, host4], '/tmp/foo')
            assert host1.check_is_file_exists('/tmp/foo') == True
            assert host2.check_is_file_exists('/tmp/foo') == True
            assert host3.check_is_file_exists('/tmp/foo') == True
            assert host4.check_is_file_exists('/tmp/foo') == True

    def test_four_hosts_two_files(self):
        with DockerContainerHost() as host1, DockerContainerHost() as host2, DockerContainerHost() as host3, DockerContainerHost() as host4:
            host1.execute('/bin/sh -c "echo content > /tmp/foo"')
            host4.execute('/bin/sh -c "echo content > /tmp/foo"')
            run_playbook([host1, host2, host3, host4], '/tmp/foo')
            assert host1.check_is_file_exists('/tmp/foo') == True
            assert host2.check_is_file_exists('/tmp/foo') == True
            assert host3.check_is_file_exists('/tmp/foo') == True
            assert host4.check_is_file_exists('/tmp/foo') == True


if __name__ == '__main__':
    unittest.main()

