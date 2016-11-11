from troposphere_sugar import Skel
from troposphere_sugar.decorators import *
from troposphere import *
from troposphere.route53 import *

class MyCf(Skel):
    @cflookup('stack', 'output')
    @cfparam
    def hostedZone(self):
        return Parameter("hostedZone",
                Type="String",
                Default="fotocasa-pre.spain.schibsted.io.",
                Description="The hosted zone through which the packer builder instance will be accessible, the end hostname will be packerbuilder.{basedomain}")

    @cfparam
    def subnetId(self):
        return Parameter("SubnetId",
                Type="String",
                Default="subnet-113e9a66",
                Description="The subnet where the packer instance will be placed. It needs to belong to VpcId")

    @cfparam
    def vpcId(self):
        return Parameter("VpcId",
                Type="String",
                Default="vpc-a9b97bcc",
                Description="The vpc where the packer instance will be placed")

    @cfparam
    def emitterInstanceProfile(self):
        return Parameter("EmitterInstanceProfile",
                Type="String",
                Description="Instance profile to assign to emitter Instances")

    @cfparam
    def emitterStreamName(self):
        return Parameter("EmitterStreamName",
                Type="String",
                Description="Name of the strem created")

    @property
    def fullHostName(self):
        return Join(".", ["packerbuilder", Ref(self.hostedZone)])



    @cfresource
    def dnsRecord(self):
        return RecordSetType("dnsRecord",
                HostedZoneName=Ref(self.hostedZone),
                Name=self.fullHostName,
                Type="A",
                TTL=900,
                ResourceRecords=[])


cf = MyCf()

cf.process()
