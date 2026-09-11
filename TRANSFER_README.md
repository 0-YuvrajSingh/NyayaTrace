# Teammate transfer package

This ZIP64 archive contains the committed frozen source snapshot and the runtime assets needed to reproduce the project locally. Start by reading `config/reproducibility_freeze.json`, then compare the two critical SHA-256 values in `TRANSFER_MANIFEST.json`.

The archive deliberately does not contain credentials or a PostgreSQL provenance dump. Obtain `provenance.dump` separately and restore it using the supplied `compose.yaml` configuration. Do not overwrite the frozen 30-case answer key or historical result artifacts when conducting later work.
