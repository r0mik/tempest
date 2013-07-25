#!/usr/bin/env python

# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 Quanta Research Cambridge, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from novaclient.v1_1 import client as nova_client
import novaclient.exceptions
from cinderclient.v2 import client as cinder_client
import tempest.config

# get the environment variables for credentials
identity = tempest.config.TempestConfig().identity

nt = nova_client.Client(identity.username, identity.password,
                        identity.tenant_name, identity.uri)
cc = cinder_client.Client(identity.username, identity.password,
                     identity.tenant_name, identity.uri)

flavor_list = nt.flavors.list()
server_list = nt.servers.list()
images_list = nt.images.list()
keypairs_list = nt.keypairs.list()
floating_ips_list = nt.floating_ips.list()
try:
    volumes_list = nt.volumes.list()
except novaclient.exceptions.NotFound:
    volumes_list = cc.volumes.list(detailed=False)

print "total servers: %3d, total flavors: %3d, total images: %3d," % \
      (len(server_list),
       len(flavor_list),
       len(images_list)),

print "total keypairs: %3d, total floating ips: %3d" % \
      (len(keypairs_list),
       len(floating_ips_list))

print "deleting all servers"
for s in server_list:
    s.delete()

print "deleting all keypairs"
for s in keypairs_list:
    s.delete()

print "deleting all floating_ips"
for s in floating_ips_list:
    s.delete()

print "deleting all volumes"
for s in volumes_list:
    s.delete()
