# neon-phal-plugin-system

Provides system specific commands to Neon.
The dbus interface for this plugin is not yet established.

# Install

`pip install neon-phal-plugin-system`

# Config

This plugin is an Admin plugin, it needs to run as root and to be explicitly enabled in mycroft.conf

```yaml
PHAL:
  admin:
    neon-phal-plugin-system:
      enabled: true
```
