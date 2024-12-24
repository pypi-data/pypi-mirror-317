import numpy as np
import uproot
import re
import pandas as pd
import fast_vertex_quality_inference.processing.transformers as tfs
import fast_vertex_quality_inference.processing.processing_tools as pts
from fast_vertex_quality_inference.rapidsim.rapidsim_tools import compute_combined_param

masses = {}
masses[321] = 493.677
masses[211] = 139.57039
masses[13] = 105.66
masses[11] = 0.51099895000  # * 1e-3
pid_list = [11, 13, 211, 321]


rapidsim_conventions = {}

rapidsim_conventions["momenta_component"] = "{particle}_P"
rapidsim_conventions["true_momenta_component"] = "{particle}_P_TRUE"

rapidsim_conventions["momenta_component"] = "{particle}_P{dim}"
rapidsim_conventions["true_momenta_component"] = "{particle}_P{dim}_TRUE"

rapidsim_conventions["pid"] = "{particle}_ID"
rapidsim_conventions["true_pid"] = "{particle}_ID_TRUE"

rapidsim_conventions["mass"] = "{particle}_M"
rapidsim_conventions["true_mass"] = "{particle}_M_TRUE"

rapidsim_conventions["origin"] = "{particle}_orig{dim}"
rapidsim_conventions["true_origin"] = "{particle}_orig{dim}_TRUE"

rapidsim_conventions["vertex"] = "{particle}_vtx{dim}"
rapidsim_conventions["true_vertex"] = "{particle}_vtx{dim}_TRUE"


class tuple_manager:

    def map_branch_names(self):
        branch_names = list(self.tuple.keys())
        branch_names = [
            branch.replace(self.mother_particle_name, self.mother)
            for branch in branch_names
        ]
        # if self.intermediate_particle_name:
        #     branch_names = [
        #         branch.replace(self.intermediate_particle_name, self.intermediate)
        #         for branch in branch_names
        #     ]
        temps = []
        for i in range(self.Nparticles):  # Nparticles
            if (
                self.particles[i] in self.daughter_particle_names
                and self.particles[i] == self.daughter_particle_names[i]
            ):
                # all good - no need really even to replace
                replace_string = self.particles[i]
            else:
                replace_string = f"{self.particles[i][0]}_temp_{self.particles[i][1:]}"
                temps.append(i)
            branch_names = [
                branch.replace(self.daughter_particle_names[i], replace_string)
                for branch in branch_names
            ]
        for i in temps:
            replace_string = f"{self.particles[i][0]}_temp_{self.particles[i][1:]}"
            branch_names = [
                branch.replace(replace_string, self.particles[i])
                for branch in branch_names
            ]
        self.tuple.columns = branch_names

    def map_branch_names_list(self, branch_names):
        branch_names = [
            branch.replace(self.mother_particle_name, self.mother)
            for branch in branch_names
        ]
        # if self.intermediate_particle_name:
        #     branch_names = [
        #         branch.replace(self.intermediate_particle_name, self.intermediate)
        #         for branch in branch_names
        #     ]
        temps = []
        for i in range(self.Nparticles):  # Nparticles
            if (
                self.particles[i] in self.daughter_particle_names
                and self.particles[i] == self.daughter_particle_names[i]
            ):
                # all good - no need really even to replace
                replace_string = self.particles[i]
            else:
                replace_string = f"{self.particles[i][0]}_temp_{self.particles[i][1:]}"
                temps.append(i)
            branch_names = [
                branch.replace(self.daughter_particle_names[i], replace_string)
                for branch in branch_names
            ]
        for i in temps:
            replace_string = f"{self.particles[i][0]}_temp_{self.particles[i][1:]}"
            branch_names = [
                branch.replace(replace_string, self.particles[i])
                for branch in branch_names
            ]
        return branch_names

    def smearelectronE(self, E_smearing_output, particle):
        for column in E_smearing_output.columns:
            dim = column[-1]
            self.tuple[f"{particle}_P{dim}"] = (
                E_smearing_output[column]
                * (self.tuple[f"{particle}_P{dim}_TRUE"] + 1e-4)
            ) + self.tuple[f"{particle}_P{dim}_TRUE"]

    def recompute_combined_particles(self, combined_particles):

        # Recompute variables of reconstructed particles

        for combined_particle in combined_particles:
            particle_daughters = combined_particles[combined_particle]
            daughter_info = {}
            for daughter in particle_daughters:
                daughter_info[daughter] = {}
                for param in ["M", "PX", "PY", "PZ"]:
                    daughter_info[daughter][param] = self.tuple[f"{daughter}_{param}"]
            for param in ["M", "PX", "PY", "PZ"]:
                self.tuple[f"{combined_particle}_{param}"] = compute_combined_param(
                    daughter_info, param
                )
            self.tuple[f"{combined_particle}_P"] = np.sqrt(
                self.tuple[f"{combined_particle}_PX"] ** 2
                + self.tuple[f"{combined_particle}_PY"] ** 2
                + self.tuple[f"{combined_particle}_PZ"] ** 2
            )
            self.tuple[f"{combined_particle}_PT"] = np.sqrt(
                self.tuple[f"{combined_particle}_PX"] ** 2
                + self.tuple[f"{combined_particle}_PY"] ** 2
            )

    def recompute_reconstructed_mass(self):

        df = self.tuple.copy()

        for _idx, particle in enumerate(self.particles):
            if _idx == 0:
                PE = np.sqrt(
                    df[f"{particle}_M"] ** 2
                    + df[f"{particle}_PX"] ** 2
                    + df[f"{particle}_PY"] ** 2
                    + df[f"{particle}_PZ"] ** 2
                )
                PX = df[f"{particle}_PX"]
                PY = df[f"{particle}_PY"]
                PZ = df[f"{particle}_PZ"]
            else:
                PE += np.sqrt(
                    df[f"{particle}_M"] ** 2
                    + df[f"{particle}_PX"] ** 2
                    + df[f"{particle}_PY"] ** 2
                    + df[f"{particle}_PZ"] ** 2
                )
                PX += df[f"{particle}_PX"]
                PY += df[f"{particle}_PY"]
                PZ += df[f"{particle}_PZ"]

        mass = np.sqrt((PE**2 - PX**2 - PY**2 - PZ**2))

        return mass

    def __init__(
        self,
        tuple_location,
        fully_reco,
        nPositive_missing_particles,
        nNegative_missing_particles,
        mother_particle_name,
        intermediate_particle_name,  # make this optional
        daughter_particle_names,
        combined_particles,
        tree="DecayTree",
        entry_stop=None,
        branch_naming_structure=None,
        physical_units="GeV",
    ):

        self.Nparticles = len(combined_particles[mother_particle_name])

        self.particle_names = combined_particles[mother_particle_name]
        self.particle_map = {}
        self.particles = []
        for i in range(self.Nparticles):
            self.particles.append(f"DAUGHTER{i+1}")
            self.particle_map[self.particle_names[i]] = self.particles[-1]

        self.mother = "MOTHER"
        # self.intermediate = intermediate_particle_name
        self.fully_reco = fully_reco
        self.nPositive_missing_particles = nPositive_missing_particles
        self.nNegative_missing_particles = nNegative_missing_particles

        self.mother_particle_name = mother_particle_name
        self.intermediate_particle_name = intermediate_particle_name
        self.combined_particles = combined_particles
        self.daughter_particle_names = daughter_particle_names

        self.tree = tree
        self.tuple_location = tuple_location

        self.raw_tuple = uproot.open(self.tuple_location)[self.tree]

        list_of_branches = list(self.raw_tuple.keys())
        list_of_branches = [
            branch for branch in list_of_branches if "COV" not in branch
        ]

        if entry_stop:
            arrays = self.raw_tuple.arrays(
                list_of_branches, library="np", entry_stop=entry_stop
            )
            self.tuple = pd.DataFrame(arrays)
        else:
            arrays = self.raw_tuple.arrays(list_of_branches, library="np")
            self.tuple = pd.DataFrame(arrays)

        # IF BRANCH STRUCTURE DIFFERENT CONVERT TO RAPIDSIM CONVENTION
        self.branch_naming_structure = branch_naming_structure
        if self.branch_naming_structure:
            self.convert_branch_aliases(self.branch_naming_structure, to_rapidsim=True)
        # IF UNITS NOT GEV
        self.physical_units = physical_units
        if self.physical_units != "GeV":
            self.convert_physical_units(conversion="from_MeV")

        self.map_branch_names()

        self.list_of_particles = []
        tag_to_find_particle_names = "origX_TRUE"
        for branch in self.tuple:
            if tag_to_find_particle_names in branch:
                self.list_of_particles.append(
                    branch.replace(f"_{tag_to_find_particle_names}", "")
                )

        self.original_branches = list(self.tuple.keys())

        self.tuple[f"{self.mother}_M"] = self.recompute_reconstructed_mass()

    def convert_physical_units(self, conversion, specific_tuple=None):
        if conversion not in ["from_MeV", "back_to_MeV"]:
            print("conversion not valid")
            raise

        if specific_tuple is not None:
            tuple_to_update = specific_tuple
        else:
            tuple_to_update = self.tuple

        # do this before and after
        if conversion == "from_MeV":
            self.branches_for_conversion = []
            for branch in tuple_to_update:

                for (
                    branch_naming_structure,
                    pattern,
                ) in rapidsim_conventions.items():

                    if branch_naming_structure in [
                        "momenta_component",
                        "true_momenta_component",
                        "mass",
                        "true_mass",
                    ]:

                        regex_pattern = (
                            pattern.replace("{particle}", r"(?P<particle>\w+)").replace(
                                "{dim}", r"(?P<dim>\w)"
                            )
                            + r"$"
                        )  # Only a single character for {dim}
                        match = re.match(regex_pattern, branch)

                        if match:
                            self.branches_for_conversion.append(branch)

            for branch in self.branches_for_conversion:
                # tuple_to_update.loc[:, branch] *= 1e-3
                tuple_to_update.loc[:, branch] = tuple_to_update.loc[:, branch] * 1e-3
        else:
            for branch in self.branches_for_conversion:
                # tuple_to_update.loc[:, branch] *= 1e3
                tuple_to_update.loc[:, branch] = tuple_to_update.loc[:, branch] * 1e3

    def convert_branch_aliases(
        self, branch_naming_structures, to_rapidsim, specific_tuple=None
    ):

        if specific_tuple is not None:
            tuple_to_update = specific_tuple
        else:
            tuple_to_update = self.tuple

        if to_rapidsim:
            new_branches = []
            for branch in tuple_to_update:

                new_branch = branch

                for (
                    branch_naming_structure,
                    pattern,
                ) in branch_naming_structures.items():

                    regex_pattern = (
                        pattern.replace("{particle}", r"(?P<particle>\w+)").replace(
                            "{dim}", r"(?P<dim>\w)"
                        )
                        + r"$"
                    )  # Only a single character for {dim}
                    match = re.match(regex_pattern, branch)

                    if match:
                        particle = match.group("particle")
                        try:
                            dim = match.group("dim")
                        except Exception:
                            dim = ""  # no dim, for example mass branch
                        updated_branch = rapidsim_conventions[
                            branch_naming_structure
                        ].format(particle=particle, dim=dim)
                        new_branch = updated_branch
                        break
                new_branches.append(new_branch)

            tuple_to_update.columns = new_branches
        else:

            new_branches = []

            for branch in tuple_to_update:

                new_branch = branch

                for (
                    branch_naming_structure,
                    custom_pattern,
                ) in branch_naming_structures.items():

                    pattern = rapidsim_conventions[branch_naming_structure]

                    regex_pattern = (
                        pattern.replace("{particle}", r"(?P<particle>\w+)").replace(
                            "{dim}", r"(?P<dim>\w)"
                        )
                        + r"$"
                    )  # Only a single character for {dim}
                    match = re.match(regex_pattern, branch)

                    if match:
                        particle = match.group("particle")
                        try:
                            dim = match.group("dim")
                        except Exception:
                            dim = ""  # no dim, for example mass branch
                        updated_branch = custom_pattern.format(
                            particle=particle, dim=dim
                        )
                        new_branch = updated_branch
                        break

                new_branches.append(new_branch)

            tuple_to_update.columns = new_branches

    def write(
        self,
        new_branches_to_keep,
        output_location=None,
        keep_vertex_info=False,
        keep_tuple_structure=False,
        extra_branches=[],
    ):

        branches = self.original_branches + new_branches_to_keep

        if not keep_tuple_structure:
            # re-name columns
            branch_swaps = {}
            branch_swaps[self.mother] = self.mother_particle_name
            if self.intermediate_particle_name:
                if isinstance(self.intermediate_particle_name, list):
                    for inter in self.intermediate_particle_name:
                        branch_swaps[inter] = inter
                else:
                    branch_swaps[self.intermediate_particle_name] = (
                        self.intermediate_particle_name
                    )
            branch_swaps[self.particles[0]] = self.daughter_particle_names[0]
            branch_swaps[self.particles[1]] = self.daughter_particle_names[1]
            branch_swaps[self.particles[2]] = self.daughter_particle_names[2]
            # add rest to list - will only be others if dropMissing=False
            if isinstance(self.intermediate_particle_name, list):
                named_particles = (
                    [self.mother] + self.intermediate_particle_name + self.particles
                )
            else:
                named_particles = (
                    [self.mother] + [self.intermediate_particle_name] + self.particles
                )
            unnamed_particles = list(set(self.list_of_particles) - set(named_particles))
            for unnamed_particle in unnamed_particles:
                branch_swaps[unnamed_particle] = unnamed_particle

        tuple_to_write = self.tuple[branches]

        if not keep_tuple_structure:
            columns = list(tuple_to_write.columns)
            new_columns = []
            for column in columns:
                for to_swap in list(branch_swaps.keys()):
                    if column[: len(to_swap)] == to_swap:
                        new_columns.append(
                            column.replace(to_swap, branch_swaps[to_swap])
                        )
                        break

            # drop columns that might hang on but are not related to an individual particle, MCorr and nEvent for example
            drop_list = []
            for i in tuple_to_write.columns:
                # if i not in new_columns:
                if not any(s in i for s in list(branch_swaps.keys())):
                    drop_list.append(i)
            tuple_to_write = tuple_to_write.drop(drop_list, axis=1)

            tuple_to_write.columns = new_columns

            if not keep_vertex_info:
                for dim in ["X", "Y", "Z"]:
                    tuple_to_write = tuple_to_write.drop(
                        columns=[
                            col for col in tuple_to_write.columns if f"_vtx{dim}" in col
                        ]
                    )
                    tuple_to_write = tuple_to_write.drop(
                        columns=[
                            col
                            for col in tuple_to_write.columns
                            if f"_orig{dim}" in col
                        ]
                    )

            # re-order columns
            columns = tuple_to_write.columns
            if self.intermediate_particle_name:
                prefix_order = [self.mother_particle_name]
                if not isinstance(self.intermediate_particle_name, list):
                    prefix_order.append(self.intermediate_particle_name)
                else:
                    prefix_order.extend(self.intermediate_particle_name)
                prefix_order.extend(
                    [
                        self.daughter_particle_names[0],
                        self.daughter_particle_names[1],
                        self.daughter_particle_names[2],
                    ]
                )
            else:
                prefix_order = [
                    self.mother_particle_name,
                    self.daughter_particle_names[0],
                    self.daughter_particle_names[1],
                    self.daughter_particle_names[2],
                ]

            for unnamed_particle in unnamed_particles:
                prefix_order.append(unnamed_particle)

            ordered_columns = []
            for prefix in prefix_order:
                cols_with_prefix = [col for col in columns if col.startswith(prefix)]
                ordered_columns.extend(cols_with_prefix)
            tuple_to_write = tuple_to_write[ordered_columns]

        if self.physical_units != "GeV":
            self.convert_physical_units(
                conversion="back_to_MeV", specific_tuple=tuple_to_write
            )

        if self.branch_naming_structure:
            self.convert_branch_aliases(
                self.branch_naming_structure,
                to_rapidsim=False,
                specific_tuple=tuple_to_write,
            )

        if len(extra_branches) > 0:
            tuple_to_write = tuple_to_write.drop(
                columns=extra_branches, errors="ignore"
            )
            tuple_to_write = pd.concat(
                [tuple_to_write, self.tuple[extra_branches]], axis=1
            )

        if not output_location:
            output_location = f"{self.tuple_location[:-5]}_reco.root"
        pts.write_df_to_root(tuple_to_write, output_location, self.tree)
        return output_location

    def add_branches(self, data_to_add, append_to_leaf_vector=False):

        if append_to_leaf_vector:
            for branch, data in data_to_add.items():
                # If the branch already exists, append_to_leaf_vector
                if branch in self.tuple.columns:

                    current_data = np.asarray(self.tuple[branch])

                    current_data = np.vstack(current_data)

                    if len(np.shape(current_data)) == 1:
                        current_data = np.expand_dims(current_data, 1)
                    if len(np.shape(data)) == 1:
                        data = np.expand_dims(data, 1)
                    new_branch_vector = np.concatenate((current_data, data), axis=1)

                    self.tuple[branch] = [list(row) for row in new_branch_vector]

                else:
                    # If the branch doesn't exist, add it as a new column
                    self.tuple[branch] = pd.DataFrame({branch: data})
        else:
            # Initialize a dictionary to collect the new columns
            columns_i = {}

            # Loop over the items in `data_to_add`
            for branch, data in data_to_add.items():
                if branch in self.tuple.columns:
                    # If the branch already exists, overwrite the column with new data
                    self.tuple[branch] = data
                else:
                    # If the branch doesn't exist, add it to the dictionary for future concatenation
                    columns_i[branch] = data

            # After the loop, concatenate the new columns in `columns_i` to the existing DataFrame
            if columns_i:
                new_columns_df = pd.DataFrame(columns_i)
                self.tuple = pd.concat([self.tuple, new_columns_df], axis=1)

    def get_branches(
        self,
        branches,
        transformers=None,
        numpy=False,
        scale_factor=1.0,
        transform_by_index=False,
        tag="",
        external_tuple=None,
        change_units={},
    ):

        if external_tuple is not None:
            working_tuple = external_tuple
        else:
            working_tuple = self.tuple

        data = working_tuple[branches] * scale_factor

        for item in change_units:
            data[item] *= change_units[item]

        if transformers:

            data = tfs.transform_df(
                data, transformers, transform_by_index=transform_by_index, tag=tag
            )

        if numpy:
            data = np.asarray(data[branches])

        return data

    def get_condition_chunks(
        self, network, particles_involved, name="MOTHER", mother=True
    ):

        Nparticles = network.Nparticles

        self.tuple["N_daughters"] = Nparticles

        conditions_graph = []
        personalised_transformers = {}
        for condition in network.conditions_graph:
            if mother:
                conditions_graph.append(condition)
                if condition != "N_daughters":
                    personalised_transformers[condition] = network.Transformers[
                        condition
                    ]
            else:
                conditions_graph.append(condition.replace("INTERMEDIATE", name))
                if condition != "N_daughters":
                    personalised_transformers[
                        condition.replace("INTERMEDIATE", name)
                    ] = network.Transformers[condition]

        graph_conditions = self.get_branches(
            conditions_graph,
            personalised_transformers,
            numpy=True,
        )
        daughter_conditions = []
        personalised_transformers = {}
        for particle in particles_involved:
            for daughter_condition in network.conditions_node:
                daughter_conditions.append(
                    daughter_condition.replace(
                        "DAUGHTERN", self.particle_map[particle]
                    ).replace("NMINUS1", f"{int(self.particle_map[particle][-1])-1}")
                )
                personalised_transformers[daughter_conditions[-1]] = (
                    network.Transformers[daughter_condition]
                )
        # print(daughter_conditions)
        # quit()
        node_conditions = self.get_branches(
            daughter_conditions,
            personalised_transformers,
            numpy=True,
        )
        node_conditions_tensor = node_conditions.reshape(
            len(node_conditions), Nparticles, len(network.conditions_node)
        ).reshape(-1, len(network.conditions_node))
        graph_conditions_tensor = np.repeat(
            graph_conditions, repeats=Nparticles, axis=0
        )
        conditions_tensor = np.concatenate(
            (node_conditions_tensor, graph_conditions_tensor), axis=1
        )

        # Batch conditions_tensor
        chunk_size = Nparticles * network.batch_size
        chunks = [
            conditions_tensor[i : i + chunk_size]
            for i in range(0, len(conditions_tensor), chunk_size)
        ]

        # Handle the last chunk if it's smaller than 1000 rows
        N_in_final_chunk = int(chunks[-1].shape[0] / Nparticles)
        if chunks[-1].shape[0] < chunk_size:
            last_chunk = chunks.pop(-1)
            # Zero-pad the last chunk to size (1000, 17)
            padded_chunk = np.zeros((chunk_size, np.shape(last_chunk)[1]))
            padded_chunk[: last_chunk.shape[0], :] = last_chunk
            chunks.append(padded_chunk)

        # (n_chunks, chunk_size, 17) if needed
        condition_chunks = np.array(chunks)

        return condition_chunks, N_in_final_chunk

    def gen_latent(self, network, chunks):

        Nparticles = network.Nparticles

        # Generate latent noise tensor
        graph_noise = np.random.normal(
            0,
            1,
            size=(np.shape(chunks)[0], network.batch_size, network.graph_latent_dims),
        )
        graph_noise = np.repeat(graph_noise, Nparticles, axis=1)
        node_noise = np.random.normal(
            0,
            1,
            size=(
                np.shape(chunks)[0],
                network.batch_size * Nparticles,
                network.node_latent_dims,
            ),
        )
        # (n_chunks, chunk_size, g+n_latent) if needed
        latent_noise_chunks = np.concatenate((graph_noise, node_noise), axis=2)

        return latent_noise_chunks

    def smearPV(self, smeared_PV_output):

        # print("Need to implement function to move the origin vertex too")

        distance_buffer = {}
        for particle in self.particles:
            for coordinate in ["X", "Y", "Z"]:
                distance_buffer[f"{particle}_{coordinate}"] = np.asarray(
                    self.tuple[f"{particle}_orig{coordinate}_TRUE"]
                    - self.tuple[f"{self.mother}_vtx{coordinate}_TRUE"]
                )

        B_plus_TRUEORIGINVERTEX = [
            self.tuple[f"{self.mother}_origX_TRUE"],
            self.tuple[f"{self.mother}_origY_TRUE"],
            self.tuple[f"{self.mother}_origZ_TRUE"],
        ]
        B_plus_TRUEENDVERTEX = [
            self.tuple[f"{self.mother}_vtxX_TRUE"],
            self.tuple[f"{self.mother}_vtxY_TRUE"],
            self.tuple[f"{self.mother}_vtxZ_TRUE"],
        ]
        theta, phi = pts.compute_angles(B_plus_TRUEORIGINVERTEX, B_plus_TRUEENDVERTEX)

        for branch in list(smeared_PV_output.keys()):
            self.tuple[branch] = smeared_PV_output[branch]

        B_plus_TRUEORIGINVERTEX = [
            self.tuple[f"{self.mother}_origX_TRUE"],
            self.tuple[f"{self.mother}_origY_TRUE"],
            self.tuple[f"{self.mother}_origZ_TRUE"],
        ]
        (
            self.tuple[f"{self.mother}_vtxX_TRUE"],
            self.tuple[f"{self.mother}_vtxY_TRUE"],
            self.tuple[f"{self.mother}_vtxZ_TRUE"],
        ) = pts.redefine_endpoint(
            B_plus_TRUEORIGINVERTEX, theta, phi, self.tuple[f"{self.mother}_TRUE_FD"]
        )

        for particle in self.particles:
            for coordinate in ["X", "Y", "Z"]:
                self.tuple[f"{particle}_orig{coordinate}_TRUE"] = (
                    self.tuple[f"{self.mother}_vtx{coordinate}_TRUE"]
                    + distance_buffer[f"{particle}_{coordinate}"]
                )

    def append_conditional_information(self, external_tuple=None, tag=""):

        if external_tuple is not None:
            working_tuple = external_tuple
        else:
            working_tuple = self.tuple

        for idx, particle in enumerate(self.particles):
            working_tuple[f"{tag}{particle}_TRUEID"] = working_tuple[
                f"{particle}_ID_TRUE"
            ]
            working_tuple[f"{tag}{particle}_FLIGHT"] = pts.compute_distance_wrapped(
                working_tuple, particle, "orig", self.mother, "vtx"
            )

        (
            working_tuple[f"{tag}{self.mother}_P"],
            working_tuple[f"{tag}{self.mother}_PT"],
        ) = pts.compute_reconstructed_mother_momenta(working_tuple, self.mother)

        (
            working_tuple[f"{tag}missing_{self.mother}_P"],
            working_tuple[f"{tag}missing_{self.mother}_PT"],
        ) = pts.compute_missing_momentum(working_tuple, self.mother, self.particles)

        for particle_i in range(0, len(self.particles)):
            (
                working_tuple[f"{tag}delta_{particle_i}_P"],
                working_tuple[f"{tag}delta_{particle_i}_PT"],
            ) = pts.compute_reconstructed_momentum_residual(
                working_tuple, self.particles[particle_i]
            )

        for particle in self.particles:
            working_tuple[f"{tag}angle_{particle}"] = pts.compute_angle(
                working_tuple, self.mother, f"{particle}"
            )

        working_tuple[f"{tag}IP_{self.mother}_true_vertex"] = (
            pts.compute_impactParameter(working_tuple, self.mother, self.particles)
        )
        for particle in self.particles:
            working_tuple[f"{tag}IP_{particle}_true_vertex"] = (
                pts.compute_impactParameter_i(working_tuple, self.mother, f"{particle}")
            )
        working_tuple[f"{tag}FD_{self.mother}_true_vertex"] = (
            pts.compute_flightDistance(working_tuple, self.mother, self.particles)
        )
        working_tuple[f"{tag}DIRA_{self.mother}_true_vertex"] = pts.compute_DIRA(
            working_tuple, self.mother, self.particles
        )

        if self.fully_reco:
            working_tuple[f"{tag}fully_reco"] = 1.0
        else:
            working_tuple[f"{tag}fully_reco"] = 0.0

        working_tuple[f"{tag}{self.mother}_nPositive_missing"] = float(
            self.nPositive_missing_particles
        )
        working_tuple[f"{tag}{self.mother}_nNegative_missing"] = float(
            self.nPositive_missing_particles
        )

        for particle in self.particles:

            if f"{particle}_PT" not in working_tuple:
                PT = working_tuple.eval(f"sqrt({particle}_PX**2 + {particle}_PY**2)")
            else:
                PT = working_tuple[f"{particle}_PT"]
            if f"{particle}_P" not in working_tuple:
                P = working_tuple.eval(
                    f"sqrt({particle}_PX**2 + {particle}_PY**2 + {particle}_PZ**2)"
                )
            else:
                P = working_tuple[f"{particle}_P"]

            working_tuple[f"{tag}{particle}_eta"] = -np.log(
                np.tan(np.arcsin(PT / P) / 2.0)
            )

        if self.intermediate_particle_name:

            if not isinstance(self.intermediate_particle_name, list):
                self.intermediate_particle_name = [self.intermediate_particle_name]

            for intermediate in self.intermediate_particle_name:

                combination = self.combined_particles[intermediate]
                combination_mapped = []
                for i in combination:
                    combination_mapped.append(self.particle_map[i])
                combination = combination_mapped

                (
                    working_tuple[f"{tag}{intermediate}_P"],
                    working_tuple[f"{tag}{intermediate}_PT"],
                ) = pts.compute_reconstructed_intermediate_momenta(
                    working_tuple, combination
                )

                (
                    working_tuple[f"{tag}missing_{intermediate}_P"],
                    working_tuple[f"{tag}missing_{intermediate}_PT"],
                ) = pts.compute_missing_momentum(
                    working_tuple, self.mother, combination
                )

                working_tuple[f"{tag}IP_{intermediate}_true_vertex"] = (
                    pts.compute_impactParameter(working_tuple, self.mother, combination)
                )
                working_tuple[f"{tag}FD_{intermediate}_true_vertex"] = (
                    pts.compute_flightDistance(working_tuple, self.mother, combination)
                )
                working_tuple[f"{tag}DIRA_{intermediate}_true_vertex"] = (
                    pts.compute_DIRA(working_tuple, self.mother, combination)
                )

        for combination in self.combined_particles:
            working_tuple[f"{tag}{combination}_N_daughters"] = len(
                list(self.combined_particles[combination])
            )
