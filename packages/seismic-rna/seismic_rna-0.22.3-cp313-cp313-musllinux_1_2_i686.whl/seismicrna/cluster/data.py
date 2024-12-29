from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any

import pandas as pd

from .batch import ClusterMutsBatch
from .io import ClusterBatchIO
from .report import ClusterReport
from ..core.batch import MutsBatch
from ..core.data import (ArrowDataset,
                         Dataset,
                         LoadedDataset,
                         LoadFunction,
                         MergedUnbiasDataset,
                         UnbiasDataset)
from ..core.header import (NUM_CLUSTS_NAME,
                           ClustHeader,
                           list_ks_clusts,
                           validate_ks)
from ..core.join.data import (BATCH_NUM,
                              READ_NUMS,
                              SEG_END5S,
                              SEG_END3S,
                              MUTS,
                              RESPS,
                              JoinMutsDataset)
from ..core.join.report import JoinClusterReport
from ..core.report import KsWrittenF, BestKF, JoinedClustersF
from ..mask.batch import MaskMutsBatch
from ..mask.data import load_mask_dataset


class ClusterDataset(Dataset, ABC):
    """ Dataset for clustered data. """

    @cached_property
    @abstractmethod
    def ks(self) -> list[int]:
        """ Numbers of clusters. """

    @cached_property
    @abstractmethod
    def best_k(self) -> int:
        """ Best number of clusters. """


class ClusterReadDataset(ClusterDataset, LoadedDataset):
    """ Load clustering results. """

    @classmethod
    def get_report_type(cls):
        return ClusterReport

    @classmethod
    def get_batch_type(cls):
        return ClusterBatchIO

    @cached_property
    def ks(self):
        return validate_ks(self.report.get_field(KsWrittenF))

    @cached_property
    def best_k(self):
        return self.report.get_field(BestKF)

    @property
    def pattern(self):
        return None


class ClusterMutsDataset(ClusterDataset, ArrowDataset, UnbiasDataset):
    """ Merge cluster responsibilities with mutation data. """

    @classmethod
    def get_dataset1_load_func(cls):
        return load_mask_dataset

    @classmethod
    def get_dataset2_type(cls):
        return ClusterReadDataset

    @property
    def pattern(self):
        return self.data1.pattern

    @pattern.setter
    def pattern(self, pattern):
        self.data1.pattern = pattern

    @property
    def region(self):
        return self.data1.region

    @property
    def min_mut_gap(self):
        return getattr(self.data1, "min_mut_gap")

    @min_mut_gap.setter
    def min_mut_gap(self, min_mut_gap):
        self.data1.min_mut_gap = min_mut_gap

    @property
    def quick_unbias(self):
        return getattr(self.data1, "quick_unbias")

    @property
    def quick_unbias_thresh(self):
        return getattr(self.data1, "quick_unbias_thresh")

    @property
    def ks(self):
        return getattr(self.data2, "ks")

    @property
    def best_k(self):
        return getattr(self.data2, "best_k")

    def _integrate(self, batch1: MaskMutsBatch, batch2: ClusterBatchIO):
        return ClusterMutsBatch(batch=batch1.batch,
                                region=batch1.region,
                                seg_end5s=batch1.seg_end5s,
                                seg_end3s=batch1.seg_end3s,
                                muts=batch1.muts,
                                resps=batch2.resps,
                                sanitize=False)


class JoinClusterMutsDataset(ClusterDataset,
                             JoinMutsDataset,
                             MergedUnbiasDataset):

    @classmethod
    def get_report_type(cls):
        return JoinClusterReport

    @classmethod
    def get_dataset_load_func(cls):
        return load_cluster_dataset

    @classmethod
    def get_batch_type(cls):
        return ClusterMutsBatch

    @classmethod
    def name_batch_attrs(cls):
        return [BATCH_NUM, READ_NUMS, SEG_END5S, SEG_END3S, MUTS, RESPS]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._joined_clusts = self.report.get_field(JoinedClustersF)
        if self._joined_clusts is None:
            raise TypeError(f"{self} requires clusters, but got None")
        if sorted(self._joined_clusts) != sorted(self.regs):
            raise ValueError(f"{self} expected clusters for {self.regs}, "
                             f"but got {self._joined_clusts}")

    @cached_property
    def ks(self):
        return self._get_common_attr("ks")

    @cached_property
    def best_k(self):
        return self._get_common_attr("best_k")

    @cached_property
    def clusts(self):
        """ Index of k and cluster numbers. """
        return list_ks_clusts(self.ks)

    def _reg_cols(self, reg: str):
        """ Get the columns for a region's responsibilities. """
        clusts = self._joined_clusts[reg]
        return pd.MultiIndex.from_tuples(
            [(k, clusts[k][clust]) for k, clust in self.clusts],
            names=ClustHeader.level_names()
        )

    def _reg_resps(self, reg: str, resps: pd.DataFrame):
        """ Get the cluster responsibilities for a region. """
        # Reorder the columns.
        reordered = resps.loc[:, self._reg_cols(reg)]
        # Rename the columns by increasing k and cluster.
        reordered.columns = self.clusts
        return reordered

    def _get_batch_attrs(self, batch: MutsBatch, reg: str):
        attrs = super()._get_batch_attrs(batch, reg)
        # Adjust the cluster labels based on the region.
        attrs[RESPS] = self._reg_resps(reg, attrs[RESPS])
        return attrs

    def _join_attrs(self, attrs: dict[str, Any], add_attrs: dict[str, Any]):
        super()._join_attrs(attrs, add_attrs)
        # Join the cluster memberships.
        attrs[RESPS] = attrs[RESPS].add(add_attrs[RESPS], fill_value=0.)

    def _finalize_attrs(self, attrs: dict[str, Any]):
        # Ensure that cluster memberships for each read sum to 1.
        attrs[RESPS] /= attrs[RESPS].T.groupby(level=NUM_CLUSTS_NAME).sum().T
        # Fill any missing values with 0 and sort the read numbers.
        attrs[RESPS] = attrs[RESPS].fillna(0.).sort_index()
        # Delete read_nums (which is the index of resps).
        attrs.pop(READ_NUMS)


load_cluster_dataset = LoadFunction(ClusterMutsDataset, JoinClusterMutsDataset)

########################################################################
#                                                                      #
# © Copyright 2024, the Rouskin Lab.                                   #
#                                                                      #
# This file is part of SEISMIC-RNA.                                    #
#                                                                      #
# SEISMIC-RNA is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation; either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# SEISMIC-RNA is distributed in the hope that it will be useful, but   #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANT- #
# ABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General     #
# Public License for more details.                                     #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with SEISMIC-RNA; if not, see <https://www.gnu.org/licenses>.  #
#                                                                      #
########################################################################
