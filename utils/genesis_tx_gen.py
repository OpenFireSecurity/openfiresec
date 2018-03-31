#!/usr/bin/python3

from textwrap import wrap
import time

from  google.protobuf.json_format import MessageToJson
import iroha
import block_pb2 as blk

def print_key(owner, key):
  print(owner, "key is:", key.privateKey().hex(), key.publicKey().hex())

# Accounts
admin = "admin"
verifier = "verifier"
sensor = "sensorid"
observer = "observer"

# Account keys
keys = {
  admin : iroha.ModelCrypto().generateKeypair(),
  verifier : iroha.ModelCrypto().generateKeypair(),
  sensor : iroha.ModelCrypto().generateKeypair(),
  observer : iroha.ModelCrypto().generateKeypair(),
}
for k in keys:
  print_key(k, keys[k])

# Account roles
moderator_role = "moderator"
verifier_role = "verifier"
visitor_role = "visitor"
sensor_role = "sensor"

# Roles permissions
roles = {
  moderator_role: ["can_create_account", "can_append_role", "can_detach_role", "can_add_asset_qty", "can_add_peer"],
  verifier_role: ["can_transfer"],
  visitor_role: ["can_get_all_acc_ast", "can_get_all_accounts", "can_get_all_acc_detail", "can_get_all_acc_txs"],
  sensor_role: ["can_receive", "can_set_my_account_detail"]
}

# Rest entities
domain = "test"
asset = "checks"
peer_key = iroha.ModelCrypto().generateKeypair()
print_key("Peer", peer_key)

# Consts
max_amnt = "14474011154664524427946373126085988481658748083205070504932198000989141204991"
peer_host = "localhost:10001"

genesis_tx = iroha.ModelTransactionBuilder()                                                        \
                     .txCounter(1)                                                                  \
                     .createdTime(int(time.time() * 1000))                                          \
                     .creatorAccountId(admin + "@" + domain)                                        \
                     .addPeer(peer_host, peer_key.publicKey())                                      \
                                                                                                    \
                     .createRole(moderator_role, roles[moderator_role])                             \
                     .createRole(verifier_role, roles[verifier_role])                               \
                     .createRole(visitor_role, roles[visitor_role])                                 \
                     .createRole(sensor_role, roles[sensor_role])                                   \
                     .createDomain(domain, "verifier")                                              \
                                                                                                    \
                     .createAccount(admin, domain, keys[admin].publicKey())                         \
                     .appendRole(admin + "@" + domain, moderator_role)                              \
                     .appendRole(admin + "@" + domain, visitor_role)                                \
                     .appendRole(admin + "@" + domain, sensor_role)                                 \
                                                                                                    \
                     .createAsset(asset, domain, 0)                                                 \
                                                                                                    \
                     .createAccount(verifier, domain, keys[verifier].publicKey())                   \
                     .addAssetQuantity(verifier + "@" + domain, asset + "#" + domain, max_amnt)     \
                                                                                                    \
                     .createAccount(observer, domain, keys[observer].publicKey())                   \
                     .appendRole(observer + "@" + domain, visitor_role)                             \
                     .detachRole(observer + "@" + domain, verifier_role)                            \
                                                                                                    \
                     .createAccount(sensor, domain, keys[sensor].publicKey())                       \
                     .appendRole(sensor + "@" + domain, sensor_role)                                \
                     .detachRole(sensor + "@" + domain, verifier_role)                              \
                     .build()

proto = iroha.ModelProtoTransaction().signAndAddSignature(genesis_tx, keys[admin])
t = blk.Transaction()
t.ParseFromString(b''.join([bytes.fromhex(x) for x in wrap(proto.hex(), 2)]))
print(MessageToJson(t))
