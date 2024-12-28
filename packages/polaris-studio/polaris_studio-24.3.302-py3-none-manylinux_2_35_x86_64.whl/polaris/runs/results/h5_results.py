# Copyright (c) 2024, UChicago Argonne, LLC
# BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
import numpy as np
import pandas as pd
from polaris.runs.results.result_version import get_version_from_handle
from tables import open_file


class H5_Results(object):
    def __init__(self, filename):
        self.filename = filename
        with open_file(self.filename, mode="r") as h5file:
            self.version = get_version_from_handle(h5file)
            self.num_timesteps = h5file.root.link_moe._v_attrs.num_timesteps

        self.num_links = self.get_vector("link_moe", "link_uids").shape[0]
        self.num_turns = self.get_vector("turn_moe", "turn_uids").shape[0]
        self.path_lu = None
        self.path_mm_lu = None

    def cache_path_lu(self):
        if self.path_lu is None:
            self.path_lu = self.extract_index_lu(self.get_paths())

    def cache_path_mm_lu(self):
        if self.path_mm_lu is None:
            self.path_mm_lu = self.extract_index_lu(self.get_mm_paths())

    def get_vector(self, group, value):
        with open_file(self.filename, mode="r") as h5file:
            return np.array(h5file.root._f_get_child(group)._f_get_child(value)).flatten()

    def get_array(self, group, table):
        with open_file(self.filename, mode="r") as h5file:
            if group not in h5file.root or table not in h5file.root._f_get_child(group):
                return None
            return np.array(h5file.root._f_get_child(group)._f_get_child(table))

    mm_cols = [
        "gen_cost",
        "duration",
        "arrival_time",
        "bus_wait_time",
        "rail_wait_time",
        "comm_rail_wait_time",
        "walk_time",
        "bike_time",
        "bus_ivtt",
        "rail_ivtt",
        "comm_rail_ivtt",
        "car_time",
        "wait_count",
        "transfer_pen",
        "standing_pen",
        "capacity_pen",
        "monetary_cost",
        "tnc_wait_count",
        "tnc_wait_time",
    ]
    path_mm_cols = (
        ["path_id", "mode", "num_switches", "link_first_index", "link_last_index"]
        + [f"est_{e}" for e in mm_cols]
        + [f"actual_{e}" for e in mm_cols]
    )
    path_mm_link_cols = [
        "path_id",
        "link_uuid",
        "entering_time",
        "transit_vehicle_trip_id",
        "stop_seq_nr",
        "est_travel_time",
        "act_travel_time",
        "est_arrival_time",
        "act_arrival_time",
        "est_gen_cost",
        "act_gen_cost",
        "est_wait_count",
        "act_wait_count",
        "est_tnc_wait_count",
        "est_wait_time",
        "act_wait_time",
        "est_transfer_penalty",
        "act_transfer_penalty",
        "est_standing_penalty",
        "act_standing_penalty",
        "est_capacity_penalty",
        "act_capacity_penalty",
        "est_monetary_cost",
        "act_monetary_cost",
    ]
    path_cols = ["path_id", "link_first_index", "link_last_index", "unit_first_index", "unit_last_index"]
    path_link_cols = ["path_id", "link_uuid", "entering_time", "travel_time"]
    path_link_cols += ["energy_consumption", "routed_travel_time"]
    timesteps = [14400, 28800, 43200, 57600, 72000, 86399]

    def get_paths(self):
        def load_timestep(t):
            df = pd.DataFrame(self.get_array("paths", f"path_timestep_{t}"), columns=self.path_cols)
            return df.assign(timestep=t)

        return self.integerize_cols(pd.concat([load_timestep(i) for i in self.timesteps]))

    def integerize_cols(self, df):
        for c in ["path_id", "timestep", "link_first_index", "link_last_index"]:
            df[c] = df[c].astype(int)
        return df

    def extract_index_lu(self, df):
        return pd.Series(list(zip(df.timestep, df.link_first_index, df.link_last_index)), index=df.path_id).to_dict()

    def get_mm_paths(self):
        cols = [e for e in self.path_mm_cols if any(f"{p}" in e for p in ["_time", "_pen", "cost", "ivtt", "duration"])]

        def load_timestep(t):
            df = pd.DataFrame(self.get_array("paths", f"path_mm_timestep_{t}"), columns=self.path_mm_cols)
            df[cols] /= 1000.0
            return df.assign(timestep=t)

        return pd.concat([load_timestep(i) for i in self.timesteps]).sort_values("path_id")

    def get_path_links(self, path_id=None):
        if path_id is not None:
            self.cache_path_lu()
            timestep, first_idx, last_idx = self.path_lu.get(path_id)
            links = self.get_path_links_for_timestep(timestep)
            return links.iloc[first_idx : last_idx + 1]

        return pd.concat([self.get_path_links_for_timestep(t) for t in self.timesteps])

    def get_path_links_for_timestep(self, timestep):
        links = pd.DataFrame(
            data=self.get_array("paths", f"path_links_timestep_{timestep}"), columns=self.path_link_cols
        )
        links["link_id"] = np.floor(links.link_uuid.to_numpy() / 2).astype(int)
        links["link_dir"] = (links.link_uuid.to_numpy() % 2).astype(int)
        cols = ["entering_time", "travel_time", "routed_travel_time"]
        links[cols] /= 1000.0
        return links

    def get_path_mm_links_for_timestep(self, timestep):
        links = pd.DataFrame(
            data=self.get_array("paths", f"path_mm_links_timestep_{timestep}"), columns=self.path_mm_link_cols
        )
        links["link_id"] = np.floor(links.link_uuid.to_numpy() / 2).astype(int)
        links["link_dir"] = (links.link_uuid.to_numpy() % 2).astype(int)

        cols = ["entering_time", "est_travel_time", "act_travel_time", "est_arrival_time", "act_arrival_time"]
        cols += ["est_gen_cost", "act_gen_cost", "est_wait_time", "act_wait_time"]
        cols += ["est_transfer_penalty", "act_transfer_penalty", "est_standing_penalty", "act_standing_penalty"]
        cols += ["est_capacity_penalty", "act_capacity_penalty", "est_monetary_cost", "act_monetary_cost"]
        links[cols] /= 1000.0

        return links

    def get_path_mm_links(self, path_id=None):
        if path_id is not None:
            self.cache_path_mm_lu()
            timestep, first_idx, last_idx = self.path_mm_lu.get(path_id)
            links = self.get_path_mm_links_for_timestep(timestep)
            return links.iloc[first_idx : last_idx + 1]

    def get_array_v0(self, f, group, table):
        tables = {
            "link_moe": [
                "link_travel_time",
                "link_travel_time_standard_deviation",
                "link_queue_length",
                "link_travel_delay",
                "link_travel_delay_standard_deviation",
                "link_speed",
                "link_density",
                "link_in_flow_rate",
                "link_out_flow_rate",
                "link_in_volume",
                "link_out_volume",
                "link_speed_ratio",
                "link_in_flow_ratio",
                "link_out_flow_ratio",
                "link_density_ratio",
                "link_travel_time_ratio",
                "num_vehicles_in_link",
                "volume_cum_BPLATE",
                "volume_cum_LDT",
                "volume_cum_MDT",
                "volume_cum_HDT",
                "entry_queue_length",
            ],
            "turn_moe": [
                "turn_penalty",
                "turn_penalty_sd",
                "inbound_turn_travel_time",
                "outbound_turn_travel_time",
                "turn_flow_rate",
                "turn_flow_rate_cv",
                "turn_penalty_cv",
                "total_delay_interval",
                "total_delay_interval_cv",
            ],
        }
        return f[group][:, :, tables[group].index(table)].T
