# OpenFireSecurity

Is a set of robust tools and configurations based on [Iroha](https://github.com/hyperledger/iroha) distributed ledger that aimed to deal with fire alarm monitoring. Its creation was inspired by Kemerovo incident.

Note, that this system is able to work not only with fire sensors (as the following text consideration) but with any sensor-based systems that require transparency of the operation.

## Architecture

There is a number of sensors that reports its tracked data. All the data is collected by regulators (may be organizations, where the data is tracked, government regulators and just some organizations interested in such information).
The second part is for inspector work controlling. An inspector should perform usual checks and report data (functional/broken/etc.) to the same ledger.
All of that data can be fully reviewed by the users with related permissions, so the transparency of organization operation is fully guaranteed.

## Roles

There is 4 main roles that is able to interact with the ledger:

- Moderator
- Verifier
- Visitor
- Sensor

### Moderator

is basically administrator of the system, who can create new accounts or disable them.

### Verifier

is the inspector who is responsible for the examination of the fire sensors, in other words regular sending information of the sensors state

### Visitor

is the party that is interested in the observing the system functionality. That may be the publicly available account, or may belong to the organization management

### Sensor

is the entity that might report data for further analysis. For example, fire sensors might send the information of the temperature of smoke density. As long as the sensors are not eternal they may need an examination by the visitor.

## Instruments

TODO
