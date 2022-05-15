from pyfbsdk import *

import json


class CharacterSetup(object):
    def setup(self, mesh_model, config_path):
        scene = FBSystem().Scene

        properties = mesh_model.PropertyList

        # create facecap device
        facecap_device = FBCreateObject(
            "Browsing/Templates/Devices",
            "FaceCap OSC Device",
            mesh_model.FullName + "_facecap_device",
        )
        if not facecap_device:
            raise Exception("FaceCap OSC Device plugin was not found ")

        scene.Devices.append(facecap_device)

        # create relation constraint

        facecap_constraint = FBConstraintRelation(
            mesh_model.FullName + "_facecap_constraint"
        )

        sender = facecap_constraint.SetAsSource(facecap_device)

        reciever = facecap_constraint.ConstrainObject(mesh_model)

        # read mappings from config
        with open(config_path, "r") as f:
            mappings = json.loads(f.read())

        print(len(mappings))
        # make channel animatable
        tmp = dict()
        for i in mappings:
            channel = properties.Find(str(mappings[i]), 1)
            if not channel:
                print(
                    'cannot find target channel "{}", skipping!!!'.format(mappings[i])
                )
                continue
            try:
                channel.SetAnimated(1)
            except AttributeError as err:
                print(str(err) + " skipping!!!")
                continue
            tmp[i] = mappings[i]
        mappings = tmp

        sender_nodes = {i.Name: i for i in sender.AnimationNodeOutGet().Nodes}
        reciever_nodes = {i.Name: i for i in reciever.AnimationNodeInGet().Nodes}

        """
        # create config file
        config = dict()
        for i in sender_nodes:
            src = i
            # to lower camel case
            split_src = i.split(" ")
            dst =[split_src[0]]
            for i in split_src[1:]:
                dst.append(i.capitalize())
            dst = "".join(dst)
            config[src] = dst

        with open(r"Z:\models\diva\config.json", "w") as f:
            f.write(json.dumps(config, indent=4, sort_keys=True))
        """

        for i in mappings:
            src_anim = sender_nodes.get(i)
            if not src_anim:
                print(
                    'cannot find source channel "{}", skipping!!!'.format(mappings[i])
                )
                continue

            tgt_anim = reciever_nodes[mappings[i]]
            FBConnect(src_anim, tgt_anim)
