Purpose
=======

To use Google's TXT records to get a list of the backend addresses of the servers that power Google Public DNS, and to turn them into formats useful for further automation.

For more information on option details see --help.

Examples
========

Return a JSON object mapping location codes to aggregated prefixes.

```
$ python gpdns2json.py
{"iad": ["74.125.18.0/25", "172.253.8.0/23", "172.253.10.0/24", "173.194.168.192/26", "[2607:f8b0:4004::]/52"], "syd": ["74.125.18.128/26", "172.217.33.0/25", "[2404:6800:4006::]/48"] ...
```

Return a JSON formatted list with all the prefixes used by Google, aggregated.

```
$ python gpdns2json.py --listonly
["74.125.18.0/25", "172.253.8.0/23", "172.253.10.0/24", "173.194.168.192/26", "2607:f8b0:4004::/52" ...
```

Return a JSON formatted list with all the prefixes used by Google, NOT aggregated.

```
$ python gpdns2json.py --listonly
["74.125.18.0/25", "172.253.8.0/24", "172.253.9.0/24", "172.253.10.0/24", "173.194.168.192/26", "2607:f8b0:4004::/52" ...
```

Return a CSV list of all the prefixes used by Google with RFC4038 style IPv6 prefix formatting.

```
$ python gpdns2json.py --csvlistonly --ipv6brackets
74.125.18.0/25,172.253.8.0/23,172.253.10.0/24,173.194.168.192/26,[2607:f8b0:4004::]/52
```

Bugs
====

* Only uses IPv4 transport for the DNS lookup.
* Forces itself to use Google itself (8.8.8.8 / 8.8.4.4) to get this data. This minimises bugs with local resolvers not doing TCP or EDNS0 big packets (Hello Sky Broadband !), but the user should get the choice via a CLI argument.
