import { lookup } from 'node:dns';
import { Agent } from 'node:https';
import { BlockList, isIP } from 'node:net';

const blocked = new BlockList();
for (const [address, prefix] of [['0.0.0.0', 8], ['10.0.0.0', 8], ['100.64.0.0', 10], ['127.0.0.0', 8],
  ['169.254.0.0', 16], ['172.16.0.0', 12], ['192.0.0.0', 24], ['192.0.2.0', 24], ['192.168.0.0', 16],
  ['198.18.0.0', 15], ['198.51.100.0', 24], ['203.0.113.0', 24], ['224.0.0.0', 4], ['240.0.0.0', 4]]) blocked.addSubnet(address, prefix, 'ipv4');
const globalV6 = new BlockList();
globalV6.addSubnet('2000::', 3, 'ipv6');
for (const [address, prefix] of [['2001::', 32], ['2001:db8::', 32], ['2002::', 16]]) blocked.addSubnet(address, prefix, 'ipv6');

export function isPublicPushAddress(address) {
  const family = isIP(address);
  if (family === 4) return !blocked.check(address, 'ipv4');
  return family === 6 && globalV6.check(address, 'ipv6') && !blocked.check(address, 'ipv6');
}

// Accept browser-issued provider URLs without a vendor list. Resolve and pin a
// public address at connection time, so arbitrary subscriptions cannot reach
// loopback, LAN, cloud metadata or DNS-rebinding targets. web-push does not follow redirects.
export function publicPushLookup(resolve = lookup) {
  return (hostname, options, callback) => {
    resolve(hostname, { all: true, verbatim: true }, (error, addresses) => {
      if (error) return callback(error);
      if (!addresses?.length || addresses.some(item => !isPublicPushAddress(item.address))) {
        return callback(Object.assign(new Error('Push endpoints must resolve to public network addresses.'), { code: 'EPUSHADDRESS' }));
      }
      const compatible = options?.family ? addresses.filter(item => item.family === options.family) : addresses;
      if (!compatible.length) return callback(Object.assign(new Error('No compatible push provider address.'), { code: 'ENOTFOUND' }));
      if (options?.all) callback(null, compatible);
      else callback(null, compatible[0].address, compatible[0].family);
    });
  };
}

export const pushAgent = new Agent({ lookup: publicPushLookup(), keepAlive: false });
