import os

import customtkinter
import jsonpickle

from helpers.AutopilotConfigDataClasses import AutopilotConfig, Feature, OverlappingGroup, DisjunctGroup

FEATURE_DISTANCE_TO_LEADING_VEHICLE = "distance_to_leading_vehicle"
FEATURE_VEHICLE_LANE_OFFSET = "vehicle_lane_offset"
FEATURE_IGNORE_LIGHTS_PERCENTAGE = "ignore_lights_percentage"
FEATURE_IGNORE_SIGNS_PERCENTAGE =  "ignore_signs_percentage"
FEATURE_IGNORE_VEHICLES_PERCENTAGE = "ignore_vehicles_percentage"
FEATURE_IGNORE_WALKERS_PERCENTAGE = "ignore_walkers_percentage"
FEATURE_KEEP_SLOW_LANE_RULE_PERCENTAGE = "keep_slow_lane_rule_percentage"
FEATURE_RANDOM_LEFT_LANECHANGE_PERCENTAGE = "random_left_lanechange_percentage"
FEATURE_RANDOM_RIGHT_LANECHANGE_PERCENTAGE = "random_right_lanechange_percentage"
FEATURE_UPDATE_VEHICLE_LIGHTS = "update_vehicle_lights"
FEATURE_VEHICLE_PERCENTAGE_SPEED_DIFFERENCE = "vehicle_percentage_speed_difference"

FEATURES = ["distance_to_leading_vehicle", "vehicle_lane_offset", "ignore_lights_percentage", "ignore_signs_percentage",
            "ignore_vehicles_percentage", "ignore_walkers_percentage", "keep_slow_lane_rule_percentage",
            "random_left_lanechange_percentage", "random_right_lanechange_percentage", "update_vehicle_lights",
            "vehicle_percentage_speed_difference"]

class FeatureFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.feature_combobox = customtkinter.CTkComboBox(self, values=FEATURES)
        self.feature_combobox.grid(row=0, column=0, sticky="nsew")

        self.value_entry = customtkinter.CTkEntry(self, placeholder_text="value")
        self.value_entry.grid(row=0, column=1, sticky="nsew")

        self.distribution_checkbox = customtkinter.CTkCheckBox(self, text="Normal Distributed")
        self.distribution_checkbox.grid(row=0, column=2, sticky="nsew")

    def get_feature(self) -> Feature:
        return Feature(name=self.feature_combobox.get(), value=float(self.value_entry.get()), normal_distributed=bool(self.distribution_checkbox.get()))




class OverlappingGroupFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.features = []

        add_feature_button = customtkinter.CTkButton(self, text="Add Feature", command=self.add_feature)
        add_feature_button.grid(row=0, column=0, sticky="nsew")

        self.percentage_entry = customtkinter.CTkEntry(self, placeholder_text="percentage")
        self.percentage_entry.grid(row=0, column=1, sticky="nsew")


    def add_feature(self):
        new_feature = FeatureFrame(self)
        self.features.append(new_feature)
        new_feature.grid(row=len(self.features), column=0, sticky="nsew")

    def get_overlapping_group(self) -> OverlappingGroup:
        features = []
        for feature in self.features:
            features.append(feature.get_feature())
        return OverlappingGroup(name="Overlapping Group x", fraction=int(self.percentage_entry.get()), features=features)



class DisjunctGroupFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.overlapping_groups = []

        add_overlapping_group_button = customtkinter.CTkButton(self, text="Add Overlapping Group", command=self.add_overlapping_group)
        add_overlapping_group_button.grid(row=0, column=0, sticky="nsew")

        self.percentage_entry = customtkinter.CTkEntry(self, placeholder_text="percentage")
        self.percentage_entry.grid(row=0, column=1, sticky="nsew")

    def add_overlapping_group(self):
        new_overlapping_group = OverlappingGroupFrame(self)
        self.overlapping_groups.append(new_overlapping_group)
        new_overlapping_group.grid(row=len(self.overlapping_groups), column=0, sticky="nsew")

    def get_disjunct_group(self) -> DisjunctGroup:
        overlapping_groups = []
        for overlapping_group in self.overlapping_groups:
            overlapping_groups.append(overlapping_group.get_overlapping_group())
        return DisjunctGroup(name="Disjunct Group x", fraction=int(self.percentage_entry.get()), overlapping_groups=overlapping_groups)


class CarlaAutopilotConfigApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("1600x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.disjunct_groups = []

        self.button = customtkinter.CTkButton(self, text="Add Disjunct Group", command=self.button_add_disjunct_group)
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.button = customtkinter.CTkButton(self, text="Save Configuration", command=self.button_save_config)
        self.button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")


    def button_add_disjunct_group(self):
        print("adding disjunt group pressed")
        new_disjunct_group = DisjunctGroupFrame(self)
        self.disjunct_groups.append(new_disjunct_group)
        new_disjunct_group.grid(row=len(self.disjunct_groups), column=0, sticky="nsew")



    def button_save_config(self):
        print("save config pressed")
        disjunct_groups = []
        for disjunct_group in self.disjunct_groups:
            disjunct_groups.append(disjunct_group.get_disjunct_group())
        autopilot_config = AutopilotConfig(disjunct_groups=disjunct_groups)

        print(str(autopilot_config))

        if os.path.exists("daten.json"):
            with open("daten.json", "w") as config_file:
                config_file.write(jsonpickle.encode(autopilot_config))



app = CarlaAutopilotConfigApp()
app.mainloop()