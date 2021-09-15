# mme

## Description

**MME**
Mobility Management Entity (MME) plays an important role in LTE EPC architecture. In fact, MME is the main signaling node in the EPC. According to LTE University, LTE MME is responsible for initiating paging and authentication of the mobile device. MME retains location information at the tracking area level for each user and then selects the appropriate gateway during the initial registration process. MME connects to the evolved node b (eNB) through the S1-MME interface and connects to S-GW through the S11 interface. Multiple MMEs can be grouped together in a pool to meet increasing signaling load in the network

## Usage

TODO: Mention relations once initcontainer work is done

## Deployment command 
juju deploy ./mme_ubuntu-20.04-amd64.charm --resource mme-image=amitinfo2k/nucleus-mme:9f86f87



## Relations

TODO: Provide any relations which are provided or required by your charm

## OCI Images

TODO: Include a link to the default image your charm uses

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines 
on enhancements to this charm following best practice guidelines, and
`CONTRIBUTING.md` for developer guidance.
