#!/usr/bin/env python3

import dns.resolver
import netaddr
import collections
import json
import argparse


def get_dns():
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    answers = my_resolver.query("locations.publicdns.goog", "TXT")

    dns_prefixes = collections.defaultdict(list)
    for rdata in answers:
        for b in rdata.strings:
            s = b.decode('utf-8')
            prefix = netaddr.IPNetwork(s.split()[0])
            site = s.split()[1]
            dns_prefixes[site].append(prefix)

    return dns_prefixes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--listonly", action="store_true", default=False,
                        help="Only provide a JSON list of addresses")
    parser.add_argument("--csvlistonly", action="store_true", default=False,
                        help="Only provide a CSV list of addresses")
    parser.add_argument("--noagg", action="store_true", default=False,
                        help="Do not attempt to aggregate prefixes")
    parser.add_argument("--ipv6brackets", action="store_true", default=False,
                        help="A compatibility hack for tools that needs IPv6 prefixes in RFC4038 format")

    args = parser.parse_args()

    dns_prefixes = get_dns()
    agg_dns_prefixes = {}

    for k, v in dns_prefixes.items():
        if args.noagg:
            if args.ipv6brackets:
                agg_dns_prefixes[k] = [f"[{str(i.ip)}]/{i.prefixlen}" if i.version == 6 else str(i) for i in v]
            else:
                agg_dns_prefixes[k] = [str(i) for i in v]
        elif not args.noagg:
            if args.ipv6brackets:
                agg_dns_prefixes[k] = [f"[{str(i.ip)}]/{i.prefixlen}" if i.version == 6 else str(i) for i in netaddr.cidr_merge(v)]
            else:
                agg_dns_prefixes[k] = [str(i) for i in netaddr.cidr_merge(v)]


    if args.csvlistonly or args.listonly:
        output_lists = agg_dns_prefixes.values()
        output_list = []
        for i in output_lists:
            output_list.extend(i)

        if args.listonly:
            print(json.dumps(output_list))

        if args.csvlistonly:
            print(",".join(output_list))

    else:
        print(json.dumps(agg_dns_prefixes))
