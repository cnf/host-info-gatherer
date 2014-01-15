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
    """
    force the use of password prompt
    unsets everything ssh agent / keys related
    """
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
    """output of /etc/{redhat-release,debian_version,slackware-version}"""
    if files.exists('/etc/redhat-release'):
        with hide('output'):
            rel = run('cat /etc/redhat-release')
    elif files.exists('/etc/debian_version'):
        with hide('output'):
            rel = run('cat /etc/debian_version')
    elif files.exists('/etc/slackware-version'):
        with hide('output'):
            rel = run('cat /etc/slackware-version')
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
        with settings(warn_only=True):
            rule = run('ip rule show')
    _write_file('ip_rule_show', rule)


def netstat():
    """netstat -neltup"""
    with hide('output'):
        na = run('netstat -neltup')
    _write_file('netstat-nltup', na)


def ss():
    """ss; ss -s"""
    with hide('output'):
        sss = run('ss -s')
    _write_file('ss-s', sss)
    with hide('output'):
        ssp = run('ss')
    _write_file('ss', ssp)


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


def mount():
    """mount"""
    with hide('output'):
        mnt = run('mount')
    _write_file('mount', mnt)


def fstab():
    """cat /etc/fstab"""
    with hide('output'):
        disk = run('cat /etc/fstab')
    _write_file('fstab', disk)

def mdstat():
    """cat /proc/mdstat"""
    if files.exists('/proc/mdstat'):
        with hide('output'):
            mdstat = run('cat /proc/mdstat')
        _write_file('mdstat', mdstat)

def delldisk():
    """omreport storage vdisk"""
    if files.exists('/opt/dell/srvadmin/bin/omreport'):
        with hide('output'):
            report = run('/opt/dell/srvadmin/bin/omreport storage vdisk')
        _write_file('omreport_storage_vdisk', report)


def lvm():
    """lvscan and pvscan"""
    # TODO: vgs, pvs, lvs
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
            with settings(warn_only=True), hide('warnings', 'running'):
                get('/var/log/sa/*', "output/{}/sysstat".format(hostname))


def user_list():
    """getent passwd"""
    with hide('output'):
        ulist = run('getent passwd')
    _write_file('userlist', ulist)
    with hide('output'):
        glist = run('getent group')
    _write_file('grouplist', glist)


def netlink():
    """mii-tool or ethtool"""
    """dmesg | grep -i duplex fallback?"""
    pass


def last():
    """w;last"""
    with hide('output'):
        lst = run('last')
    _write_file('last', lst)
    with hide('output'):
        who = run('w')
    _write_file('w', who)


def history():
    """history"""
    with hide('output'):
        lst = run('last')
    _write_file('last', lst)

def hostname():
    """hostname"""
    with settings(warn_only=True), hide('output'):
        realname = run('hostname')
        realfqdn = run('hostname -f')
    realhostname = "hostname: "+realname+"\nhostname -f: "+realfqdn+"\n"
    _write_file('hostname', realhostname)

def htop():
    """htop"""
    pass


def sysctl():
    """sysctl -a"""
    with hide('output'):
        sctl = run('sysctl -a')
    _write_file('sysctl', sctl)


def logs():
    """/var/log..."""
    if files.exists('/var/log'):
        hostname = env.hosts[env.host_string]
        _host_dir()
        if not os.path.isdir("output/{}/logs".format(hostname)):
            os.mkdir("output/{}/logs".format(hostname))
    loglist = ['messages', 'auth.log', 'libvirt/libvirtd.log',
               'logstash/logstash-indexer.log']
    for log in loglist:
        if files.exists('/var/log/{}'.format(log)):
            with settings(warn_only=True), hide('warnings', 'running'):
                get('/var/log/{}'.format(log),
                    "output/{}/logs/{}".format(hostname, log))


# @task(default=True)
def info():
    """everything"""
    print(env.hosts[env.host_string])
    date()
    hostname()
    release()
    uname()
    ip_a()
    netlink()
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
    mount()
    fstab()
    delldisk()
    lvm()
    iptables()
    cron()
    sysstat()
    sysctl()
    user_list()
    ss()
    mdstat()
    print('all done')


def debug():
    """server debug"""
    """
    http://devo.ps/blog/2013/03/06/troubleshooting-5minutes-on-a-yet-unknown-box.html
    """
    # TODO: FS read actions last
    last()
    history()
    ps_aux()
    netstat()
    free()
    uptime()
    htop()
    lspci()
    dmidecode()
    netlink()
    # cat /etc/apt/sources.list
    # iostat -kx 1 1
    # vmstat 2 10
    # mpstat 2 10
    # dstat --top-io --top-bio
    mount()
    fstab()
    df()
    # lsof +D / ????
    sysctl()
    # cat /proc/interrupts
    # cat /proc/net/ip_conntrack
    ss()
    dmesg()
    cron()
    logs()


def ping():
    """check host"""
    print(env.hosts[env.host_string])
    run('uptime')
