Version 1.2.3 (Status: DEVELOPMENT)
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
