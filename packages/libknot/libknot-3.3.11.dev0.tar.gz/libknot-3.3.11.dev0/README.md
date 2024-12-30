# Libknot API in Python

A Python interface for managing the Knot DNS daemon.

# Table of contents

* [Introduction](#introduction)
* [Control module](#control-module)
  + [Control usage](#control-usage)
  + [CTL protocol reference](#kctl-proto)
  + [CTL commands reference](#kctl-cmds)
  + [Control examples](#control-examples)
* [Probe module](#probe-module)
  + [Probe usage](#probe-usage)
  + [Probe examples](#probe-examples)
* [Dname module](#dname-module)
  + [Dname usage](#dname-usage)
  + [Dname examples](#dname-examples)

## Introduction<a id="introduction"></a>

If the shared `libknot.so` library isn't available in the library search path, it's
necessary to load the library first, e.g.:

```python3
import libknot
libknot.Knot("/usr/lib/libknot.so")
```

## Control module<a id="control-module"></a>

Using this module it's possible to create scripts for efficient tasks that
would require complex shell scripts with multiple calls of `knotc`. For
communication with the daemon it uses the same mechanism as the `knotc` utility,
i.e. communication via a Unix socket.

The module API is stored in `libknot.control`.

### Control usage<a id="control-usage"></a>

The module usage consists of several steps:

* Initialization and connection to the daemon control socket.
* One or more control operations. An operation is called by sending a command
  with optional data to the daemon. The operation result has to be received
  afterwards.
* Closing the connection and deinitialization.

### KnotCTL protocol overview<a id="kctl-proto"></a>

Connections are supposed to be short-lived, because maintaining a passive
connection is costly for the server. Therefore the expected usage of the ctl
interface is to always open a new connection on demand, then close it once it's
not immediately needed.

Messages are composed of units. These are of four types whose identifiers are
defined in `libknot.control.KnotCtlType`:

| Type    | Description                                                | IO action |
| ------- | ---------------------------------------------------------- | --------- |
| `END`   | Signals intent to terminate connection.                    | flush     |
| `DATA`  | Holds various information - see about data sections below. | cache     |
| `EXTRA` | Additional data.                                           | cache     |
| `BLOCK` | End of data block.                                         | flush     |

A unit can optionaly hold data, though this is only meaningful for the `DATA`
and `EXTRA` types. The data consists of several sections of which usually only
a few at a time will be present. For example when a unit issuing a `stats`
command is sent, there is no reason for it to contain an `ERROR` section.

The data section identifiers are defined in `libknot.control.KnotCtlDataIdx`:

| Section name | Description                                            |
| ------------ | ------------------------------------------------------ |
| `COMMAND`    | Command name.                                          |
| `FLAGS`      | Command flags.                                         |
| `ERROR`      | Error message.                                         |
| `SECTION`    | Configuration section name.                            |
| `ITEM`       | Configuration item name.                               |
| `ID`         | Configuration item identifier.                         |
| `ZONE`       | Zone name.                                             |
| `OWNER`      | Zone record owner                                      |
| `TTL`        | Zone record TTL.                                       |
| `TYPE`       | Zone record type name.                                 |
| `DATA`       | Configuration item/zone record data.                   |
| `FILTERS`    | Command options or filters for output data processing. |

### CTL commands reference<a id="kctl-cmds"></a>

The following is a reference for the low-level CTL API. In case you're unsure
of the commands' semantics, please consult the
<a href="https://knot.pages.nic.cz/knot-dns/master/html/man_knotc.html#actions">knotc documentation</a>.

A concise notation is used for command synopsis:

<pre>
cmd-name(SECTION_NAME:<i>section's purpouse</i>,
    [OPTIONAL_SECTION=<b>"literal value"</b><i>:literal's purpouse</i>],
    [OPT_SECTION1, OPT_SECTION2],      <i># Sections must be present together or not at all</i>
    [OPT_MASTER, [OPT_SLAVE]],         <i># OPT_SLAVE may only appear if OPT_MASTER is present</i>
    SECTION_NAME2=<b>"option1"</b>|<b>"option2"</b>, <i># Either one or the other literal may be used</i>
    SECTION_NAME3={<b>"asdf"</b>},            <i># any subset of characters</i>
    SECTION_NAME4={<b>"a"</b><i>:flag's purpouse</i>,<b>"s"</b>,<b>"d"</b>,<b>"f"</b>} <i># any subset of characters</i>
)
</pre>

The **`"B"`** flag always represents an option to execute in blocking mode.

#### Server

* `status([TYPE=`<b>`"cert-key"`</b>`|`<b>`"configure"`</b>`|`<b>`"version"`</b>`|`<b>`"workers"`</b>`])`
* `stop()`
* `reload()`
* `stats([SECTION:`<i>`module`</i>`], [ITEM:`<i>`counter`</i>`], [FLAGS=`<b>`"F"`</b>`:`<i>`include 0 counters`</i>`])`

#### Zone events

`ZONE`: if none applies to all zones

* `zone-status([ZONE], [FILTERS={`<b>`"rstefc"`</b>`}])`
  + `FILTERS`: role `(r)`, serial `(s)`, transaction `(t)`, events `(e)`, freeze `(f)`, catalog `(c)`
* `zone-reload([ZONE], [FLAGS=`<b>`"B"`</b>`,`<b>`"F"`</b><i>`:reload modules`</i>`])`
* `zone-refresh([ZONE], [FLAGS=`<b>`"B"`</b>`])`
* `zone-retransfer([ZONE], [FLAGS=`<b>`"B"`</b>`])`
* `zone-notify([ZONE], [FLAGS=`<b>`"B"`</b>`])`
* `zone-flush([ZONE], [FILTERS=`<b>`"d"`</b><i>`:specify output directory`</i>`, DATA:`<i>`output directory`</i>`], [FLAGS=`<b>`"B"`</b>`])`
* `zone-backup([ZONE], [FILTERS={`<b>`"dzjtkocq"`</b>`}, [DATA:`<i>`if "d" filter present; output directory`</i>`]], [FLAGS=`<b>`"B"`</b>`])`
  + `FILTERS`
	- zonefile `(z)`, journal `(j)`, timers `(t)`, kaspdb `(k)`, keysonly `(o)`, catalog `(c)`, quic `(q)`
	- negative counterparts (eg. `nozonefile`) are symmetrical and capitalized
* `zone-restore` <i>analogous to `zone-backup`</i>
* `zone-sign([ZONE], [FLAGS=`<b>`"B"`</b>`])`
* `zone-validate([ZONE], [FLAGS=`<b>`"B"`</b>`])`
* `zone-keys-load([ZONE], [FLAGS=`<b>`"B"`</b>`])`
* `zone-key-rollover([ZONE], TYPE=`<b>`"ksk"`</b>`|`<b>`"zsk"`</b>`, [FLAGS=`<b>`"B"`</b>`])`
* `zone-ksk-submitted([ZONE], [FLAGS=`<b>`"B"`</b>`])`
* `zone-freeze([ZONE], [FLAGS=`<b>`"B"`</b>`])`
* `zone-thaw([ZONE], [FLAGS=`<b>`"B"`</b>`])`
* `zone-xfr-freeze([ZONE], [FLAGS=`<b>`"B"`</b>`])`
* `zone-xfr-thaw([ZONE], [FLAGS=`<b>`"B"`</b>`])`

#### Zone editing

Use `"@"` as `OWNER` if you want to denote `ZONE` itself as the owner.

* `zone-read([ZONE`<i>`:if none read all`</i>`], [OWNER], [TYPE])`
* `zone-begin(ZONE)`
* `zone-commit(ZONE)`
* `zone-abort(ZONE)`
* `zone-diff(ZONE)`
* `zone-get(ZONE, [OWNER], [TYPE])` <!-- TODO: test if OWNER and TYPE may be specified independently -->
* `zone-set(ZONE, OWNER, [TTL], TYPE, DATA)`
* `zone-unset(ZONE, OWNER, [TYPE, [DATA]])`
* `zone-purge(ZONE, [FILTERS={`<b>`"o"`</b>`:orphan,`<b>`"c"`</b>`:catalog,`<b>`"e"`</b>`:expire,`<b>`"j"`</b>`:journal,`<b>`"k"`</b>`:kaspdb,`<b>`"t"`</b>`:timers,`<b>`"f"`</b>`:zonefile}], [FLAGS=`<b>`"B"`</b>`])`
* `zone-stats(ZONE, [SECTION`<i>`:module`</i>`], [ITEM`<i>`:counter`</i>`], [FLAGS=`<b>`"F"`</b>`:`<i>`include 0 counters`</i>`])`

#### Configuration

optional list schema option ('s') in FILTERS <!-- TODO: k cemu to je? -->

* `conf-list([SECTION, [ITEM], [ID]], [FILTERS=`<b>`"s"`</b>`])`
* `conf-read([SECTION, [ITEM], [ID]])`
* `conf-begin()`
* `conf-commit()`
* `conf-abort()`
* `conf-diff([SECTION, [ITEM], [ID]])`
* `conf-get([SECTION, [ITEM], [ID]])`
* `conf-set(SECTION, ITEM, ID, [DATA], [FILTERS=`<b>`"s"`</b>`])`
* `conf-unset([SECTION, [ITEM], [ID]], [DATA])`

### Control examples<a id="control-examples"></a>

```python3
import json
import libknot.control

# Initialization
ctl = libknot.control.KnotCtl()
ctl.connect("/var/run/knot/knot.sock")
ctl.set_timeout(60)

try:
    # Operation without parameters
    ctl.send_block(cmd="conf-begin")
    resp = ctl.receive_block()

    # Operation with parameters
    ctl.send_block(cmd="conf-set", section="zone", item="domain", data="test")
    resp = ctl.receive_block()

    ctl.send_block(cmd="conf-commit")
    resp = ctl.receive_block()

    # Operation with a result displayed in JSON format
    ctl.send_block(cmd="conf-read", section="zone", item="domain")
    resp = ctl.receive_block()
    print(json.dumps(resp, indent=4))
except libknot.control.KnotCtlError as exc:
    # Print libknot error
    print(exc)
finally:
    # Deinitialization
    ctl.send(libknot.control.KnotCtlType.END)
    ctl.close()
```

```python3
    # List configured zones (including catalog member ones)
    ctl.send_block(cmd="conf-list", filters="z")
    resp = ctl.receive_block()
    for zone in resp['zone']:
        print(zone)
```

```python3
    # Print expirations as unixtime for all secondary zones
    ctl.send_block(cmd="zone-status", filters="u")
    resp = ctl.receive_block()
    for zone in resp:
        if resp[zone]["role"] == "master":
            continue

        expiration = resp[zone]["expiration"]
        if expiration == "-":
            print("Zone %s not loaded" % zone)
        else:
            print("Zone %s expires at %s" % (zone, resp[zone]["expiration"]))
```

## Probe module<a id="probe module"></a>

Using this module it's possible to receive traffic data from a running daemon with
active probe module.

The module API is stored in `libknot.probe`.

### Probe usage<a id="probe-usage"></a>

The module usage consists of several steps:

* Initialization of one or more probe channels
* Periodical receiving of data units from the channels and data processing

### Probe examples<a id="probe-examples"></a>

```python3
import libknot.probe

# Initialization of the first probe channel stored in `/run/knot`
probe = libknot.probe.KnotProbe("/run/knot", 1)

# Array for storing up to 8 data units
data = libknot.probe.KnotProbeDataArray(8)
while (True):
    # Receiving data units with timeout of 1000 ms
    if probe.consume(data, 1000) > 0:
        # Printing received data units in the default format
        for item in data:
            print(item)
```

## Dname module<a id="dname-module"></a>

This module provides a few dname-related operations.

The module API is stored in `libknot.dname`.

### Dname usage<a id="dname-usage"></a>

The dname object is initialized from a string with textual dname.
Then the dname can be reformatted to wire format or back to textual format.

### Dname examples<a id="dname-examples"></a>

```python3
import libknot.dname

dname1 = libknot.dname.KnotDname("knot-dns.cz")
print("%s: wire: %s size: %u" % (dname1.str(), dname1.wire(), dname1.size()))

dname2 = libknot.dname.KnotDname("e\\120ample.c\om.")
print("%s: wire: %s size: %u" % (dname2.str(), dname2.wire(), dname2.size()))

dname3 = libknot.dname.KnotDname(dname_wire=b'\x02cz\x00')
print("%s: wire: %s size: %u" % (dname3.str(), dname3.wire(), dname3.size()))
```

```bash
knot-dns.cz.: wire: b'\x08knot-dns\x02cz\x00' size: 13
example.com.: wire: b'\x07example\x03com\x00' size: 13
cz.: wire: b'\x02cz\x00' size: 4
```
