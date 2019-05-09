Role Name
=========

[![Build Status](https://travis-ci.org/znerol/ansible-role-ssh-kba.svg?branch=master)](https://travis-ci.org/znerol/ansible-role-ssh-kba)

Setup SSH public key authentication for machine to machine communication.

Requirements
------------

OpenSSH server and client software present.

Role Variables
--------------

In a typical setup this role is applied either to an SSH client or an SSH
server.  Tasks for the other side can be delegated by setting
`ssh_kba_server_hostname` and `ssh_kba_client_hostname` respectively. Also in
most cases it is recommended to specify `ssh_kba_server_user` and
`ssh_kba_client_user` explicitely instead of relying on the defaults.

Note: SSH host keys are collected from ansible facts. Thus it is important that
they are gathered beforehand for all involved machines.

### Variables affecting the server

Host and user representing the server side enpoint of the public key
authenticated ssh connection:

```
ssh_kba_server_hostname: "{{ inventory_hostname }}"
ssh_kba_server_user: # Ansible user on the server according to facts.
```

### Variables affecting the client

```
ssh_kba_client_hostname: "{{ inventory_hostname }}"
ssh_kba_client_user: # Ansible user on the server according to facts.
```

```
ssh_kba_client_host_fqdn: # FQDN of the server according to facts.
ssh_kba_client_host_ip4: # Default IP address of the server according to facts.
ssh_kba_client_host_ip6: # Default IP address of the server according to facts.

```

### Variables affecting the keypair

```
ssh_kba_keypair_type: rsa # One of dsa, ecdsa, ed25519, rsa
ssh_kba_keypair_size: # Omit by default
ssh_kba_keypair_comment: "{{ ssh_kba_client_user }}@{{ ssh_kba_client_hostname }}"
ssh_kba_keypair_dir: ~/.ssh
ssh_kba_keypair_name: "id_{{ ssh_kba_keypair_type }}"
ssh_kba_keypair_path: "{{ ssh_kba_keypair_dir }}/{{ ssh_kba_keypair_name }}"
ssh_kba_keypair_owner: "{{ ssh_kba_client_user }}"
ssh_kba_keypair_group: # Omit by default
ssh_kba_keypair_attributes: # Omit by default
ssh_kba_keypair_selevel: # Omit by default
ssh_kba_keypair_serole: # Omit by default
ssh_kba_keypair_setype: # Omit by default
ssh_kba_keypair_seuser: # Omit by default
```

The keypair will be regenerated if `ssh_kba_keypair_force` is set to `yes`.

```
ssh_kba_keypair_force: # Omit by default
```

The fact `ssh_kba_keypair_pub` is set to the public part of the keypair during
role evaluation.

### Variables affecting the servers authorized keys file

```
ssh_kba_keypair_pub: # see keypair section above
ssh_kba_server_authorized_keys_owner: "{{ ssh_kba_server_user }}"
ssh_kba_server_authorized_keys_comment: # Omit by default
ssh_kba_server_authorized_keys_exclusive: # Omit by default
ssh_kba_server_authorized_keys_key_options: # Omit by default
ssh_kba_server_authorized_keys_manage_dir: # Omit by default
ssh_kba_server_authorized_keys_path: # Omit by default
```

### Variables affecting the clients known hosts file

```
ssh_kba_client_known_hosts_owner: "{{ ssh_kba_client_user }}"
ssh_kba_client_known_hosts_hash_host | default(omit) }}"
ssh_kba_client_known_hosts_path | default(omit) }}"
```

Server FQDN, IPs and host key facts are collected in order to make them
available in the clients `known_hosts`. Overriding any of the following
variables will modify this behavior:

```
ssh_kba_server_host_fqdn: # FQDN of the server according to facts.
ssh_kba_server_host_ip4: # Default IP address of the server according to facts.
ssh_kba_server_host_ip6: # Default IP address of the server according to facts.
ssh_kba_server_host_names: # A list consisting of FQDN and default IP addresses.
ssh_kba_server_host_keys: # A list of pairs, each one consisting of the key
    type (first field) and the actual host key (second field). Defaults to
    values available from host facts.
```

The afforementioned variables will be used to populate a variable with a list
of host names and keys:

```
ssh_kba_server_host_names_and_keys: # A list of pairs, each one consisting of a
    hostname (or ip address) and a corresponding host key (in the form which is
    accepted by the known_hosts module)
```


Dependencies
------------

None.

Example Playbook
----------------

    - hosts: server.example.com
      tasks:
        - name: Gather client facts
          delegate: client.example.com
          delegate_facts: yes
          setup:

        - name: >-
            Key based authentication granted to beta@client.example.com on
            alpha@server.example.com
          vars:
            ssh_kba_server_user: alpha
            ssh_kba_client_hostname: client.example.com
            ssh_kba_client_user: beta
          import_role:
            name: znerol.ssh_kba

License
-------

BSD
