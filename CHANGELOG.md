Version ? (Status: DEVELOPMENT)
* Fix issue #24 (nafsdm-webinterface password resets on upgrade)
* Add slavestatus page to nafsdm-webinterface.
* New bootstrap theme for webinterface
* New index for webinterface (domains separate page, index has system status/health)

Version 1.3.1 (Status: RELEASED)
* Bugfix: Slaves reported incorrect date to nafsdmctl slavestatus (minute instead of month under the "latest connection date" section)
* Slaves now check if another nafsdm-slave process is running before boot
* Fix issue #22
* Visual adjustments to the upgrade scripts.
* (minor): Slaves properly catch SIGINT and SIGTERM to exit gracefully
* (minor): Updated nafsdm-slave systemd service to only start after internet connection is available
* (minor): CHANGELOG is now included in install

Version 1.3 (Status: RELEASED)
* Upgrade scripts now check for "github_branch" to download correct latest version file.
* Upgrade scripts now return different exit codes depending on issue (dev versions will no longer crash the daemon due to unsupported version)
* Complete visual overhaul of nafsdmctl (looks a lot nicer)
* New development mode, allowing latest commit to always be installed on master and slave (not set version numbers).
* Slave: development functions are now enabled using the config.conf instead of adding files.
* Developer mode introduced in version 1.2.5-stable has been renamed to "skipVersionCheck"
* nafsdmctl: now has remove by domain and remove by ID functions
* nafsdmctl: now has status/start/stop/restart functions for the webinterface
* Slaves now report last connection time to master (nafsdmctl can show a table of which slaves has connected recently)
* nafscli logviewer no longer throws a traceback message on exit (using CTRL+C)
* Rewrote most log messages for both master and slave
* Ability to enable or disable nafsdm upgrades on start (if turned off, you will have to use nafscli upgrade) on slave daemon
* nafscli status now has -a argument which shows the full systemd status of the nafsdm daemon
* (minor): Update all copyright notices to 2018

Version 1.2.5 (Status: RELEASED)
* Added nafscli for the slave, a command-line interface
* Added developer mode for both Slave and Master (disables version checking)

Version 1.2.4 (Status: RELEASED)
* experimental: webinterface for the master, allowing control from a browser
* Slaves now check if their version matches with the one the master is running
Smaller changes/bugfixes:
* Remove double import of sys in nafsdmctl
* Added extra script to check if nafsdm is running (should work with monitoring software like nagios)
* Nicer looking setup scripts
* Installer now installs pip libs using a requirements.txt file (and updater).

Version 1.2.3 (Status: RELEASED)
* nafsdm-master now uses SQL to save domains (updated nafsdmctl and slave with the new save format)
* nafsdmctl list now prints in a nicer format
(from dev2)
* Bugfixes for dev1 issues (which need to be retested, therefore new dev release)

Version 1.2.2 (Status: RELEASED)
* Reworked logger function completely (now catches exceptions, new logging levels, stdout and filehandler)
* Small changes

Version 1.2.1 (Status: RELEASED)
* Development feature: specifiy GitHub branch to use
* Issue #8 fixed (nafsdm-slave not start on boot)
* Issue #11 fixed (nafsdmctl editor open causing slaves to crash).
* Issue #12 fixed (CTRL+C in nafsdmctl edit).
(from dev2)
* Remove non-working fix for issue #8.
* New fix for issue #8.
(from dev3, not released we just go straight to stable)
* New fix for issue #8
* Issue #11 silly fix

Version 1.2 (Status: RELEASED)
* Added DNSSEC support.
* Added upgrade scripts.
* Added support for automatic upgrades (1.2 and forwards)
* New edit function for nafsdmctl (master).
(from 1.2-dev3):
* Tons of bugfixes from 1.2-dev2. See release notes.

Version 1.1 (Status: RELEASED)
* New version files.
* New config parsing.
* Setup scripts has new version selection (and another fix on that since 1.1-dev2)
* Minor bug/spell fixes in master aswell as slave config changed (section name)

Version 1.0.1-stable (Status: RELEASED)
* Slave: Fixed serious writing issue where ' is used instead of ".
* Slave: Updated hostname finding function.

Version 1.0 (Status: RELEASED, now UNSTABLE)
* First version.
