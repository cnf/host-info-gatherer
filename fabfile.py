#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gather host information
fab host:127.0.0.1,localhost password info
fab hostlist:list.csv dmesg
"""

__author__ = "Frank Rosquin <frank@rosquin.net>"
__copyright__ = "Copyright 2013, Frank Rosquin"

__license__ = "ISC"
__maintainer__ = "Frank Rosquin"
__email__ = "frank@rosquin.net"

from fabric.api import env, settings, hide, run, get, runs_once
from fabric.contrib import files

import os

# defaults
env.user = 'root'


@runs_once
def host(host, name="__unset__"):
    """
    hostname to run against
    host:<ip>,<name>
    """
    if name == "__unset__":
        env.hosts = {host: host}
    else:
        env.hosts = {host: name}


@runs_once
def hostfile(filename):
    """
    hostfile to use
    comma separated (ip,name)
    hostfile:<file.csv>
    """
    env.hosts = {}
    with open(filename) as hfp:
        for line in hfp.readlines():
            ip, name = line.rstrip().split(',')
            env.hosts[ip] = name


@runs_once
def username(username):
    """
    username to use
    default is root
    username:admin
    """
    env.user = username


@runs_once
def passwd():
    env.no_agent = True
    env.no_keys = True


def _host_dir():
    hostname = env.hosts[env.host_string]
    if not os.path.isdir('output'):
        os.mkdir('output')
    if not os.path.isdir("output/{}".format(hostname)):
        os.mkdir("output/{}".format(hostname))


def _write_file(fname, content):
    hostname = env.hosts[env.host_string]
    _host_dir()
    filename = "output/{}/{}.txt".format(hostname, fname)
    with open(filename, 'w') as fp:
        fp.write(content)


def date():
    """`date` command"""
    cur = run('date')
    _write_file('date', cur)


def release():
    """output of /etc/{redhat-release,debian_version}"""
    if files.exists('/etc/redhat-release'):
        with hide('output'):
            rel = run('cat /etc/redhat-release')
    elif files.exists('/etc/debian_version'):
        with hide('output'):
            rel = run('cat /etc/debian_version')
    else:
        rel = "unknown distribution"
        print('{}: unknown distribution'.format(env.hosts[env.host_string]))
    _write_file('release', rel)


def uname():
    """uname -a"""
    with hide('output'):
        huname = run('uname -a')
    _write_file('uname', huname)


def ip_a():
    """ip a"""
    with hide('output'):
        ipa = run('ip a')
    _write_file('ip_a', ipa)


def ip_route():
    """ip route show table all"""
    with hide('output'):
        route = run('ip route show table all')
    _write_file('ip_route_show_table_all', route)


def ip_rule():
    """ip rule show"""
    with hide('output'):
        rule = run('ip rule show')
    _write_file('ip_rule_show', rule)


def netstat():
    """netstat -neltup"""
    with hide('output'):
        na = run('netstat -neltup')
    _write_file('netstat-nltup', na)


def chkconfig():
    """chkconfig --list|grep on"""
    with hide('output'):
        if files.exists('/sbin/chkconfig'):
            chkconf = run('chkconfig --list|grep on')
            _write_file('chkconfig', chkconf)
        elif files.exists('/sbin/initctl'):
            chkconf = run('initctl list')
            _write_file('initctl_list', chkconf)
        elif files.exists('sysv-rc-conf'):
            chkconf = run('/usr/sbin/sysv-rc-conf --list')
            _write_file('sysv-rc-conf_list', chkconf)
        else:
            chkconf = run('ls /etc/rc*.d/')
            _write_file('', chkconf)


def packages():
    """rpm -qa or dpkg -l"""
    if files.exists('/bin/rpm'):
        with hide('output'):
            pkgs = run('rpm -qa')
            _write_file('rpm-qa', pkgs)
    elif files.exists('/usr/bin/dpkg'):
        with hide('output'):
            pkgs = run('dpkg -l')
            _write_file('dpkg-l', pkgs)


def ps_aux():
    """ps auxww --forest"""
    with hide('output'):
        ps = run('ps auxww --forest')
    _write_file('ps_auxww--forest', ps)


def free():
    """free -m"""
    with hide('output'):
        mem = run('free -m')
    _write_file('free-m', mem)


def cpuinfo():
    """cat /proc/cpuinfo"""
    with hide('output'):
        info = run('cat /proc/cpuinfo')
    _write_file('cpuinfo', info)


def uptime():
    """uptime"""
    with hide('output'):
        time = run('uptime')
    _write_file('uptime', time)


def dmesg():
    """dmesg"""
    with hide('output'):
        msg = run('dmesg')
    _write_file('dmesg', msg)


def dmidecode():
    """dmidecode"""
    with settings(warn_only=True), hide('output'):
        dmi = run('dmidecode')
    _write_file('dmidecode', dmi)


def lsmod():
    """lsmod"""
    with hide('output'):
        mod = run('lsmod')
    _write_file('lsmod', mod)


def lspci():
    """lspci"""
    with settings(warn_only=True), hide('output'):
        pci = run('lspci')
    _write_file('lspci', pci)


def df():
    """df -H"""
    with hide('output'):
        disk = run('df -H')
    _write_file('df-H', disk)


def fstab():
    """cat /etc/fstab"""
    with hide('output'):
        disk = run('cat /etc/fstab')
    _write_file('fstab', disk)


def delldisk():
    """omreport storage vdisk"""
    if files.exists('/opt/dell/srvadmin/bin/omreport'):
        with hide('output'):
            report = run('/opt/dell/srvadmin/bin/omreport storage vdisk')
        _write_file('omreport_storage_vdisk', report)


def lvm():
    """lvscan and pvscan"""
    with settings(warn_only=True):
        with hide('output'):
            lvs = run('lvscan')
        _write_file('lvscan', lvs)
        with hide('output'):
            pvs = run('pvscan')
        _write_file('pvscan', pvs)


def iptables():
    """iptables-save"""
    with settings(warn_only=True), hide('output'):
            tables = run('iptables-save')
    _write_file('iptables-save', tables)


def cron():
    """system crontab files"""
    hostname = env.hosts[env.host_string]
    _host_dir()
    if not os.path.isdir("output/{}/cron".format(hostname)):
        os.mkdir("output/{}/cron".format(hostname))
    with settings(warn_only=True), hide('output', 'warnings', 'running'):
        get('/etc/cron*', "output/{}/cron".format(hostname))
    with settings(warn_only=True), hide('output', 'warnings', 'running'):
        get('/var/spool/cron/*', "output/{}/cron".format(hostname))


def sysstat():
    """sysstat log files"""
    if files.exists('/var/log/sa'):
        hostname = env.hosts[env.host_string]
        _host_dir()
        if not os.path.isdir("output/{}/sysstat".format(hostname)):
            os.mkdir("output/{}/sysstat".format(hostname))
            with settings(warn_only=True), hide('output', 'warnings', 'running'):
                get('/var/log/sa/*', "output/{}/sysstat".format(hostname))


def user_list():
    """getent passwd"""
    with hide('output'):
        ulist = run('getent passwd')
        glist = run('getent group')
    _write_file('userlist', ulist)
    _write_file('grouplist', glist)


# @task(default=True)
def info():
    """everything"""
    print(env.hosts[env.host_string])
    date()
    release()
    uname()
    ip_a()
    netstat()
    ip_route()
    ip_rule()
    chkconfig()
    packages()
    ps_aux()
    free()
    cpuinfo()
    uptime()
    dmesg()
    dmidecode()
    lsmod()
    lspci()
    df()
    fstab()
    delldisk()
    lvm()
    iptables()
    cron()
    sysstat()
    user_list()
    print('all done')


def ping():
    """check host"""
    print(env.hosts[env.host_string])
    run('uptime')
