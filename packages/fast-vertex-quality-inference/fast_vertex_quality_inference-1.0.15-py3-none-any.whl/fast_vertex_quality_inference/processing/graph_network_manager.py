import fast_vertex_quality_inference.tools.globals as myGlobals
import numpy as np
import pickle
import onnxruntime as ort
import fast_vertex_quality_inference.processing.transformers as tfs
import pandas as pd

ort.set_default_logger_severity(3)  # suppress shape warnings, due to graphs,


class graph_network_manager:

    def __init__(self, network, config, transformers, Nparticles, graphify=True):

        # myGlobals._verbose = True

        config = pickle.load(open(config, "rb"))

        self.targets_node = config["targets_node"]
        self.targets_graph = config["targets_graph"]
        self.conditions_node = config["conditions_node"]
        self.conditions_graph = config["conditions_graph"]
        self.batch_size = config["batch_size"]

        transformer_quantiles = pickle.load(open(transformers, "rb"))
        self.Transformers = {}
        for i, (key, quantiles) in enumerate(transformer_quantiles.items()):
            transformer_i = tfs.UpdatedTransformer()
            transformer_i.fit(quantiles, key)
            self.Transformers[key] = transformer_i

        # self.branches = self.conditions + self.targets

        if myGlobals._verbose:
            print(f"\n########\nStarting up ONNX InferenceSession for:\n{network}\n")
        self.session = ort.InferenceSession(network)

        # Check model inputs
        self.input_names = [inp.name for inp in self.session.get_inputs()]
        if myGlobals._verbose:
            print(f"\tModel Input Names: {self.input_names}")
        input_shapes = [inp.shape for inp in self.session.get_inputs()]
        if myGlobals._verbose:
            print(f"\tModel Input Dimensions: {input_shapes}")

        self.graphify = graphify
        if self.graphify:
            self.graph_latent_dims = config["graph_latent_dims"]
            self.node_latent_dims = config["node_latent_dims"]
            print(self.graph_latent_dims, self.node_latent_dims)
        else:
            self.targets = self.targets_graph
            self.conditions = self.conditions_graph
            self.latent_dims = config["latent_dims"]
            print(self.latent_dims)

        if myGlobals._verbose:
            print("\n")
        # Check model outputs
        self.output_names = [out.name for out in self.session.get_outputs()]
        if myGlobals._verbose:
            print(f"\tModel Output Names: {self.output_names}")
        output_shapes = [out.shape for out in self.session.get_outputs()]
        if myGlobals._verbose:
            print(f"\tModel Output Dimensions: {output_shapes}")
        if myGlobals._verbose:
            print("\n")

        if myGlobals._verbose:
            print(f"\t targets_node branches: {self.targets_node}\n")
            print(f"\t targets_graph branches: {self.targets_graph}\n")
            print(f"\t conditions_node branches: {self.conditions_node}\n")
            print(f"\t conditions_graph branches: {self.conditions_graph}\n")

        if myGlobals._verbose:
            print("\n########\n")

        self.Nparticles = Nparticles

    # vertexing_output, noise = vertexing_network.query_network(
    #                 latent_noise_chunks, condition_chunks, edge_index, batch
    #             )

    def get_branch_names(
        self, Nparticles, generalise=False, name="MOTHER", mother=True
    ):

        branches = []
        for i, branch in enumerate(self.targets_graph):
            if mother or generalise:
                branches.append(branch)
            else:
                branches.append(branch.replace("INTERMEDIATE", name))
        for j in range(1, Nparticles + 1):
            for i, branch in enumerate(self.targets_node):
                if not generalise:
                    branch = branch.replace("DAUGHTERN", f"DAUGHTER{j}")
                branches.append(branch)

        return branches

    def get_graph_tensors(self):

        # print(self.Nparticles)
        # compute edge_index, and batch tensors for a single batch
        edge_index_i = np.array(
            [
                [i, j]
                for i in range(self.Nparticles)
                for j in range(self.Nparticles)
                if i != j
            ]
        ).T
        edge_index = []
        for batch in range(self.batch_size):
            batch_offset = batch * self.Nparticles
            batch_edges = edge_index_i + batch_offset
            edge_index.append(batch_edges)
        edge_index = np.concatenate(edge_index, axis=1)
        batch = np.repeat(np.arange(self.batch_size), self.Nparticles)

        return edge_index, batch, self.batch_size

    def query_network_vanilla(
        self, inputs, process=True, numpy=False, ignore_targets=False
    ):

        noise = None

        for input_i in inputs:
            try:
                N = np.shape(input_i)[0]
            except:
                pass

        for idx, input_i in enumerate(inputs):
            if isinstance(input_i, str):
                if input_i == "noise":
                    noise = np.random.normal(0, 1, (N, self.latent_dims))
                    inputs[idx] = noise

        input_data = {}
        for idx, input_i in enumerate(inputs):
            input_data[self.input_names[idx]] = inputs[idx].astype(np.float32)

        output = self.session.run(self.output_names, input_data)[0]

        if not ignore_targets:
            df = {}
            for idx, target in enumerate(self.targets):
                df[target] = output[:, idx]
            output = pd.DataFrame.from_dict(df)

        if process:
            output = tfs.untransform_df(output, self.Transformers)

        if numpy:
            if ignore_targets:
                output = np.asarray(output)
            else:
                output = np.asarray(output[self.targets])

        return output, noise

    def query_network(
        self,
        latent_noise_chunks,
        condition_chunks,
        edge_index,
        batch,
        batch_size,
        Nparticles,
        N_in_final_chunk,
        process=True,
        numpy=False,
        ignore_targets=False,
        name="MOTHER",
        mother=True,
    ):

        self.targets = self.get_branch_names(self.Nparticles, name=name, mother=mother)
        self.targets_generalised = self.get_branch_names(
            self.Nparticles, generalise=True, name=name, mother=mother
        )

        ort_inputs = {"edge_index": edge_index, "batch": batch}
        Nchunks = np.shape(latent_noise_chunks)[0]
        for chunk in range(Nchunks):

            ort_inputs["latent"] = latent_noise_chunks[chunk].astype("f")
            ort_inputs["conditions"] = condition_chunks[chunk].astype("f")

            ort_outs = self.session.run(None, ort_inputs)

            graph_outputs = ort_outs[0]
            if len(self.targets_node) > 0:
                node_outputs = ort_outs[1]
                unfolded = node_outputs.reshape(
                    batch_size, Nparticles * len(self.targets_node)
                )
                chunk_output = np.concatenate((graph_outputs, unfolded), axis=1)
            else:
                chunk_output = graph_outputs

            if chunk == Nchunks - 1:

                chunk_output = chunk_output[:N_in_final_chunk]

            if chunk == 0:
                output = chunk_output
            else:
                output = np.concatenate((output, chunk_output), axis=0)

        if not ignore_targets:
            df = {}
            for idx, target in enumerate(self.targets):
                df[target] = output[:, idx]
            output = pd.DataFrame.from_dict(df)

        if process:
            output = tfs.untransform_df(
                output,
                self.Transformers,
                transformer_key_overrides=self.targets_generalised,
            )

        if numpy:
            if ignore_targets:
                output = np.asarray(output)
            else:
                output = np.asarray(output[self.targets])

        return output, latent_noise_chunks
