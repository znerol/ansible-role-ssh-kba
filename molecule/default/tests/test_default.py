import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_authorized_connections(host):
    host_vars = host.ansible.get_variables()

    dest_host = host_vars["ssh_m2m_dest_hostname"]
    dest_user = host_vars["ssh_m2m_dest_user"]
    source_user = host_vars["ssh_m2m_source_user"]

    assert dest_user == host.check_output(
        "sudo -u %s -- ssh -q -o BatchMode=yes %s@%s -- whoami", source_user,
        dest_user, dest_host)
    assert dest_host in host.check_output(
        "sudo -u %s -- ssh -q -o BatchMode=yes %s@%s -- getent hosts",
        source_user, dest_user, dest_host)


def test_unauthorized_local_user(host):
    host_vars = host.ansible.get_variables()

    dest_host = host_vars["ssh_m2m_dest_hostname"]
    dest_user = host_vars["ssh_m2m_dest_user"]
    source_user = "root"

    host.run_expect(
        [255], "sudo -u %s -- ssh -q -o BatchMode=yes %s@%s -- whoami",
        source_user, dest_user, dest_host)


def test_unauthorized_remote_user(host):
    host_vars = host.ansible.get_variables()

    dest_host = host_vars["ssh_m2m_dest_hostname"]
    dest_user = "root"
    source_user = host_vars["ssh_m2m_source_user"]

    host.run_expect(
        [255], "sudo -u %s -- ssh -q -o BatchMode=yes %s@%s -- whoami",
        source_user, dest_user, dest_host)
