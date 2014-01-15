# Host Info Gatherer

gather host information using fabric.

## Requirements

  * [fabric](http://fabfile.org)
  * [python 2](http://python.org/)

## Examples

    fab host:127.0.0.1,localhost password info

    fab hostlist:list.csv dmesg
    
Output will be stored in `output/`. The directory is created in the cwd if it doesn't exist.
A subdirectory will be created for each host.
