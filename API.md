# Interaction API

## [Iroha](https://github.com/hyperledger/iroha) Intro

Peer is entity that __validate, store, commit__ transactions of the ledger (similar to DB instances).
Account is entity of the system that __can perform actions__ on the ledger (change/querying)
Account has roles
Roles has permission (e.g can make some transaction, can query some data)

Query - entity for __asking__ ledger information.
Transaction - entity for __changing__ ledger state. Compound of multiple commands.
Command - exact action of changing 

Account may send query & transaction iff it roles has related permission that has name similar to query/command, e.g:
- `"can_add_asset_qty"` allows perform command `AddAssetQuantity`
- `"can_receive"` allows receive assets from `TransferAssets`
- `"can_transfer_my_assets"` allows send assets from `TransferAssets`


## Iroha Entities

### Sensor

is Account with
- account (account_name=`"sensorid"` (NFC id))
- role (name=`"sensor"`, permissions=`{can_set_my_account_detail, can_receive}`)


### Checks

is Asset with
- asset (asset_name="checks", precision=0)
- quantity <==> number of checks

Sending `TransferAsset` is semantically performing a check
Bindings use string representation e.g `amount="123"`


### Verifier

is Account with
- account (account_name=`"verifier"`)
- role (name=`"verifier"`, permissions=`{can_transfer}`)


### Observer

is Account with
- account (account_name=`"observer"`)
- role (name=`"visitor"`, permissions=`{can_get_all_acc_ast, can_get_all_accounts, can_get_all_acc_detail, can_get_all_acc_txs}`)


### Admin

is Account with
- account (account_name=`"admin"`)
- role (name`"moderator"`, permissions=`{can_create_account, can_append_role, can_detach_role, can_add_asset_qty, can_add_peer}`)
- the rest existing roles

Adds or disables subjects of the network. Note that the list of specified permissions are the minimal and it can be extended for more feature-rich managing.


## System Actions

All interaction with Iroha performed via [gRPC](https://github.com/grpc/grpc) protocol. Data is transferred via [protobuf](https://github.com/google/protobuf) (similar to json, but binary thus more efficient).

### Sensor Data Heartbeat

Sensors periodically send data about its state, in our example that might be only temperature
Temperature represented by `AccountDetail`:
- Can be updated with `SetAccountDetail` (key=`"temp"`, val=`"30"`)
- Can be queries with `getAccountDetail` (account_name=`sensorid`)


### Sensors Checking (via NFC)

Android application attaches to the NFC transmitter and receives NFC id.
Then it able to send the sensor state (either good or bad):
- Good is TransferAsset(src_account_id=`verified`,
                        dest_account_id=`sensorid`,
                        asset_id=`"checks"`,
                        description=`"work"`,
                        amount=`"1"`)
- Bad is TransferAsset(src_account_id=`verified`,
                       dest_account_id=`sensorid`,
                       asset_id=`"checks"`,
                       description=`"broken"`,
                       amount=`"1"`)
