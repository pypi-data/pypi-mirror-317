# except ImportError:
#     from dataset import Dataset, load_dataset
#     from scpermut.tools.utils import scanpy_to_input, default_value, str2bool
#     from scpermut.tools.clust_compute import nn_overlap, batch_entropy_mixing_score,lisi_avg
# from dca.utils import str2bool,tuple_to_scalar
import argparse
import functools
import os
import sys

import keras
from sklearn.metrics import (accuracy_score, adjusted_mutual_info_score,
                             adjusted_rand_score, balanced_accuracy_score,
                             cohen_kappa_score, confusion_matrix,
                             davies_bouldin_score, f1_score, matthews_corrcoef,
                             normalized_mutual_info_score)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import compute_class_weight

# try :
#     from .dataset import Dataset, load_dataset
#     from ..tools.utils import scanpy_to_input, default_value, str2bool
#     from ..tools.clust_compute import nn_overlap, batch_entropy_mixing_score,lisi_avg


sys.path.insert(1, os.path.join(sys.path[0], ".."))

try:
    from .dataset import Dataset, load_dataset
except ImportError:
    from workflow.dataset import Dataset, load_dataset

try:
    from ..tools.clust_compute import (balanced_cohen_kappa_score,
                                       balanced_f1_score,
                                       balanced_matthews_corrcoef,
                                       batch_entropy_mixing_score, lisi_avg,
                                       nn_overlap)
    from ..tools.models import DANN_AE
    from ..tools.permutation import batch_generator_training_permuted
    from ..tools.utils import (check_dir, default_value, nan_to_0,
                               scanpy_to_input, str2bool)

except ImportError:
    from tools.clust_compute import (balanced_cohen_kappa_score,
                                     balanced_f1_score,
                                     balanced_matthews_corrcoef,
                                     batch_entropy_mixing_score, lisi_avg,
                                     nn_overlap)
    from tools.models import DANN_AE
    from tools.permutation import batch_generator_training_permuted
    from tools.utils import (check_dir, default_value, nan_to_0,
                             scanpy_to_input, str2bool)


f1_score = functools.partial(f1_score, average="macro")
import gc
import json
import os
import subprocess
import sys
import time

import matplotlib.pyplot as plt
import neptune
import numpy as np
import pandas as pd
import scanpy as sc
import seaborn as sns
import tensorflow as tf
from ax.service.managed_loop import optimize
# from numba import cuda
from neptune.utils import stringify_unsupported

# from ax import RangeParameter, SearchSpace, ParameterType, FixedParameter, ChoiceParameter

physical_devices = tf.config.list_physical_devices("GPU")
for gpu_instance in physical_devices:
    tf.config.experimental.set_memory_growth(gpu_instance, True)


# Reset Keras Session
def reset_keras():
    sess = tf.compat.v1.keras.backend.get_session()
    tf.compat.v1.keras.backend.clear_session()
    sess.close()
    sess = tf.compat.v1.keras.backend.get_session()

    try:
        del classifier  # this is from global space - change this as you need
    except:
        pass

    print(gc.collect())

    # use the same config as you used to create the session
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 1
    config.gpu_options.visible_device_list = "0"
    tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))


class Workflow:
    def __init__(self, run_file, working_dir):
        """
        run_file : a dictionary outputed by the function load_runfile
        """
        self.run_file = run_file
        # dataset identifiers
        self.dataset_name = self.run_file.dataset_name
        self.class_key = self.run_file.class_key
        self.batch_key = self.run_file.batch_key
        # normalization parameters
        self.filter_min_counts = (
            self.run_file.filter_min_counts
        )  # TODO :remove, we always want to do that
        self.normalize_size_factors = self.run_file.normalize_size_factors
        self.size_factor = self.run_file.size_factor
        self.scale_input = self.run_file.scale_input
        self.logtrans_input = self.run_file.logtrans_input
        self.use_hvg = self.run_file.use_hvg
        self.batch_size = self.run_file.batch_size
        # self.optimizer = self.run_file.optimizer
        # self.verbose = self.run_file[model_training_spec][verbose] # TODO : not implemented yet for DANN_AE
        # self.threads = self.run_file[model_training_spec][threads] # TODO : not implemented yet for DANN_AE
        self.learning_rate = self.run_file.learning_rate
        self.n_perm = 1
        self.semi_sup = False  # TODO : Not yet handled by DANN_AE, the case wwhere unlabeled cells are reconstructed as themselves
        self.unlabeled_category = "UNK"  # TODO : Not yet handled by DANN_AE, the case wwhere unlabeled cells are reconstructed as themselves

        # train test split # TODO : Simplify this, or at first only use the case where data is split according to batch
        self.test_split_key = self.run_file.test_split_key
        self.test_obs = self.run_file.test_obs
        self.test_index_name = self.run_file.test_index_name

        self.mode = self.run_file.mode
        self.pct_split = self.run_file.pct_split
        self.obs_key = self.run_file.obs_key
        self.n_keep = self.run_file.n_keep
        self.split_strategy = self.run_file.split_strategy
        self.keep_obs = self.run_file.keep_obs
        self.train_test_random_seed = self.run_file.train_test_random_seed
        # self.use_TEST = self.run_file[dataset_train_split][use_TEST] # TODO : remove, obsolete in the case of DANN_AE
        self.obs_subsample = self.run_file.obs_subsample
        # Create fake annotations
        self.make_fake = self.run_file.make_fake
        self.true_celltype = self.run_file.true_celltype
        self.false_celltype = self.run_file.false_celltype
        self.pct_false = self.run_file.pct_false

        self.working_dir = working_dir
        self.data_dir = working_dir + "/data"

        self.start_time = time.time()
        self.stop_time = time.time()
        # self.runtime_path = self.result_path + '/runtime.txt'

        self.run_done = False
        self.predict_done = False
        self.umap_done = False

        self.dataset = None
        self.model = None
        self.predictor = None

        self.training_kwds = {}
        self.network_kwds = {}

        ##### TODO : Add to runfile

        self.clas_loss_name = self.run_file.clas_loss_name
        self.clas_loss_name = default_value(
            self.clas_loss_name, "categorical_crossentropy"
        )
        self.balance_classes = self.run_file.balance_classes
        self.dann_loss_name = self.run_file.dann_loss_name
        self.dann_loss_name = default_value(
            self.dann_loss_name, "categorical_crossentropy"
        )
        self.rec_loss_name = self.run_file.rec_loss_name
        self.rec_loss_name = default_value(self.rec_loss_name, "MSE")

        self.clas_loss_fn = None
        self.dann_loss_fn = None
        self.rec_loss_fn = None

        self.weight_decay = self.run_file.weight_decay
        self.weight_decay = default_value(self.clas_loss_name, None)
        self.optimizer_type = self.run_file.optimizer_type
        self.optimizer_type = default_value(self.optimizer_type, "adam")

        self.clas_w = self.run_file.clas_w
        self.dann_w = self.run_file.dann_w
        self.rec_w = self.run_file.rec_w
        self.warmup_epoch = self.run_file.warmup_epoch

        self.num_classes = None
        self.num_batches = None

        self.ae_hidden_size = self.run_file.ae_hidden_size
        self.ae_hidden_size = default_value(
            self.ae_hidden_size, (128, 64, 128)
        )
        self.ae_hidden_dropout = self.run_file.ae_hidden_dropout

        self.dropout = self.run_file.dropout  # alternate way to give dropout
        self.layer1 = (
            self.run_file.layer1
        )  # alternate way to give model dimensions
        self.layer2 = self.run_file.layer2
        self.bottleneck = self.run_file.bottleneck

        # self.ae_hidden_dropout = default_value(self.ae_hidden_dropout , None)
        self.ae_activation = self.run_file.ae_activation
        self.ae_activation = default_value(self.ae_activation, "relu")
        self.ae_bottleneck_activation = self.run_file.ae_bottleneck_activation
        self.ae_bottleneck_activation = default_value(
            self.ae_bottleneck_activation, "linear"
        )
        self.ae_output_activation = self.run_file.ae_output_activation
        self.ae_output_activation = default_value(
            self.ae_output_activation, "relu"
        )
        self.ae_init = self.run_file.ae_init
        self.ae_init = default_value(self.ae_init, "glorot_uniform")
        self.ae_batchnorm = self.run_file.ae_batchnorm
        self.ae_batchnorm = default_value(self.ae_batchnorm, True)
        self.ae_l1_enc_coef = self.run_file.ae_l1_enc_coef
        self.ae_l1_enc_coef = default_value(self.ae_l1_enc_coef, 0)
        self.ae_l2_enc_coef = self.run_file.ae_l2_enc_coef
        self.ae_l2_enc_coef = default_value(self.ae_l2_enc_coef, 0)

        self.class_hidden_size = self.run_file.class_hidden_size
        self.class_hidden_size = default_value(
            self.class_hidden_size, None
        )  # default value will be initialize as [(bottleneck_size + num_classes)/2] once we'll know num_classes
        self.class_hidden_dropout = self.run_file.class_hidden_dropout
        self.class_batchnorm = self.run_file.class_batchnorm
        self.class_batchnorm = default_value(self.class_batchnorm, True)
        self.class_activation = self.run_file.class_activation
        self.class_activation = default_value(self.class_activation, "relu")
        self.class_output_activation = self.run_file.class_output_activation
        self.class_output_activation = default_value(
            self.class_output_activation, "softmax"
        )

        self.dann_hidden_size = self.run_file.dann_hidden_size
        self.dann_hidden_size = default_value(
            self.dann_hidden_size, None
        )  # default value will be initialize as [(bottleneck_size + num_batches)/2] once we'll know num_classes
        self.dann_hidden_dropout = self.run_file.dann_hidden_dropout
        self.dann_batchnorm = self.run_file.dann_batchnorm
        self.dann_batchnorm = default_value(self.dann_batchnorm, True)
        self.dann_activation = self.run_file.dann_activation
        self.dann_activation = default_value(self.dann_activation, "relu")
        self.dann_output_activation = self.run_file.dann_output_activation
        self.dann_output_activation = default_value(
            self.dann_output_activation, "softmax"
        )

        self.dann_ae = None

        self.pred_metrics_list = {
            "acc": accuracy_score,
            "mcc": matthews_corrcoef,
            "f1_score": f1_score,
            "KPA": cohen_kappa_score,
            "ARI": adjusted_rand_score,
            "NMI": normalized_mutual_info_score,
            "AMI": adjusted_mutual_info_score,
        }

        self.pred_metrics_list_balanced = {
            "balanced_acc": balanced_accuracy_score,
            "balanced_mcc": balanced_matthews_corrcoef,
            "balanced_f1_score": balanced_f1_score,
            "balanced_KPA": balanced_cohen_kappa_score,
        }

        self.clustering_metrics_list = {  #'clisi' : lisi_avg,
            "db_score": davies_bouldin_score
        }

        self.batch_metrics_list = {
            "batch_mixing_entropy": batch_entropy_mixing_score,
            #'ilisi': lisi_avg
        }
        self.metrics = []

        self.mean_loss_fn = keras.metrics.Mean(
            name="total loss"
        )  # This is a running average : it keeps the previous values in memory when it's called ie computes the previous and current values
        self.mean_clas_loss_fn = keras.metrics.Mean(name="classification loss")
        self.mean_dann_loss_fn = keras.metrics.Mean(name="dann loss")
        self.mean_rec_loss_fn = keras.metrics.Mean(name="reconstruction loss")

        self.training_scheme = self.run_file.training_scheme

        self.log_neptune = self.run_file.log_neptune
        self.run = None

        self.hparam_path = self.run_file.hparam_path
        self.hp_params = None
        self.opt_metric = default_value(self.run_file.opt_metric, None)

    def set_hyperparameters(self, params):

        print(f"setting hparams {params}")
        self.use_hvg = params["use_hvg"]
        self.batch_size = params["batch_size"]
        self.clas_w = params["clas_w"]
        self.dann_w = params["dann_w"]
        self.rec_w = params["rec_w"]
        self.ae_bottleneck_activation = params["ae_bottleneck_activation"]
        self.clas_loss_name = params["clas_loss_name"]
        self.size_factor = params["size_factor"]
        self.weight_decay = params["weight_decay"]
        self.learning_rate = params["learning_rate"]
        self.warmup_epoch = params["warmup_epoch"]
        self.dropout = params["dropout"]
        self.layer1 = params["layer1"]
        self.layer2 = params["layer2"]
        self.bottleneck = params["bottleneck"]
        self.training_scheme = params["training_scheme"]
        self.hp_params = params

    def start_neptune_log(self):
        if self.log_neptune:
            self.run = neptune.init_run(
                project="becavin-lab/benchmark",
                api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJiMmRkMWRjNS03ZGUwLTQ1MzQtYTViOS0yNTQ3MThlY2Q5NzUifQ==",
            )
            self.run[f"parameters/model"] = "scPermut"
            for par, val in self.run_file.__dict__.items():
                self.run[f"parameters/{par}"] = stringify_unsupported(
                    getattr(self, par)
                )
            if (
                self.hp_params
            ):  # Overwrites the defaults arguments contained in the runfile
                for par, val in self.hp_params.items():
                    self.run[f"parameters/{par}"] = stringify_unsupported(val)

    def add_custom_log(self, name, value):
        self.run[f"parameters/{name}"] = stringify_unsupported(value)

    def stop_neptune_log(self):
        self.run.stop()

    def process_dataset(self):
        # Loading dataset
        adata = load_dataset(
            dataset_dir=self.data_dir, dataset_name=self.dataset_name
        )

        self.dataset = Dataset(
            adata=adata,
            class_key=self.class_key,
            batch_key=self.batch_key,
            filter_min_counts=self.filter_min_counts,
            normalize_size_factors=self.normalize_size_factors,
            size_factor=self.size_factor,
            scale_input=self.scale_input,
            logtrans_input=self.logtrans_input,
            use_hvg=self.use_hvg,
            test_split_key=self.test_split_key,
            unlabeled_category=self.unlabeled_category,
        )

        if not "X_pca" in self.dataset.adata.obsm:
            print("Did not find existing PCA, computing it")
            sc.tl.pca(self.dataset.adata)
            self.dataset.adata.obsm["X_pca"] = np.asarray(
                self.dataset.adata.obsm["X_pca"]
            )
        # Processing dataset. Splitting train/test.
        self.dataset.normalize()

    def split_train_test(self):
        self.dataset.test_split(
            test_obs=self.test_obs, test_index_name=self.test_index_name
        )

    def split_train_val(self):
        self.dataset.train_split(
            mode=self.mode,
            pct_split=self.pct_split,
            obs_key=self.obs_key,
            n_keep=self.n_keep,
            keep_obs=self.keep_obs,
            split_strategy=self.split_strategy,
            obs_subsample=self.obs_subsample,
            train_test_random_seed=self.train_test_random_seed,
        )

        print("dataset has been preprocessed")
        self.dataset.create_inputs()

    def make_experiment(self):
        self.ae_hidden_size = [
            self.layer1,
            self.layer2,
            self.bottleneck,
            self.layer2,
            self.layer1,
        ]

        (
            self.dann_hidden_dropout,
            self.class_hidden_dropout,
            self.ae_hidden_dropout,
        ) = (self.dropout, self.dropout, self.dropout)

        adata_list = {
            "full": self.dataset.adata,
            "train": self.dataset.adata_train,
            "val": self.dataset.adata_val,
            "test": self.dataset.adata_test,
        }

        X_list = {
            "full": self.dataset.X,
            "train": self.dataset.X_train,
            "val": self.dataset.X_val,
            "test": self.dataset.X_test,
        }

        y_nooh_list = {
            "full": self.dataset.y,
            "train": self.dataset.y_train,
            "val": self.dataset.y_val,
            "test": self.dataset.y_test,
        }

        y_list = {
            "full": self.dataset.y_one_hot,
            "train": self.dataset.y_train_one_hot,
            "val": self.dataset.y_val_one_hot,
            "test": self.dataset.y_test_one_hot,
        }

        batch_list = {
            "full": self.dataset.batch_one_hot,
            "train": self.dataset.batch_train_one_hot,
            "val": self.dataset.batch_val_one_hot,
            "test": self.dataset.batch_test_one_hot,
        }

        X_pca_list = {
            "full": self.dataset.adata.obsm["X_pca"],
            "train": self.dataset.adata_train.obsm["X_pca"],
            "val": self.dataset.adata_val.obsm["X_pca"],
            "test": self.dataset.adata_test.obsm["X_pca"],
        }

        knn_cl = KNeighborsClassifier(n_neighbors=5)
        knn_cl.fit(X_pca_list["train"], y_nooh_list["train"])

        pseudo_y_val = pd.Series(
            knn_cl.predict(X_pca_list["val"]),
            index=adata_list["val"].obs_names,
        )
        pseudo_y_test = pd.Series(
            knn_cl.predict(X_pca_list["test"]),
            index=adata_list["test"].obs_names,
        )

        pseudo_y_full = pd.concat(
            [pseudo_y_val, pseudo_y_test, y_nooh_list["train"]]
        )
        pseudo_y_full = pseudo_y_full[
            adata_list["full"].obs_names
        ]  # reordering cells in the right order

        print(f"pseudo_y_full = {pseudo_y_full}")

        pseudo_y_list = {
            "full": self.dataset.ohe_celltype.transform(
                np.array(pseudo_y_full).reshape(-1, 1)
            )
            .astype(float)
            .todense(),
            "train": y_list["train"],
            "val": self.dataset.ohe_celltype.transform(
                np.array(pseudo_y_val).reshape(-1, 1)
            )
            .astype(float)
            .todense(),
            "test": self.dataset.ohe_celltype.transform(
                np.array(pseudo_y_test).reshape(-1, 1)
            )
            .astype(float)
            .todense(),
        }

        print({i: adata_list[i] for i in adata_list})
        print({i: len(y_list[i]) for i in y_list})
        print(
            f"sum : {len(y_list['train']) + len(y_list['test']) + len(y_list['val'])}"
        )
        print(f"full: {len(y_list['full'])}")

        self.num_classes = len(np.unique(self.dataset.y_train))
        self.num_batches = len(np.unique(self.dataset.batch))

        bottleneck_size = int(
            self.ae_hidden_size[int(len(self.ae_hidden_size) / 2)]
        )

        self.class_hidden_size = default_value(
            self.class_hidden_size, (bottleneck_size + self.num_classes) / 2
        )  # default value [(bottleneck_size + num_classes)/2]
        self.dann_hidden_size = default_value(
            self.dann_hidden_size, (bottleneck_size + self.num_batches) / 2
        )  # default value [(bottleneck_size + num_batches)/2]

        # Creation of model
        self.dann_ae = DANN_AE(
            ae_hidden_size=self.ae_hidden_size,
            ae_hidden_dropout=self.ae_hidden_dropout,
            ae_activation=self.ae_activation,
            ae_output_activation=self.ae_output_activation,
            ae_bottleneck_activation=self.ae_bottleneck_activation,
            ae_init=self.ae_init,
            ae_batchnorm=self.ae_batchnorm,
            ae_l1_enc_coef=self.ae_l1_enc_coef,
            ae_l2_enc_coef=self.ae_l2_enc_coef,
            num_classes=self.num_classes,
            class_hidden_size=self.class_hidden_size,
            class_hidden_dropout=self.class_hidden_dropout,
            class_batchnorm=self.class_batchnorm,
            class_activation=self.class_activation,
            class_output_activation=self.class_output_activation,
            num_batches=self.num_batches,
            dann_hidden_size=self.dann_hidden_size,
            dann_hidden_dropout=self.dann_hidden_dropout,
            dann_batchnorm=self.dann_batchnorm,
            dann_activation=self.dann_activation,
            dann_output_activation=self.dann_output_activation,
        )

        self.optimizer = self.get_optimizer(
            self.learning_rate, self.weight_decay, self.optimizer_type
        )
        self.rec_loss_fn, self.clas_loss_fn, self.dann_loss_fn = (
            self.get_losses(y_list)
        )  # redundant
        training_scheme = self.get_scheme()
        start_time = time.time()

        print(
            "bottleneck activation : " + self.dann_ae.ae_bottleneck_activation
        )
        # Training
        history = self.train_scheme(
            training_scheme=training_scheme,
            verbose=False,
            ae=self.dann_ae,
            adata_list=adata_list,
            X_list=X_list,
            y_list=y_list,
            batch_list=batch_list,
            pseudo_y_list=pseudo_y_list,
            #  optimizer= self.optimizer, # not an **loop_param since it resets between strategies
            clas_loss_fn=self.clas_loss_fn,
            dann_loss_fn=self.dann_loss_fn,
            rec_loss_fn=self.rec_loss_fn,
        )
        stop_time = time.time()
        if self.log_neptune:
            self.run["evaluation/training_time"] = stop_time - start_time
        # TODO also make it on gpu with smaller batch size
        if self.log_neptune:
            neptune_run_id = self.run["sys/id"].fetch()
            save_dir = (
                self.working_dir
                + "experiment_script/results/"
                + str(neptune_run_id)
                + "/"
            )
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            y_true_full = adata_list["full"].obs[f"true_{self.class_key}"]
            ct_prop = (
                pd.Series(y_true_full).value_counts()
                / pd.Series(y_true_full).value_counts().sum()
            )
            sizes = {
                "xxsmall": list(ct_prop[ct_prop < 0.001].index),
                "small": list(
                    ct_prop[(ct_prop >= 0.001) & (ct_prop < 0.01)].index
                ),
                "medium": list(
                    ct_prop[(ct_prop >= 0.01) & (ct_prop < 0.1)].index
                ),
                "large": list(ct_prop[ct_prop >= 0.1].index),
            }

            for group in ["full", "train", "val", "test"]:
                with tf.device("CPU"):
                    input_tensor = {
                        k: tf.convert_to_tensor(v)
                        for k, v in scanpy_to_input(
                            adata_list[group], ["size_factors"]
                        ).items()
                    }
                    enc, clas, dann, rec = self.dann_ae(
                        input_tensor, training=False
                    ).values()  # Model predict

                    if (
                        group == "full"
                    ):  # saving full predictions as probability output from the classifier
                        y_pred_proba = pd.DataFrame(
                            np.asarray(clas),
                            index=adata_list["full"].obs_names,
                            columns=self.dataset.ohe_celltype.categories_[0],
                        )
                        y_pred_proba.to_csv(
                            save_dir + f"y_pred_proba_full.csv"
                        )
                        self.run[
                            f"evaluation/{group}/y_pred_proba_full"
                        ].track_files(save_dir + f"y_pred_proba_full.csv")

                    clas = np.eye(clas.shape[1])[np.argmax(clas, axis=1)]

                    y_pred = self.dataset.ohe_celltype.inverse_transform(
                        clas
                    ).reshape(
                        -1,
                    )
                    y_true = adata_list[group].obs[f"true_{self.class_key}"]
                    batches = np.asarray(
                        batch_list[group].argmax(axis=1)
                    ).reshape(
                        -1,
                    )
                    split = adata_list[group].obs["train_split"]

                    # Saving confusion matrices
                    labels = list(
                        set(np.unique(y_true)).union(set(np.unique(y_pred)))
                    )
                    cm_no_label = confusion_matrix(y_true, y_pred)
                    print(f"no label : {cm_no_label.shape}")
                    cm = confusion_matrix(y_true, y_pred, labels=labels)
                    cm_norm = cm / cm.sum(axis=1, keepdims=True)
                    print(f"label : {cm.shape}")
                    cm_to_plot = pd.DataFrame(
                        cm_norm, index=labels, columns=labels
                    )
                    cm_to_save = pd.DataFrame(cm, index=labels, columns=labels)
                    cm_to_plot = cm_to_plot.fillna(value=0)
                    cm_to_save = cm_to_save.fillna(value=0)
                    cm_to_save.to_csv(
                        save_dir + f"confusion_matrix_{group}.csv"
                    )
                    self.run[
                        f"evaluation/{group}/confusion_matrix_file"
                    ].track_files(save_dir + f"confusion_matrix_{group}.csv")
                    size = len(labels)
                    f, ax = plt.subplots(figsize=(size / 1.5, size / 1.5))
                    sns.heatmap(
                        cm_to_plot,
                        annot=True,
                        ax=ax,
                        fmt=".2f",
                        vmin=0,
                        vmax=1,
                    )
                    show_mask = np.asarray(cm_to_plot > 0.01)
                    print(f"label df : {cm_to_plot.shape}")
                    for text, show_annot in zip(
                        ax.texts,
                        (element for row in show_mask for element in row),
                    ):
                        text.set_visible(show_annot)

                    self.run[f"evaluation/{group}/confusion_matrix"].upload(f)

                    # Computing batch mixing metrics
                    if (
                        len(
                            np.unique(
                                np.asarray(batch_list[group].argmax(axis=1))
                            )
                        )
                        >= 2
                    ):  # If there are more than 2 batches in this group
                        for metric in self.batch_metrics_list:
                            self.run[f"evaluation/{group}/{metric}"] = (
                                self.batch_metrics_list[metric](enc, batches)
                            )
                            print(
                                type(
                                    self.batch_metrics_list[metric](
                                        enc, batches
                                    )
                                )
                            )

                    # Computing classification metrics
                    for metric in self.pred_metrics_list:
                        self.run[f"evaluation/{group}/{metric}"] = (
                            self.pred_metrics_list[metric](y_true, y_pred)
                        )

                    for metric in self.pred_metrics_list_balanced:
                        self.run[f"evaluation/{group}/{metric}"] = (
                            self.pred_metrics_list_balanced[metric](
                                y_true, y_pred
                            )
                        )

                    # Metrics by size of ct
                    for s in sizes:
                        idx_s = np.isin(
                            y_true, sizes[s]
                        )  # Boolean array, no issue to index y_pred
                        y_true_sub = y_true[idx_s]
                        y_pred_sub = y_pred[idx_s]
                        print(s)
                        for metric in self.pred_metrics_list:
                            self.run[f"evaluation/{group}/{s}/{metric}"] = (
                                nan_to_0(
                                    self.pred_metrics_list[metric](
                                        y_true_sub, y_pred_sub
                                    )
                                )
                            )

                        for metric in self.pred_metrics_list_balanced:
                            self.run[f"evaluation/{group}/{s}/{metric}"] = (
                                nan_to_0(
                                    self.pred_metrics_list_balanced[metric](
                                        y_true_sub, y_pred_sub
                                    )
                                )
                            )

                    # Computing clustering metrics
                    for metric in self.clustering_metrics_list:
                        self.run[f"evaluation/{group}/{metric}"] = (
                            self.clustering_metrics_list[metric](enc, y_pred)
                        )

                    if group == "full":
                        y_pred_df = pd.DataFrame(
                            {"pred": y_pred, "true": y_true, "split": split},
                            index=adata_list[group].obs_names,
                        )
                        split = pd.DataFrame(
                            split, index=adata_list[group].obs_names
                        )
                        np.save(
                            save_dir + f"latent_space_{group}.npy", enc.numpy()
                        )
                        y_pred_df.to_csv(save_dir + f"predictions_{group}.csv")
                        split.to_csv(save_dir + f"split_{group}.csv")
                        self.run[
                            f"evaluation/{group}/latent_space"
                        ].track_files(save_dir + f"latent_space_{group}.npy")
                        self.run[
                            f"evaluation/{group}/predictions"
                        ].track_files(save_dir + f"predictions_{group}.csv")

                        # Saving umap representation
                        pred_adata = sc.AnnData(
                            X=adata_list[group].X,
                            obs=adata_list[group].obs,
                            var=adata_list[group].var,
                        )
                        pred_adata.obs[f"{self.class_key}_pred"] = y_pred_df[
                            "pred"
                        ]
                        pred_adata.obsm["latent_space"] = enc.numpy()
                        sc.pp.neighbors(pred_adata, use_rep="latent_space")
                        sc.tl.umap(pred_adata)
                        np.save(
                            save_dir + f"umap_{group}.npy",
                            pred_adata.obsm["X_umap"],
                        )
                        self.run[f"evaluation/{group}/umap"].track_files(
                            save_dir + f"umap_{group}.npy"
                        )
                        sc.set_figure_params(figsize=(15, 10), dpi=300)
                        fig_class = sc.pl.umap(
                            pred_adata,
                            color=f"true_{self.class_key}",
                            size=10,
                            return_fig=True,
                        )
                        fig_pred = sc.pl.umap(
                            pred_adata,
                            color=f"{self.class_key}_pred",
                            size=10,
                            return_fig=True,
                        )
                        fig_batch = sc.pl.umap(
                            pred_adata,
                            color=self.batch_key,
                            size=10,
                            return_fig=True,
                        )
                        fig_split = sc.pl.umap(
                            pred_adata,
                            color="train_split",
                            size=10,
                            return_fig=True,
                        )
                        self.run[f"evaluation/{group}/true_umap"].upload(
                            fig_class
                        )
                        self.run[f"evaluation/{group}/pred_umap"].upload(
                            fig_pred
                        )
                        self.run[f"evaluation/{group}/batch_umap"].upload(
                            fig_batch
                        )
                        self.run[f"evaluation/{group}/split_umap"].upload(
                            fig_split
                        )

        if self.opt_metric:
            split, metric = self.opt_metric.split("-")
            self.run.wait()
            opt_metric = self.run[f"evaluation/{split}/{metric}"].fetch()
            print("opt_metric")
            print(opt_metric)
        else:
            opt_metric = None
        # Redondant, à priori c'est le mcc qu'on a déjà calculé au dessus.
        # with tf.device('CPU'):
        #     inp = scanpy_to_input(adata_list['val'],['size_factors'])
        #     inp = {k:tf.convert_to_tensor(v) for k,v in inp.items()}
        #     _, clas, dann, rec = self.dann_ae(inp, training=False).values()
        #     clas = np.eye(clas.shape[1])[np.argmax(clas, axis=1)]
        #     opt_metric = self.pred_metrics_list_balanced['balanced_mcc'](np.asarray(y_list['val'].argmax(axis=1)), clas.argmax(axis=1)) # We retrieve the last metric of interest
        # if self.log_neptune:
        #     self.run.stop()
        del enc
        del clas
        del dann
        del rec
        # # del _
        # del input_tensor
        # # del inp
        del self.dann_ae
        # del self.dataset
        del history
        del self.optimizer
        del self.rec_loss_fn
        del self.clas_loss_fn
        del self.dann_loss_fn

        gc.collect()
        tf.keras.backend.clear_session()

        return opt_metric

    def train_scheme(self, training_scheme, verbose=True, **loop_params):
        """
        training scheme : dictionnary explaining the succession of strategies to use as keys with the corresponding number of epochs and use_perm as values.
                        ex :  training_scheme_3 = {"warmup_dann" : (10, False), "full_model":(10, False)}
        """
        history = {"train": {}, "val": {}}  # initialize history
        for group in history.keys():
            history[group] = {
                "total_loss": [],
                "clas_loss": [],
                "dann_loss": [],
                "rec_loss": [],
            }
            for m in self.pred_metrics_list:
                history[group][m] = []
            for m in self.pred_metrics_list_balanced:
                history[group][m] = []

        # if self.log_neptune:
        #     for group in history:
        #         for par,val in history[group].items():
        #             self.run[f"training/{group}/{par}"] = []
        i = 0

        total_epochs = np.sum([n_epochs for _, n_epochs, _ in training_scheme])
        running_epoch = 0

        for strategy, n_epochs, use_perm in training_scheme:
            optimizer = self.get_optimizer(
                self.learning_rate, self.weight_decay, self.optimizer_type
            )  # resetting optimizer state when switching strategy
            if verbose:
                print(
                    f"Step number {i}, running {strategy} strategy with permuation = {use_perm} for {n_epochs} epochs"
                )
                time_in = time.time()

                # Early stopping for those strategies only
            if strategy in [
                "full_model",
                "classifier_branch",
                "permutation_only",
                "encoder_classifier",
            ]:
                wait = 0
                best_epoch = 0
                patience = 20
                min_delta = 0
                if strategy == "permutation_only":
                    monitored = "rec_loss"
                    es_best = np.inf  # initialize early_stopping
                else:
                    split, metric = self.opt_metric.split("-")
                    monitored = metric
                    es_best = -np.inf
            memory = {}
            if strategy in [
                "warmup_dann_pseudolabels",
                "full_model_pseudolabels",
            ]:  # We use the pseudolabels computed with the model
                input_tensor = {
                    k: tf.convert_to_tensor(v)
                    for k, v in scanpy_to_input(
                        loop_params["adata_list"]["full"], ["size_factors"]
                    ).items()
                }
                enc, clas, dann, rec = self.dann_ae(
                    input_tensor, training=False
                ).values()  # Model predict
                pseudo_full = np.eye(clas.shape[1])[np.argmax(clas, axis=1)]
                pseudo_full[
                    loop_params["adata_list"]["full"].obs["train_split"]
                    == "train",
                    :,
                ] = loop_params["pseudo_y_list"][
                    "train"
                ]  # the true labels
                loop_params["pseudo_y_list"]["full"] = pseudo_full
                for group in ["val", "test"]:
                    loop_params["pseudo_y_list"][group] = pseudo_full[
                        loop_params["adata_list"]["full"].obs["train_split"]
                        == group,
                        :,
                    ]  # the predicted labels in test and val

            elif strategy in ["warmup_dann_semisup"]:
                memory = {}
                memory["pseudo_full"] = loop_params["pseudo_y_list"]["full"]
                for group in ["val", "test"]:
                    loop_params["pseudo_y_list"]["full"][
                        loop_params["adata_list"]["full"].obs["train_split"]
                        == group,
                        :,
                    ] = (
                        self.unlabeled_category
                    )  # set val and test to self.unlabeled_category
                    loop_params["pseudo_y_list"][group] = pseudo_full[
                        loop_params["adata_list"]["full"].obs["train_split"]
                        == group,
                        :,
                    ]

            else:
                if (
                    memory
                ):  # In case we are no longer using semi sup config, we reset to the previous known pseudolabels
                    for group in ["val", "test", "full"]:
                        loop_params["pseudo_y_list"][group] = memory[group]
                    memory = {}

            for epoch in range(1, n_epochs + 1):
                running_epoch += 1
                print(
                    f"Epoch {running_epoch}/{total_epochs}, Current strat Epoch {epoch}/{n_epochs}"
                )
                history, _, _, _, _ = self.training_loop(
                    history=history,
                    training_strategy=strategy,
                    use_perm=use_perm,
                    optimizer=optimizer,
                    **loop_params,
                )

                if self.log_neptune:
                    for group in history:
                        for par, value in history[group].items():
                            self.run[f"training/{group}/{par}"].append(
                                value[-1]
                            )
                            if physical_devices:
                                self.run[
                                    "training/train/tf_GPU_memory"
                                ].append(
                                    tf.config.experimental.get_memory_info(
                                        "GPU:0"
                                    )["current"]
                                    / 1e6
                                )
                if strategy in [
                    "full_model",
                    "classifier_branch",
                    "permutation_only",
                    "encoder_classifier",
                ]:
                    # Early stopping
                    wait += 1
                    monitored_value = history["val"][monitored][-1]

                    if "loss" in monitored:
                        if monitored_value < es_best - min_delta:
                            best_epoch = epoch
                            es_best = monitored_value
                            wait = 0
                            best_model = self.dann_ae.get_weights()
                    else:
                        if monitored_value > es_best + min_delta:
                            best_epoch = epoch
                            es_best = monitored_value
                            wait = 0
                            best_model = self.dann_ae.get_weights()
                    if wait >= patience:
                        print(
                            f"Early stopping at epoch {best_epoch}, restoring model parameters from this epoch"
                        )
                        self.dann_ae.set_weights(best_model)
                        break
            del optimizer

            if verbose:
                time_out = time.time()
                print(f"Strategy duration : {time_out - time_in} s")
        if self.log_neptune:
            self.run[f"training/{group}/total_epochs"] = running_epoch
        return history

    def training_loop(
        self,
        history,
        ae,
        adata_list,
        X_list,
        y_list,
        pseudo_y_list,
        batch_list,
        optimizer,
        clas_loss_fn,
        dann_loss_fn,
        rec_loss_fn,
        use_perm=True,
        training_strategy="full_model",
        verbose=False,
    ):
        """
        A consolidated training loop function that covers common logic used in different training strategies.

        training_strategy : one of ["full", "warmup_dann", "warmup_dann_no_rec", "classifier_branch", "permutation_only"]
            - full_model : trains the whole model, optimizing the 3 losses (reconstruction, classification, anti batch discrimination ) at once
            - warmup_dann : trains the dann, encoder and decoder with reconstruction (no permutation because unsupervised), maximizing the dann loss and minimizing the reconstruction loss
            - warmup_dann_no_rec : trains the dann and encoder without reconstruction, maximizing the dann loss only.
            - dann_with_ae : same as warmup dann but with permutation. Separated in two strategies because this one is supervised
            - classifier_branch : trains the classifier branch only, without the encoder. Use to fine tune the classifier once training is over
            - permutation_only : trains the autoencoder with permutations, optimizing the reconstruction loss without the classifier
        use_perm : True by default except form "warmup_dann" training strategy. Note that for training strategies that don't involve the reconstruction, this parameter has no impact on training
        """

        self.unfreeze_all(ae)  # resetting freeze state
        if training_strategy == "full_model":
            group = "train"
        elif training_strategy == "full_model_pseudolabels":
            group = "full"
        elif training_strategy == "encoder_classifier":
            group = "train"
            self.freeze_block(ae, "all_but_classifier")  # training only
        elif training_strategy in [
            "warmup_dann",
            "warmup_dann_pseudolabels",
            "warmup_dann_semisup",
        ]:
            group = "full"  # semi-supervised setting
            ae.classifier.trainable = False  # Freezing classifier just to be sure but should not be necessary since gradient won't be propagating in this branch
        elif training_strategy == "warmup_dann_train":
            group = "train"  # semi-supervised setting
            ae.classifier.trainable = False  # Freezing classifier just to be sure but should not be necessary since gradient won't be propagating in this branch
        elif training_strategy == "warmup_dann_no_rec":
            group = "full"
            self.freeze_block(ae, "all_but_dann")
        elif training_strategy == "dann_with_ae":
            group = "train"
            ae.classifier.trainable = False
        elif training_strategy == "classifier_branch":
            group = "train"
            self.freeze_block(
                ae, "all_but_classifier_branch"
            )  # training only classifier branch
        elif training_strategy == "permutation_only":
            group = "train"
            self.freeze_block(ae, "all_but_autoencoder")
        elif training_strategy == "no_dann":
            group = "train"
            self.freeze_block(ae, "freeze_dann")
        elif training_strategy == "no_decoder":
            group = "train"
            self.freeze_block(ae, "freeze_dec")

        print(f"use_perm = {use_perm}")
        batch_generator = batch_generator_training_permuted(
            X=X_list[group],
            y=pseudo_y_list[
                group
            ],  # We use pseudo labels for val and test. y_train are true labels
            batch_ID=batch_list[group],
            sf=adata_list[group].obs["size_factors"],
            ret_input_only=False,
            batch_size=self.batch_size,
            n_perm=1,
            unlabeled_category=self.unlabeled_category,  # Those cells are matched with themselves during AE training
            use_perm=use_perm,
        )
        n_obs = adata_list[group].n_obs
        steps = n_obs // self.batch_size + 1
        n_steps = steps
        n_samples = 0

        self.mean_loss_fn.reset_state()
        self.mean_clas_loss_fn.reset_state()
        self.mean_dann_loss_fn.reset_state()
        self.mean_rec_loss_fn.reset_state()

        for step in range(1, n_steps + 1):
            input_batch, output_batch = next(batch_generator)
            # X_batch, sf_batch = input_batch.values()
            clas_batch, dann_batch, rec_batch = output_batch.values()

            with tf.GradientTape() as tape:
                # Forward pass
                input_batch = {
                    k: tf.convert_to_tensor(v) for k, v in input_batch.items()
                }
                enc, clas, dann, rec = ae(input_batch, training=True).values()

                # Computing loss
                clas_loss = tf.reduce_mean(clas_loss_fn(clas_batch, clas))
                dann_loss = tf.reduce_mean(dann_loss_fn(dann_batch, dann))
                rec_loss = tf.reduce_mean(rec_loss_fn(rec_batch, rec))
                if training_strategy in [
                    "full_model",
                    "full_model_pseudolabels",
                ]:
                    loss = tf.add_n(
                        [self.clas_w * clas_loss]
                        + [self.dann_w * dann_loss]
                        + [self.rec_w * rec_loss]
                        + ae.losses
                    )
                elif training_strategy in [
                    "warmup_dann",
                    "warmup_dann_pseudolabels",
                    "warmup_dann_train",
                    "warmup_dann_semisup",
                ]:
                    loss = tf.add_n(
                        [self.dann_w * dann_loss]
                        + [self.rec_w * rec_loss]
                        + ae.losses
                    )
                elif training_strategy == "warmup_dann_no_rec":
                    loss = tf.add_n([self.dann_w * dann_loss] + ae.losses)
                elif training_strategy == "dann_with_ae":
                    loss = tf.add_n(
                        [self.dann_w * dann_loss]
                        + [self.rec_w * rec_loss]
                        + ae.losses
                    )
                elif training_strategy == "classifier_branch":
                    loss = tf.add_n([self.clas_w * clas_loss] + ae.losses)
                elif training_strategy == "encoder_classifier":
                    loss = tf.add_n([self.clas_w * clas_loss] + ae.losses)
                elif training_strategy == "permutation_only":
                    loss = tf.add_n([self.rec_w * rec_loss] + ae.losses)
                elif training_strategy == "no_dann":
                    loss = tf.add_n(
                        [self.rec_w * rec_loss]
                        + [self.clas_w * clas_loss]
                        + ae.losses
                    )
                elif training_strategy == "no_decoder":
                    loss = tf.add_n(
                        [self.dann_w * dann_loss]
                        + [self.clas_w * clas_loss]
                        + ae.losses
                    )

            # Backpropagation
            n_samples += enc.shape[0]
            gradients = tape.gradient(loss, ae.trainable_variables)

            optimizer.apply_gradients(zip(gradients, ae.trainable_variables))

            self.mean_loss_fn(loss.__float__())
            self.mean_clas_loss_fn(clas_loss.__float__())
            self.mean_dann_loss_fn(dann_loss.__float__())
            self.mean_rec_loss_fn(rec_loss.__float__())

            if verbose:
                self.print_status_bar(
                    n_samples,
                    n_obs,
                    [
                        self.mean_loss_fn,
                        self.mean_clas_loss_fn,
                        self.mean_dann_loss_fn,
                        self.mean_rec_loss_fn,
                    ],
                    self.metrics,
                )
        self.print_status_bar(
            n_samples,
            n_obs,
            [
                self.mean_loss_fn,
                self.mean_clas_loss_fn,
                self.mean_dann_loss_fn,
                self.mean_rec_loss_fn,
            ],
            self.metrics,
        )
        history, _, clas, dann, rec = self.evaluation_pass(
            history,
            ae,
            adata_list,
            X_list,
            y_list,
            batch_list,
            clas_loss_fn,
            dann_loss_fn,
            rec_loss_fn,
        )
        del input_batch
        return history, _, clas, dann, rec

    def evaluation_pass(
        self,
        history,
        ae,
        adata_list,
        X_list,
        y_list,
        batch_list,
        clas_loss_fn,
        dann_loss_fn,
        rec_loss_fn,
    ):
        """
        evaluate model and logs metrics. Depending on "on parameter, computes it on train and val or train,val and test.

        on : "epoch_end" to evaluate on train and val, "training_end" to evaluate on train, val and "test".
        """
        for group in ["train", "val"]:  # evaluation round
            inp = scanpy_to_input(adata_list[group], ["size_factors"])
            with tf.device("CPU"):
                inp = {k: tf.convert_to_tensor(v) for k, v in inp.items()}
                _, clas, dann, rec = ae(inp, training=False).values()

                #         return _, clas, dann, rec
                clas_loss = tf.reduce_mean(
                    clas_loss_fn(y_list[group], clas)
                ).numpy()
                history[group]["clas_loss"] += [clas_loss]
                dann_loss = tf.reduce_mean(
                    dann_loss_fn(batch_list[group], dann)
                ).numpy()
                history[group]["dann_loss"] += [dann_loss]
                rec_loss = tf.reduce_mean(
                    rec_loss_fn(X_list[group], rec)
                ).numpy()
                history[group]["rec_loss"] += [rec_loss]
                history[group]["total_loss"] += [
                    self.clas_w * clas_loss
                    + self.dann_w * dann_loss
                    + self.rec_w * rec_loss
                    + np.sum(ae.losses)
                ]  # using numpy to prevent memory leaks
                # history[group]['total_loss'] += [tf.add_n([self.clas_w * clas_loss] + [self.dann_w * dann_loss] + [self.rec_w * rec_loss] + ae.losses).numpy()]

                clas = np.eye(clas.shape[1])[np.argmax(clas, axis=1)]
                for (
                    metric
                ) in self.pred_metrics_list:  # only classification metrics ATM
                    history[group][metric] += [
                        self.pred_metrics_list[metric](
                            np.asarray(y_list[group].argmax(axis=1)).reshape(
                                -1,
                            ),
                            clas.argmax(axis=1),
                        )
                    ]  # y_list are onehot encoded
                for (
                    metric
                ) in (
                    self.pred_metrics_list_balanced
                ):  # only classification metrics ATM
                    history[group][metric] += [
                        self.pred_metrics_list_balanced[metric](
                            np.asarray(y_list[group].argmax(axis=1)).reshape(
                                -1,
                            ),
                            clas.argmax(axis=1),
                        )
                    ]  # y_list are onehot encoded
        del inp
        return history, _, clas, dann, rec

    # def evaluation_pass_gpu(self,history, ae, adata_list, X_list, y_list, batch_list, clas_loss_fn, dann_loss_fn, rec_loss_fn):
    #     '''
    #     evaluate model and logs metrics. Depending on "on parameter, computes it on train and val or train,val and test.

    #     on : "epoch_end" to evaluate on train and val, "training_end" to evaluate on train, val and "test".
    #     '''
    #     for group in ['train', 'val']: # evaluation round
    #         # inp = scanpy_to_input(adata_list[group],['size_factors'])
    #         batch_generator = batch_generator_training_permuted(X = X_list[group],
    #                                                 y = y_list[group],
    #                                                 batch_ID = batch_list[group],
    #                                                 sf = adata_list[group].obs['size_factors'],
    #                                                 ret_input_only=False,
    #                                                 batch_size=self.batch_size,
    #                                                 n_perm=1,
    #                                                 use_perm=use_perm)
    #         n_obs = adata_list[group].n_obs
    #         steps = n_obs // self.batch_size + 1
    #         n_steps = steps
    #         n_samples = 0

    #         clas_batch, dann_batch, rec_batch = output_batch.values()

    #         with tf.GradientTape() as tape:
    #             input_batch = {k:tf.convert_to_tensor(v) for k,v in input_batch.items()}
    #             enc, clas, dann, rec = ae(input_batch, training=True).values()
    #             clas_loss = tf.reduce_mean(clas_loss_fn(clas_batch, clas)).numpy()
    #             dann_loss = tf.reduce_mean(dann_loss_fn(dann_batch, dann)).numpy()
    #             rec_loss = tf.reduce_mean(rec_loss_fn(rec_batch, rec)).numpy()
    #     #         return _, clas, dann, rec
    #             history[group]['clas_loss'] += [clas_loss]
    #             history[group]['dann_loss'] += [dann_loss]
    #             history[group]['rec_loss'] += [rec_loss]
    #             history[group]['total_loss'] += [self.clas_w * clas_loss + self.dann_w * dann_loss + self.rec_w * rec_loss + np.sum(ae.losses)] # using numpy to prevent memory leaks
    #             # history[group]['total_loss'] += [tf.add_n([self.clas_w * clas_loss] + [self.dann_w * dann_loss] + [self.rec_w * rec_loss] + ae.losses).numpy()]

    #             clas = np.eye(clas.shape[1])[np.argmax(clas, axis=1)]
    #             for metric in self.pred_metrics_list: # only classification metrics ATM
    #                 history[group][metric] += [self.pred_metrics_list[metric](np.asarray(y_list[group].argmax(axis=1)), clas.argmax(axis=1))] # y_list are onehot encoded
    #     del inp
    #     return history, _, clas, dann, rec

    def freeze_layers(self, ae, layers_to_freeze):
        """
        Freezes specified layers in the model.

        ae: Model to freeze layers in.
        layers_to_freeze: List of layers to freeze.
        """
        for layer in layers_to_freeze:
            layer.trainable = False

    def freeze_block(self, ae, strategy):
        if strategy == "all_but_classifier_branch":
            layers_to_freeze = [
                ae.dann_discriminator,
                ae.enc,
                ae.dec,
                ae.ae_output_layer,
            ]
        elif strategy == "all_but_classifier":
            layers_to_freeze = [
                ae.dann_discriminator,
                ae.dec,
                ae.ae_output_layer,
            ]
        elif strategy == "all_but_dann_branch":
            layers_to_freeze = [
                ae.classifier,
                ae.enc,
                ae.dec,
                ae.ae_output_layer,
            ]
        elif strategy == "all_but_dann":
            layers_to_freeze = [ae.classifier, ae.dec, ae.ae_output_layer]
        elif strategy == "all_but_autoencoder":
            layers_to_freeze = [ae.classifier, ae.dann_discriminator]
        elif strategy == "freeze_dann":
            layers_to_freeze = [ae.dann_discriminator]
        elif strategy == "freeze_dec":
            layers_to_freeze = [ae.dec]
        else:
            raise ValueError("Unknown freeze strategy: " + strategy)

        self.freeze_layers(ae, layers_to_freeze)

    def freeze_all(self, ae):
        for l in ae.layers:
            l.trainable = False

    def unfreeze_all(self, ae):
        for l in ae.layers:
            l.trainable = True

    def get_scheme(self):
        if self.training_scheme == "training_scheme_1":
            training_scheme = [
                ("warmup_dann", self.warmup_epoch, False),
                ("full_model", 100, True),
            ]  # This will end with a callback
        if self.training_scheme == "training_scheme_2":
            training_scheme = [
                ("warmup_dann_no_rec", self.warmup_epoch, False),
                ("full_model", 100, True),
            ]  # This will end with a callback
        if self.training_scheme == "training_scheme_3":
            training_scheme = [
                ("warmup_dann", self.warmup_epoch, False),
                ("full_model", 100, True),
                ("classifier_branch", 50, False),
            ]  # This will end with a callback
        if self.training_scheme == "training_scheme_4":
            training_scheme = [
                ("warmup_dann", self.warmup_epoch, False),
                (
                    "permutation_only",
                    100,
                    True,
                ),  # This will end with a callback
                ("classifier_branch", 50, False),
            ]  # This will end with a callback
        if self.training_scheme == "training_scheme_5":
            training_scheme = [
                ("warmup_dann", self.warmup_epoch, False),
                ("full_model", 100, False),
            ]  # This will end with a callback, NO PERMUTATION HERE
        if self.training_scheme == "training_scheme_6":
            training_scheme = [
                (
                    "warmup_dann",
                    self.warmup_epoch,
                    True,
                ),  # Permutating with pseudo labels during warmup
                ("full_model", 100, True),
            ]

        if self.training_scheme == "training_scheme_7":
            training_scheme = [
                (
                    "warmup_dann",
                    self.warmup_epoch,
                    True,
                ),  # Permutating with pseudo labels during warmup
                ("full_model", 100, False),
            ]

        if self.training_scheme == "training_scheme_8":
            training_scheme = [
                (
                    "warmup_dann",
                    self.warmup_epoch,
                    True,
                ),  # Permutating with pseudo labels during warmup
                ("full_model", 100, False),
                ("classifier_branch", 50, False),
            ]  # This will end with a callback]

        if self.training_scheme == "training_scheme_9":
            training_scheme = [
                ("warmup_dann", self.warmup_epoch, False),
                ("full_model", 100, True),
                ("classifier_branch", 50, False),
            ]  # This will end with a callback]

        if self.training_scheme == "training_scheme_10":
            training_scheme = [
                (
                    "warmup_dann",
                    self.warmup_epoch,
                    True,
                ),  # Permutating with pseudo labels during warmup
                ("full_model", 100, False),
                ("classifier_branch", 50, False),
                (
                    "warmup_dann_pseudolabels",
                    self.warmup_epoch,
                    True,
                ),  # Permutating with pseudo labels from the current model state
                ("full_model", 100, False),
                ("classifier_branch", 50, False),
            ]  # This will end with a callback

        if self.training_scheme == "training_scheme_11":
            training_scheme = [
                (
                    "warmup_dann",
                    self.warmup_epoch,
                    True,
                ),  # Permutating with pseudo labels during warmup
                ("full_model", 100, False),
                ("classifier_branch", 50, False),
                (
                    "full_model_pseudolabels",
                    100,
                    True,
                ),  # using permutations on plabels for full training
                ("classifier_branch", 50, False),
            ]  # This will end with a callback

        if self.training_scheme == "training_scheme_12":
            training_scheme = [
                (
                    "permutation_only",
                    self.warmup_epoch,
                    True,
                ),  # Permutating with pseudo labels during warmup
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_13":
            training_scheme = [
                ("full_model", 100, True),
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_14":
            training_scheme = [
                ("full_model", 100, False),
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_15":
            training_scheme = [
                ("warmup_dann_train", self.warmup_epoch, True),
                ("full_model", 100, False),
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_16":
            training_scheme = [
                ("warmup_dann", self.warmup_epoch, True),
                ("full_model", 100, True),
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_17":
            training_scheme = [
                ("no_dann", 100, True),
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_18":
            training_scheme = [
                ("no_dann", 100, False),
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_19":
            training_scheme = [
                (
                    "warmup_dann",
                    self.warmup_epoch,
                    False,
                ),  # Permutating with pseudo labels during warmup
                ("full_model", 100, False),
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_20":
            training_scheme = [
                (
                    "warmup_dann_semisup",
                    self.warmup_epoch,
                    True,
                ),  # Permutating in semisup fashion ie unknown cells reconstruc themselves
                ("full_model", 100, False),
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_21":
            training_scheme = [
                ("warmup_dann", self.warmup_epoch, False),
                ("no_dann", 100, False),
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_22":
            training_scheme = [
                ("permutation_only", self.warmup_epoch, True),
                ("warmup_dann", self.warmup_epoch, True),
                ("full_model", 100, False),
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_23":
            training_scheme = [("full_model", 100, True)]

        if self.training_scheme == "training_scheme_24":
            training_scheme = [
                ("full_model", 100, False),
            ]

        if self.training_scheme == "training_scheme_25":
            training_scheme = [
                ("no_decoder", 100, False),
            ]

        if self.training_scheme == "training_scheme_26":
            training_scheme = [
                (
                    "warmup_dann",
                    self.warmup_epoch,
                    False,
                ),  # Permutating with pseudo labels during warmup
                ("full_model", 100, False),
                ("classifier_branch", 50, False),
                (
                    "full_model_pseudolabels",
                    100,
                    False,
                ),  # using permutations on plabels for full training
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_debug_1":
            training_scheme = [
                ("classifier_branch", 50, False),
            ]

        if self.training_scheme == "training_scheme_debug_2":
            training_scheme = [
                ("encoder_classifier", 50, False),
            ]

        return training_scheme

    def get_losses(self, y_list):
        if self.rec_loss_name == "MSE":
            self.rec_loss_fn = tf.keras.losses.mean_squared_error
        else:
            print(self.rec_loss_name + " loss not supported for rec")

        if self.balance_classes:
            y_integers = np.argmax(np.asarray(y_list["train"]), axis=1)
            class_weights = compute_class_weight(
                class_weight="balanced",
                classes=np.unique(y_integers),
                y=y_integers,
            )

        if self.clas_loss_name == "categorical_crossentropy":
            self.clas_loss_fn = tf.keras.losses.categorical_crossentropy
        elif self.clas_loss_name == "categorical_focal_crossentropy":

            self.clas_loss_fn = tf.keras.losses.CategoricalFocalCrossentropy(
                alpha=class_weights, gamma=3
            )
        else:
            print(self.clas_loss_name + " loss not supported for classif")

        if self.dann_loss_name == "categorical_crossentropy":
            self.dann_loss_fn = tf.keras.losses.categorical_crossentropy
        else:
            print(self.dann_loss_name + " loss not supported for dann")
        return self.rec_loss_fn, self.clas_loss_fn, self.dann_loss_fn

    def print_status_bar(self, iteration, total, loss, metrics=None):
        metrics = " - ".join(
            [
                "{}: {:.4f}".format(m.name, m.result())
                for m in loss + (metrics or [])
            ]
        )

        end = "" if int(iteration) < int(total) else "\n"
        #     print(f"{iteration}/{total} - "+metrics ,end="\r")
        #     print(f"\r{iteration}/{total} - " + metrics, end=end)
        print("\r{}/{} - ".format(iteration, total) + metrics, end=end)

    def get_optimizer(
        self, learning_rate, weight_decay, optimizer_type, momentum=0.9
    ):
        """
        This function takes a  learning rate, weight decay and optionally momentum and returns an optimizer object
        Args:
            learning_rate: The optimizer's learning rate
            weight_decay: The optimizer's weight decay
            optimizer_type: The optimizer's type [adam or sgd]
            momentum: The optimizer's momentum
        Returns:
            an optimizer object
        """
        # TODO Add more optimizers
        print(optimizer_type)
        if optimizer_type == "adam":
            optimizer = tf.keras.optimizers.Adam(
                learning_rate=learning_rate,
                #  decay=weight_decay
            )
        elif optimizer_type == "adamw":
            optimizer = tf.keras.optimizers.AdamW(
                learning_rate=learning_rate, weight_decay=weight_decay
            )
        elif optimizer_type == "rmsprop":
            optimizer = tf.keras.optimizers.RMSprop(
                learning_rate=learning_rate,
                weight_decay=weight_decay,
                momentum=momentum,
            )
        elif optimizer_type == "adafactor":
            optimizer = tf.keras.optimizers.Adafactor(
                learning_rate=learning_rate,
                weight_decay=weight_decay,
            )
        else:
            optimizer = tf.keras.optimizers(
                learning_rate=learning_rate,
                weight_decay=weight_decay,
                momentum=momentum,
            )
        return optimizer


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()

#     # parser.add_argument('--run_file', type = , default = , help ='')
#     # parser.add_argument('--workflow_ID', type = , default = , help ='')
#     parser.add_argument('--dataset_name', type = str, default = 'disco_ajrccm_downsampled', help ='Name of the dataset to use, should indicate a raw h5ad AnnData file')
#     parser.add_argument('--class_key', type = str, default = 'celltype_lv2_V3', help ='Key of the class to classify')
#     parser.add_argument('--batch_key', type = str, default = 'manip', help ='Key of the batches')
#     parser.add_argument('--filter_min_counts', type=str2bool, nargs='?',const=True, default=True, help ='Filters genes with <1 counts')# TODO :remove, we always want to do that
#     parser.add_argument('--normalize_size_factors', type=str2bool, nargs='?',const=True, default=True, help ='Weither to normalize dataset or not')
#     parser.add_argument('--scale_input', type=str2bool, nargs='?',const=False, default=False, help ='Weither to scale input the count values')
#     parser.add_argument('--logtrans_input', type=str2bool, nargs='?',const=True, default=True, help ='Weither to log transform count values')
#     parser.add_argument('--use_hvg', type=int, nargs='?', const=10000, default=None, help = "Number of hvg to use. If no tag, don't use hvg.")
#     # parser.add_argument('--reduce_lr', type = , default = , help ='')
#     # parser.add_argument('--early_stop', type = , default = , help ='')
#     parser.add_argument('--batch_size', type = int, nargs='?', default = 256, help = 'Training batch size')
#     # parser.add_argument('--verbose', type = , default = , help ='')
#     # parser.add_argument('--threads', type = , default = , help ='')
#     parser.add_argument('--mode', type = str, default = 'percentage', help ='Train test split mode to be used by Dataset.train_split')
#     parser.add_argument('--pct_split', type = float,nargs='?', default = 0.9, help ='')
#     parser.add_argument('--obs_key', type = str,nargs='?', default = 'manip', help ='')
#     parser.add_argument('--n_keep', type = int,nargs='?', default = 0, help ='')
#     parser.add_argument('--split_strategy', type = str,nargs='?', default = None, help ='')
#     parser.add_argument('--keep_obs', type = str,nargs='+',default = None, help ='')
#     parser.add_argument('--train_test_random_seed', type = float,nargs='?', default = 0, help ='')
#     parser.add_argument('--obs_subsample', type = str,nargs='?', default = None, help ='')
#     parser.add_argument('--make_fake', type=str2bool, nargs='?',const=False, default=False, help ='')
#     parser.add_argument('--true_celltype', type = str,nargs='?', default = None, help ='')
#     parser.add_argument('--false_celltype', type = str,nargs='?', default = None, help ='')
#     parser.add_argument('--pct_false', type = float,nargs='?', default = 0, help ='')
#     parser.add_argument('--clas_loss_name', type = str,nargs='?', choices = ['categorical_crossentropy'], default = 'categorical_crossentropy' , help ='Loss of the classification branch')
#     parser.add_argument('--dann_loss_name', type = str,nargs='?', choices = ['categorical_crossentropy'], default ='categorical_crossentropy', help ='Loss of the DANN branch')
#     parser.add_argument('--rec_loss_name', type = str,nargs='?', choices = ['MSE'], default ='MSE', help ='Reconstruction loss of the autoencoder')
#     parser.add_argument('--weight_decay', type = float,nargs='?', default = 1e-4, help ='Weight decay applied by th optimizer')
#     parser.add_argument('--learning_rate', type = float,nargs='?', default = 0.001, help ='Starting learning rate for training')
#     parser.add_argument('--optimizer_type', type = str, nargs='?',choices = ['adam','adamw','rmsprop'], default = 'adam' , help ='Name of the optimizer to use')
#     parser.add_argument('--clas_w', type = float,nargs='?', default = 0.1, help ='Wight of the classification loss')
#     parser.add_argument('--dann_w', type = float,nargs='?', default = 0.1, help ='Wight of the DANN loss')
#     parser.add_argument('--rec_w', type = float,nargs='?', default = 0.8, help ='Wight of the reconstruction loss')
#     parser.add_argument('--warmup_epoch', type = float,nargs='?', default = 50, help ='Number of epoch to warmup DANN')
#     parser.add_argument('--ae_hidden_size', type = int,nargs='+', default = [128,64,128], help ='Hidden sizes of the successive ae layers')
#     parser.add_argument('--ae_hidden_dropout', type =float, nargs='?', default = 0, help ='')
#     parser.add_argument('--ae_activation', type = str ,nargs='?', default = 'relu' , help ='')
#     parser.add_argument('--ae_output_activation', type = str,nargs='?', default = 'linear', help ='')
#     parser.add_argument('--ae_init', type = str,nargs='?', default = 'glorot_uniform', help ='')
#     parser.add_argument('--ae_batchnorm', type=str2bool, nargs='?',const=True, default=True , help ='')
#     parser.add_argument('--ae_l1_enc_coef', type = float,nargs='?', default = 0, help ='')
#     parser.add_argument('--ae_l2_enc_coef', type = float,nargs='?', default = 0, help ='')
#     parser.add_argument('--class_hidden_size', type = int,nargs='+', default = [64], help ='Hidden sizes of the successive classification layers')
#     parser.add_argument('--class_hidden_dropout', type =float, nargs='?', default = 0, help ='')
#     parser.add_argument('--class_batchnorm', type=str2bool, nargs='?',const=True, default=True , help ='')
#     parser.add_argument('--class_activation', type = str ,nargs='?', default = 'relu' , help ='')
#     parser.add_argument('--class_output_activation', type = str,nargs='?', default = 'softmax', help ='')
#     parser.add_argument('--dann_hidden_size', type = int,nargs='?', default = [64], help ='')
#     parser.add_argument('--dann_hidden_dropout', type =float, nargs='?', default = 0, help ='')
#     parser.add_argument('--dann_batchnorm', type=str2bool, nargs='?',const=True, default=True , help ='')
#     parser.add_argument('--dann_activation', type = str ,nargs='?', default = 'relu' , help ='')
#     parser.add_argument('--dann_output_activation', type = str,nargs='?', default = 'softmax', help ='')
#     parser.add_argument('--training_scheme', type = str,nargs='?', default = 'training_scheme_1', help ='')
#     parser.add_argument('--log_neptune', type=str2bool, nargs='?',const=True, default=True , help ='')
#     parser.add_argument('--hparam_path', type=str, nargs='?', default=None, help ='')
#     # parser.add_argument('--epochs', type=int, nargs='?', default=100, help ='')

#     run_file = parser.parse_args()
#     # experiment = MakeExperiment(run_file=run_file, working_dir=working_dir)
#     # workflow = Workflow(run_file=run_file, working_dir=working_dir)
#     print("Workflow loaded")
#     if run_file.hparam_path:
#         with open(run_file.hparam_path, 'r') as hparam_json:
#             hparams = json.load(hparam_json)

#     else:
#         hparams = [ # round 1
#             #{"name": "use_hvg", "type": "range", "bounds": [5000, 10000], "log_scale": False},
#             {"name": "clas_w", "type": "range", "bounds": [1e-4, 1e2], "log_scale": False},
#             {"name": "dann_w", "type": "range", "bounds": [1e-4, 1e2], "log_scale": False},
#             {"name": "learning_rate", "type": "range", "bounds": [1e-4, 1e-2], "log_scale": True},
#             {"name": "weight_decay", "type": "range", "bounds": [1e-8, 1e-4], "log_scale": True},
#             {"name": "warmup_epoch", "type": "range", "bounds": [1, 50]},
#             {"name": "dropout", "type": "range", "bounds": [0.0, 0.5]},
#             {"name": "bottleneck", "type": "range", "bounds": [32, 64]},
#             {"name": "layer2", "type": "range", "bounds": [64, 512]},
#             {"name": "layer1", "type": "range", "bounds": [512, 2048]},

#         ]


#     def train_cmd(params):
#         print(params)
#         run_file.clas_w =  params['clas_w']
#         run_file.dann_w = params['dann_w']
#         run_file.rec_w =  1
#         run_file.learning_rate = params['learning_rate']
#         run_file.weight_decay =  params['weight_decay']
#         run_file.warmup_epoch =  params['warmup_epoch']
#         dropout =  params['dropout']
#         layer1 = params['layer1']
#         layer2 =  params['layer2']
#         bottleneck = params['bottleneck']

#         run_file.ae_hidden_size = [layer1, layer2, bottleneck, layer2, layer1]

#         run_file.dann_hidden_dropout, run_file.class_hidden_dropout, run_file.ae_hidden_dropout = dropout, dropout, dropout

#         cmd = ['sbatch', '--wait', '/home/simonp/dca_permuted_workflow/workflow/run_workflow_cmd.sh']
#         for k, v in run_file.__dict__.items():
#             cmd += ([f'--{k}'])
#             if type(v) == list:
#                 cmd += ([str(i) for i in v])
#             else :
#                 cmd += ([str(v)])
#         print(cmd)
#         subprocess.Popen(cmd).wait()
#         with open(working_dir + 'mcc_res.txt', 'r') as my_file:
#             mcc = float(my_file.read())
#         os.remove(working_dir + 'mcc_res.txt')
#         return mcc

#     best_parameters, values, experiment, model = optimize(
#         parameters=hparams,
#         evaluation_function=train_cmd,
#         objective_name='mcc',
#         minimize=False,
#         total_trials=50,
#         random_seed=40,
#     )

# best_parameters, values, experiment, model = optimize(
#     parameters=hparams,
#     evaluation_function=workflow.make_experiment,
#     objective_name='mcc',
#     minimize=False,
#     total_trials=30,
#     random_seed=40,
# )

# print(best_parameters)


# run_workflow_cmd.py --run_file --wd --args --params

# self.workflow = Workflow(run_file=self.run_file, working_dir=self.working_dir)
# mcc = self.workflow.make_experiment(params)
# mcc.write('somewhere')
