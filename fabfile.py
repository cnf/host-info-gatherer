#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gather host information
fab host:127.0.0.1,localhost password info
fab host:127.0.0.1,localhost username:demo debug
fab hostlist:list.csv dmesg
"""

__author__ = "Frank Rosquin <frank@rosquin.net>"
__copyright__ = "Copyright 2013, Frank Rosquin"

__license__ = "ISC"
__maintainer__ = "Frank Rosquin"
__email__ = "frank@rosquin.net"

from fabric.api import env, settings, hide, run, sudo, get, runs_once
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
    # lsb-release?
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
        with settings(warn_only=True):
            ipa = run('ip a')
        if ipa.succeeded:
            _write_file('ip_a', ipa)
        else:
            with settings(warn_only=True):
                ipa = run('ifconfig')
            _write_file('ifconfig', ipa)


def ip_route():
    """ip route show table all"""
    with hide('output'):
        with settings(warn_only=True):
            route = run('ip route show table all')
        if route.succeeded:
            _write_file('ip_route_show_table_all', route)
        else:
            with settings(warn_only=True):
                route = run('netstat -nr')
            _write_file('netstat -nr', route)


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
        dmi = sudo('dmidecode')
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
            lvs = sudo('lvscan')
        _write_file('lvscan', lvs)
        with hide('output'):
            pvs = sudo('pvscan')
        _write_file('pvscan', pvs)


def iostat():
    """iostat -kx 2"""
    with settings(warn_only=True):
        with hide('output'):
            iostat = run('iostat -kx 2')
        _write_file('iostat', iostat)


def vmstat():
    """vmstat"""
    with settings(warn_only=True):
        with hide('output'):
            vmstat = run('vmstat')
        _write_file('vmstat', vmstat)


def mpstat():
    """mpstat"""
    with settings(warn_only=True):
        with hide('output'):
            mpstat = run('mpstat')
        _write_file('mpstat', mpstat)


def dstat():
    """dstat --top-io --top-bio"""
    with settings(warn_only=True):
        with hide('output'):
            dstat = run('dstat --top-io --top-bio')
        _write_file('dstat', dstat)


def iptables():
    """iptables-save"""
    with settings(warn_only=True), hide('output'):
            tables = run('iptables-save')
    _write_file('iptables-save', tables)


def conntrack():
    """ip_conntrack or nf_conntrack"""
    with hide('output'):
        if files.exists('/proc/net/nf_conntrack'):
            conntrack = run('cat /proc/net/nf_conntrack')
            _write_file('conntrack', conntrack)
        elif files.exists('/proc/net/ip_conntrack'):
            conntrack = run('cat /proc/net/ip_conntrack')
            _write_file('conntrack', conntrack)


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
    # TODO: dmesg | grep -i duplex fallback?
    with hide('output'):
        with settings(warn_only=True):
            mii = sudo('mii-tool')
        _write_file('mii-tool', mii)
        with settings(warn_only=True):
            ethtool = sudo('ethtool')
        _write_file('ethtool', ethtool)


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
    # TODO: ...
    pass


def sysctl():
    """sysctl -a"""
    with hide('output'):
        sctl = run('sysctl -a')
    _write_file('sysctl', sctl)


def procinterrupts():
    if files.exists('/proc/interrupts'):
        with hide('output'):
            intr = run('cat /proc/interrupts')
        _write_file('proc_interrupts', intr)


def apt():
    """ apt-sources and packages"""
    if files.exists('/etc/apt'):
        hostname = env.hosts[env.host_string]
        with hide('output'):
            get('/etc/apt', "output/{}/".format(hostname))
    pass


def logs():
    """/var/log..."""
    if files.exists('/var/log'):
        hostname = env.hosts[env.host_string]
        _host_dir()
        if not os.path.isdir("output/{}/logs".format(hostname)):
            os.mkdir("output/{}/logs".format(hostname))
    loglist = ['messages', 'syslog', 'auth', 'auth.log', 'secure',
               'libvirt/libvirtd.log', 'logstash/logstash-indexer.log']
    for log in loglist:
        if files.exists('/var/log/{}'.format(log)):
            with settings(warn_only=True), hide('warnings', 'running'):
                get('/var/log/{}'.format(log),
                    "output/{}/logs/{}".format(hostname, log))


# @task(default=True)
def info():
    """everything"""
    print(env.hosts[env.host_string])
    # system info
    date()
    hostname()
    release()
    last()
    uname()
    history()
    ps_aux()

    # network
    ip_a()
    netlink()
    netstat()
    ip_route()
    ip_rule()
    iptables()
    ss()

    chkconfig()
    packages()
    apt()

    free()
    cpuinfo()
    uptime()
    htop()
    dmesg()

    # hardware
    dmidecode()
    lsmod()
    lspci()
    df()
    mount()
    fstab()
    delldisk()
    lvm()
    df()
    mdstat()

    # IO
    iostat()
    vmstat()
    mpstat()
    dstat()

    cron()
    sysstat()
    sysctl()
    procinterrupts()
    user_list()
    logs()
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

    free()
    uptime()
    htop()

    lspci()
    dmidecode()
    netlink()

    # IO
    iostat()
    vmstat()
    mpstat()
    dstat()

    # disks and FS
    mount()
    fstab()
    df()
    lvm()
    # lsof +D / ????

    sysctl()
    procinterrupts()

    # network
    conntrack()
    iptables()
    netstat()
    ss()

    apt()

    # logs etc
    dmesg()
    cron()
    logs()


def ping():
    """check host"""
    print(env.hosts[env.host_string])
    run('uptime')
