import string
import random
import time

from novaclient.v1_1.client import Client

# Ad-hoc client driver for OpenStack which implements the following logic:
# (a) boots X VMs asynchronously
# (b) sleeps for Y seconds
# (c) deletes the X VMs asynchronously
#

ID_URL = 'http://localhost:5000/v2.0/'
USER = 'admin'
PASSWORD = 'passw0rd'
IMAGE_NAME = 'Ubuntu 12.04 LTS MySQL'
PROJECT = 'admin'
FLAVOR_ID = '2'
SERVER_COUNT = 15
WAIT_DURATION = 60 * 5

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def nova_client(context):
    client = Client(USER, PASSWORD,
                    project_id=PROJECT, auth_url=ID_URL)

    return client


client = nova_client(None)

image_to_boot = None

print("locating image and flavor...")

for image in client.images.list():
    if image.name == IMAGE_NAME:
        image_to_boot = image
        break


flavor_to_boot = None
for flavor in client.flavors.list():
    if flavor.id == FLAVOR_ID:
        flavor_to_boot = flavor
        break


servers = []

for i in range(0, SERVER_COUNT):
    server_name = "bench-nova-%s" % (id_generator())
    print("booting server '%s' with image %s and flavor %s ..." %
          (server_name, str(image_to_boot), str(flavor_to_boot)))
    server = client.servers.create(server_name, image_to_boot, flavor_to_boot)
    servers.append(server)

print("sleeping for %s seconds" % (WAIT_DURATION))
time.sleep(WAIT_DURATION)

print("deleting servers...")
for server in servers:
    print("deleting %s" % (str(server)))
    server.delete()

print("done!")
