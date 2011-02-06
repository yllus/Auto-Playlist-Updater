AUTO PLAYLIST UPDATER 0.1 INSTALLATION INSTRUCTIONS

1. Install the included Python package for the fun_plug:

	funpkg -i Python-2.5.2-2.tgz

   Note: More recent versions of Python for fun_plug can be found at:

	http://81.216.140.39/dns-323/denyhosts/

2. ?

X. Add a recurring scheduled job to the DNS-323 to scan for new files by adding the below as the very last line of the file /mnt/HD_a2/fun_plug:

	echo '*/10 * * * * /ffp/bin/python /ffp/sbin/autoplaylistupdater/autoplaylistupdater.py' > /var/spool/cron/crontabs/root