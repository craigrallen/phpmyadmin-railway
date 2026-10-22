# TECH-84 PHP admin image pins

This companion change pins only the declared admin sidecar images. No application
runtime pins, Composer/npm locks, app code, ports, environment, security settings,
volumes, ENTRYPOINT or CMD bytes are changed. Commented declarations stay commented.

The controller supplied these immutable references and isolated native PHP CLI
results; this work did not independently build or execute any image:
- Adminer: PHP 8.4.27.
- LinuxServer phpMyAdmin: PHP 8.5.12.
- Official phpMyAdmin: PHP 8.3.36.

Exact references and original image declarations are in
`scripts/check_php_admin_images.py`. LinuxServer and official vendor families
remain distinct; the deprecated `phpmyadmin/phpmyadmin` alias, where present,
becomes the official `phpmyadmin` image.

Run with Python 3.9+ and no dependencies:
```sh
python3 -B scripts/test_php_admin_images.py
python3 -B scripts/check_php_admin_images.py
git diff --check
```
Tests reject missing, old, floating, wrong-family, wrong-digest and duplicate
declarations and accept the declared pins. The inverse test restores only the
original image lines and compares SHA-256 with the real clean baseline captured
before editing. Baseline commit: 27a894ed0d266db58a7c60d50eb9743fe77de3d6.
It deliberately fails if any other bytes in these scoped files change; legitimate
future edits require separately reviewing and refreshing that baseline evidence.
The guard checks exact declaration positions and spelling, including commented
examples, without loading YAML, dotenv, credentials or application configuration.
Actual RED and GREEN command receipts are in `evidence/TECH-84-red.txt` and
`evidence/TECH-84-green.txt`.

An immutable image is not configured-application or deployed-target acceptance.
Rebuilding derived images or moving from a previous/default `latest` image may
change the vendor application version even when the PHP version is acceptable.
The controller/operator must independently verify image provenance, target
architecture, vendor application version and compatibility, backups and restore,
configuration, and staged rollout/rollback before accepting any target.
No image entrypoint, application, real database login or live target ran here.
No live target is claimed patched. Review, builds, native checks, commits, PRs
and rollout belong to the controller.

## External vendor: LOCAL PATCH ONLY

Upstream permissions are pull=true, push=false. No push, fork, image publication
or ownership change is authorized. No upstream workflow is added.
`evidence/TECH-84-owner.patch` contains the Dockerfile edit and offline tests,
docs and receipts for owner review. From the recorded clean baseline, run
`git apply --check /path/to/TECH-84-owner.patch` then
`git apply /path/to/TECH-84-owner.patch`. This checkout already has the edits.
The existing custom entrypoint, CMD and inherited port contract are preserved
in source; the changed upstream image still needs operator contract verification.
This runtime feeds two Railway targets; neither has been changed or validated.
