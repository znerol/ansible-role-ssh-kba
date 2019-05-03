import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_authorized_connections(host):
    host_vars = host.ansible.get_variables()

    server_host = host_vars["ssh_kba_server_hostname"]
    server_user = host_vars["ssh_kba_server_user"]
    client_user = host_vars["ssh_kba_client_user"]

    assert server_user == host.check_output(
        "sudo -u %s -- ssh -q -o BatchMode=yes %s@%s -- whoami", client_user,
        server_user, server_host)
    assert server_host in host.check_output(
        "sudo -u %s -- ssh -q -o BatchMode=yes %s@%s -- getent hosts",
        client_user, server_user, server_host)


def test_unauthorized_local_user(host):
    host_vars = host.ansible.get_variables()

    server_host = host_vars["ssh_kba_server_hostname"]
    server_user = host_vars["ssh_kba_server_user"]
    client_user = "root"

    host.run_expect(
        [255], "sudo -u %s -- ssh -q -o BatchMode=yes %s@%s -- whoami",
        client_user, server_user, server_host)


def test_unauthorized_remote_user(host):
    host_vars = host.ansible.get_variables()

    server_host = host_vars["ssh_kba_server_hostname"]
    server_user = "root"
    client_user = host_vars["ssh_kba_client_user"]

    host.run_expect(
        [255], "sudo -u %s -- ssh -q -o BatchMode=yes %s@%s -- whoami",
        client_user, server_user, server_host)
