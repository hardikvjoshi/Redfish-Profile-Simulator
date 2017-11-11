# Copyright Notice:
# Copyright 2016 Distributed Management Task Force, Inc. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Profile-Simulator/LICENSE.md

import os

from .resource import RfResource, RfCollection


class RfFabricsCollection(RfCollection):
    def element_type(self):
        return RfFabricObj

class RfFabricsCollection(RfCollection):
    def element_type(self):
        return RfFabricObj

#    def create_sub_objects(self, base_path, rel_path):
#        if os.path.isdir(os.path.join(base_path, rel_path)):
#            self.components["SAS"] = RfFabricObj(base_path,
#                                                 os.path.normpath("redfish/v1/Fabrics/SAS"),
#                                                              parent=self)


class RfFabricObj(RfResource):
    # create the dependent sub-objects that live under the Fabric object
    def create_sub_objects(self, base_path, rel_path):
        resource_path = os.path.join(base_path, rel_path);
        contents = os.listdir(resource_path)
        for item in contents:
            if item == "Endpoints":
                self.components[item] = RfFabricEndpoints(base_path, os.path.join(rel_path, item), parent=self)
            elif item == "Switches":
                self.components[item] = RfFabricSwitchs(base_path, os.path.join(rel_path, item), parent=self)
            elif item == "Zones":
                self.components[item] = RfFabricZones(base_path, os.path.join(rel_path, item), parent=self)

    def patch_resource(self, patch_data):
        # first verify client didn't send us a property we cant patch
        for key in patch_data.keys():
            if key != "AssetTag" and key != "IndicatorLED":
                return 4, 400, "Invalid Patch Property Sent", ""
        # now patch the valid properties sent
        if "AssetTag" in patch_data:
            self.res_data['AssetTag'] = patch_data['AssetTag']
        if "IndicatorLED" in patch_data:
            self.res_data['IndicatorLED'] = patch_data['IndicatorLED']
        return 0, 204, None, None

    def reset_resource(self, reset_data):
        if "ResetType" in reset_data:
            # print("RESETDATA: {}".format(resetData))
            value = reset_data['ResetType']
            valid_values = self.res_data["Actions"]["#Chassis.Reset"]["ResetType@Redfish.AllowableValues"]
            if value in valid_values:
                # it is a supoported reset action  modify other properties appropritely
                if value == "On":
                    self.res_data["PowerState"] = "On"
                    print("PROFILE_SIM--SERVER WAS RESET. power now ON")
                elif value == "ForceOff":
                    self.res_data["PowerState"] = "Off"
                    print("PROFILE_SIM--SERVER WAS RESET. Power now Off")
                return 0, 204, "Chassis Reset", ""
            else:
                return 4, 400, "Invalid reset value: ResetType", ""
        else:  # invalid request
            return 4, 400, "Invalid request property", ""


# subclass Thermal Metrics
class RfFabricEndpoints(RfResource):
    def create_sub_objects(self, base_path, rel_path):
        resource_path = os.path.join(base_path, rel_path);
        contents = os.listdir(resource_path)
        for item in contents:
            if item.__contains__("Drive"):
                self.components[item] = RfDriveCollection(base_path,
                                                          os.path.join(rel_path, item),
                                                          parent=self)
            elif item.__contains__("Enclosure"):
                self.components[item] = RfEnclosureCollection(base_path,
                                                          os.path.join(rel_path, item),
                                                          parent=self)
            elif item.__contains__("Initiator"):
                self.components[item] = RfInitiatorCollection(base_path,
                                                          os.path.join(rel_path, item),
                                                          parent=self)
            if item.__contains__("TapeDrive"):
                self.components[item] = RfTapeDriveCollection(base_path,
                                                          os.path.join(rel_path, item),
                                                          parent=self)

class RfFabricZones(RfResource):
    def create_sub_objects(self, base_path, rel_path):
        resource_path = os.path.join(base_path, rel_path);
        contents = os.listdir(resource_path)
        for item in contents:
            self.components[item] = RfSwitchCollection(base_path,
                                                          os.path.join(rel_path, item),
                                                          parent=self)


class RfFabricSwitchs(RfResource):
    def create_sub_objects(self, base_path, rel_path):
        resource_path = os.path.join(base_path, rel_path);
        contents = os.listdir(resource_path)
        for item in contents:
            self.components[item] = RfSwitchCollection(base_path,
                                                          os.path.join(rel_path, item),
                                                          parent=self)
class RfFabricPorts(RfResource):
    def create_sub_objects(self, base_path, rel_path):
        resource_path = os.path.join(base_path, rel_path);
        contents = os.listdir(resource_path)
        for item in contents:
                self.components[item] = RfPortCollection(base_path,
                                                          os.path.join(rel_path, item),
                                                          parent=self)
class RfSwitchCollection(RfResource):
    def create_sub_objects(self, base_path, rel_path):
        resource_path = os.path.join(base_path, rel_path);
        contents = os.listdir(resource_path)
        for item in contents:
            if item == "Ports":
                self.components[item] = RfFabricPorts(base_path,
                                                  os.path.join(rel_path, item),
                                                  parent=self)


class RfPortCollection(RfResource):
    def element_type(self):
        return RfPortCollection

class RfDriveCollection(RfResource):
    def element_type(self):
        return RfDriveCollection

class RfEnclosureCollection(RfResource):
    def element_type(self):
        return RfEnclosureCollection

class RfInitiatorCollection(RfResource):
    def element_type(self):
        return RfInitiatorCollection

class RfTapeDriveCollection(RfResource):
    def element_type(self):
        return RfTapeDriveCollection

