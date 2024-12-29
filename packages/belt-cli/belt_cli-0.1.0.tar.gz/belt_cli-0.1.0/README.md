# `belt`: a cli toolbox

## Language

Python 3.12

## Args and flags

### Universal flags

| Full flag               | Abbreviation  |
| ----------------------- | ------------- |
| `--config` `FILE`       | `-c` `FILE`   |
| `--env-prefix` `PREFIX` | `-e` `PREFIX` |
| `--help`                | `-h`          |
| `--in` `FILE`           | `-i` `FILE`   |
| `--out` `FILE`          | `-o` `FILE`   |
| `--verbose`             | `-v`          |
| `--version`             | `-V`          |

### Functionality selection

| Command  | Subcommand  | Function   | Positional           | Params                                      |
| -------- | ----------- | ---------- | -------------------- | ------------------------------------------- |
| `audio`  | `info`      |            |                      |                                             |
| `crypt`  | `rand`      | `char`     | `LENGTH`             |                                             |
| `crypt`  | `rand`      | `hex`      | `LENGTH`             |                                             |
| `crypt`  | `rand`      | `pw`       | `LENGTH`             |                                             |
| `crypt`  | `simple`    | `dec`      |                      | `-e`, `--env` `VAR` Use passphrase from env |
| `crypt`  | `simple`    | `enc`      |                      | `-e`, `--env` `VAR` Use passphrase from env |
| `crypt`  | `wireguard` |            |                      |                                             |
| `dns`    | `flush`     |            |                      |                                             |
| `dns`    | `lookup`    |            | `QUERY [RECORDTYPE]` | `-s`, `--server` `HOSTNAME` Use server      |
|          |             |            |                      | `-r`, `--root` Use root servers             |
| `dns`    | `sec`       |            | `DOMAIN.TLD`         |                                             |
| `tls`    | `cert`      | `req`      | `COMMONNAME`         | `-c`, `--client` Request client cert        |
| `tls`    | `cert`      | `selfsign` | `COMMONNAME`         | `-c`, `--client` Generate client cert       |
| `tls`    | `ciphers`   |            | `HOSTNAME` `PORT`    |                                             |
| `domain` | `expiry`    |            | `DOMAIN.TLD`         |                                             |
| `domain` | `ns`        |            | `DOMAIN.TLD`         |                                             |

## Features

### 1.0

- DNS
  - Lookup
  - DNSSEC check
    - Remediation instructions
  - OS cache flush
- TLS
  - Cipher list and order
  - Certificate generation
    - All features for client or server certificate
    - Self signed
    - Certificate request
- Cryptography
  - Simple encrypt/decrypt
    - Password from readline or env var
  - Generate WireGuard keypair
  - Random generation
    - Alphanumeric + symbols
    - Alphanumeric
    - Alphabetical
    - Numeric
    - Hex
    - 0x prefixed hex
- Domain
  - Time to expiry from WHOIS
  - Nameserver lookup from WHOIS
- Audio files
  - Get sample rate and bit depth

### Planned

- Git
  - Clone
  - Pull
  - Push
  - Branch
  - Detect remote changes
- SSH
  - Tunnels
  - Connections
  - Config management
  - Cipherspec validation
    - Remediation
- DNS
  - Propagation checks
    - Multiple public resolvers
- Cloudflare
  - Clear cache
- Workspace
  - Replicate `ws` functionality
