from pyfbsdk import *
import json
import os

# def write_config(self, path):
#     pass
#     # create config file
#     config = dict()
#     for i in facecap_device_sender_nodes:
#         src = i
#         # to lower camel case
#         split_src = i.split(" ")
#         dst =[split_src[0]]
#         for i in split_src[1:]:
#             dst.append(i.capitalize())
#         dst = "".join(dst)
#         config[src] = dst
#     with open(r"Z:\models\diva\config.json", "w") as f:
#         f.write(json.dumps(config, indent=4, sort_keys=True))


class AnimInputs(dict):
    def __init__(self, anim_node):
        super(AnimInputs, self).__init__({i.Name: i for i in anim_node.Nodes})


class CharacterSetup(object):
    def __init__(self):
        self.facecap_device_name = "FaceCap OSC Device"
        self._scene = FBSystem().Scene

    @property
    def scene(self):
        return self._scene

    def _read_config(self, path):
        """
        reads mappings config from json file
        :param path: path to .json file
        :type path: str
        :return: channel mappings config
        :rtype: dict
        """
        if not os.path.exists(path):
            raise OSError('config does not exist "{}"'.format(path))
        with open(path) as f:
            return json.loads(f.read())

    def find_node_by_name(self, node, name):
        for i in node.Nodes:
            if i.Name == name:
                return i

    def enable_anim_channels(self, node, channel_names_list):
        # set all required (in mappings config) channels animated
        # and clear all non existing attributes from mappings
        for i in channel_names_list:
            channel = node.PropertyList.Find(str(i), 1)
            if not channel:
                # TODO create logging
                print('cannot find target channel "{}", skipping!!!'.format(i))
                continue
            try:
                channel.SetAnimated(1)
            except AttributeError as err:
                print(str(err) + " skipping!!!")
                continue

    def create_device(self, device_name, name):
        """
        creates device in scene
        :param device_name: device plugin name
        :type device_name str
        :param name: device_name: device nice name (how it is depict in mobu scene)
        :type name: str
        :return: created device
        :rtype: FBDevice
        """
        device = FBCreateObject("Browsing/Templates/Devices", device_name, name)
        if not device:
            raise Exception("{} plugin was not found ".format(device_name))
        self.scene.Devices.append(device)
        return device

    def setup(self, face_mesh_model, config_path):
        # create devices
        facecap_device = self.create_device(
            self.facecap_device_name, face_mesh_model.FullName + "_facecap_device"
        )

        # create relation constraint
        facecap_relation_constraint = FBConstraintRelation(
            face_mesh_model.FullName + "_facecap_constraint"
        )
        # set Active
        facecap_relation_constraint.Active = True

        # add facecap device to relation constraint
        facecap_device_sender = facecap_relation_constraint.SetAsSource(facecap_device)

        # add mesh to relation constraint
        face_mesh_model_reciever = facecap_relation_constraint.ConstrainObject(
            face_mesh_model
        )

        # TODO make more nice name for mappings
        mappings_config = self._read_config(config_path)

        # set all required (in mappings_config) channels animated
        self.enable_anim_channels(face_mesh_model, mappings_config.values())

        # get anim channels from nodes in constraint
        facecap_device_sender_anim_channels = AnimInputs(
            facecap_device_sender.AnimationNodeOutGet()
        )

        face_mesh_model_reciever_anim_channels = AnimInputs(
            face_mesh_model_reciever.AnimationNodeInGet()
        )

        # make connections
        for i in mappings_config:
            src_anim = facecap_device_sender_anim_channels.get(i)
            tgt_anim = face_mesh_model_reciever_anim_channels.get(mappings_config[i])

            if not src_anim:
                print('facecap device has no channel named: "{}"'.format(i))
                continue

            if not tgt_anim:
                print("mesh has no anim channel named: {}".format(i))
                continue

            FBConnect(src_anim, tgt_anim)


class CharacterSetupWithTweak(CharacterSetup):
    def __init__(self):
        super(CharacterSetupWithTweak, self).__init__()
        self.facecap_tweak_device_name = "FaceCap Multconcert"

    def setup(self, face_mesh_model, config_path):
        # create devices
        facecap_device = self.create_device(
            self.facecap_device_name, face_mesh_model.FullName + "_facecap_device"
        )
        facecap_tweak_device = self.create_device(
            self.facecap_tweak_device_name,
            face_mesh_model.FullName + "_facecap_tweak_device",
        )

        # create relation constraint
        facecap_relation_constraint = FBConstraintRelation(
            face_mesh_model.FullName + "_facecap_constraint"
        )
        # set Active
        facecap_relation_constraint.Active = True

        # add facecap device to relation constraint
        facecap_device_sender = facecap_relation_constraint.SetAsSource(facecap_device)

        # add facecap tweak device to realtion constraint
        facecap_tweak_device_sender = facecap_relation_constraint.SetAsSource(
            facecap_tweak_device
        )

        # add mesh to relation constraint
        face_mesh_model_reciever = facecap_relation_constraint.ConstrainObject(
            face_mesh_model
        )

        # TODO make more nice name for mappings
        mappings_config = self._read_config(config_path)

        # set all required (in mappings config) channels animated
        self.enable_anim_channels(face_mesh_model, mappings_config.values())

        # get anim channels from nodes in constraint
        facecap_device_sender_anim_channels = AnimInputs(
            facecap_device_sender.AnimationNodeOutGet()
        )

        facecap_tweak_device_sender_anim_channels = AnimInputs(
            facecap_tweak_device_sender.AnimationNodeOutGet()
        )

        face_mesh_model_reciever_anim_channels = AnimInputs(
            face_mesh_model_reciever.AnimationNodeInGet()
        )

        # make connections
        for i in mappings_config:
            src_anim = facecap_device_sender_anim_channels.get(i)
            tgt_anim = face_mesh_model_reciever_anim_channels.get(mappings_config[i])

            if not src_anim:
                print('facecap device has no channel named: "{}"'.format(i))
                continue

            if not tgt_anim:
                print("mesh has no anim channel named: {}".format(i))
                continue

            # create scale offset node
            scale_offset_node = facecap_relation_constraint.CreateFunctionBox(
                "Number", "Scale And Offset (Number)"
            )
            scale_offset_node.Name = "offset_" + src_anim.Name

            # bind scale offset node input connections
            _find = lambda x: self.find_node_by_name(
                scale_offset_node.AnimationNodeInGet(), x
            )

            FBConnect(
                facecap_tweak_device_sender_anim_channels.get(i + " offset"),
                _find("Offset"),
            )
            FBConnect(
                facecap_tweak_device_sender_anim_channels.get(i + " clamp min"),
                _find("Clamp Min"),
            )
            FBConnect(
                facecap_tweak_device_sender_anim_channels.get(i + " clamp max"),
                _find("Clamp Max"),
            )

            FBConnect(
                facecap_tweak_device_sender_anim_channels.get(i + " scale"),
                _find("Scale Factor"),
            )

            scale_offset_node_in = self.find_node_by_name(
                scale_offset_node.AnimationNodeInGet(), "X"
            )
            scale_offset_node_out = self.find_node_by_name(
                scale_offset_node.AnimationNodeOutGet(), "Result"
            )
            # connections
            FBConnect(src_anim, scale_offset_node_in)
            FBConnect(scale_offset_node_out, tgt_anim)
