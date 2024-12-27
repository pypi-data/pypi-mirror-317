import os

import pandas as pd
import pytest

from hmmCDR.bed_parser import bed_parser
from hmmCDR.calculate_matrices import calculate_matrices
from hmmCDR.hmmCDR import hmmCDR


class TestHMMCDR:
    @pytest.fixture
    def test_data(self):
        """Fixture to set up test data and parser"""
        test_data_dir = os.path.join("tests", "data")

        parser = bed_parser(
            mod_code="m",
            bedgraph=False,
            min_valid_cov=10,
            sat_type=["active_hor"],
            pre_subset_censat=False,
        )

        bedmethyl_test = os.path.join(test_data_dir, "bedmethyl_test.bed")
        censat_test = os.path.join(test_data_dir, "censat_test.bed")

        return parser.process_files(
            bedmethyl_path=bedmethyl_test,
            censat_path=censat_test,
        )

    @pytest.fixture
    def matrix_calculator(self):
        """Fixture for matrix calculator"""
        return calculate_matrices(
            window_size=1190,
            step_size=1190,
            min_prior_size=8330,
            enrichment=False,
            percentile_emissions=False,
            w=0.0,
            x=33.0,
            y=66.0,
            z=100.0,
            output_label="CDR",
        )

    @pytest.fixture
    def hmmcdr(self):
        """Fixture for matrix calculator"""
        return hmmCDR(
            n_iter=1,
            tol=10,
            merge_distance=200000,
            min_cdr_size=3000,
            min_cdr_score=95,
            min_low_conf_size=1,
            min_low_conf_score=50,
            main_color="50,50,255",
            low_conf_color="100,150,200",
            output_label="CDR",
        )

    def test_run_hmm(self, test_data, matrix_calculator, hmmcdr):
        """Test making matrices"""
        (
            priors_chrom_dict,
            windowmean_chrom_dict,
            labelled_methylation_chrom_dict,
            emission_matrix_chrom_dict,
            transition_matrix_chrom_dict,
        ) = matrix_calculator.priors_all_chromosomes(
            methylation_chrom_dict=test_data[0],
            regions_chrom_dict=test_data[1],
            prior_percentile=False,
            prior_threshold=20,
        )

        (hmm_results_chrom_dict, hmm_scores_chrom_dict) = hmmcdr.hmm_all_chromosomes(
            labelled_methylation_chrom_dict=labelled_methylation_chrom_dict,
            emission_matrix_chrom_dict=emission_matrix_chrom_dict,
            transition_matrix_chrom_dict=transition_matrix_chrom_dict,
        )

        # Changed from .values to proper dictionary access
        assert isinstance(hmm_results_chrom_dict, dict)
        assert isinstance(hmm_scores_chrom_dict, dict)
        assert len(hmm_results_chrom_dict) == 1
        assert len(hmm_scores_chrom_dict) == 1

        # Add more specific assertions about the matrices
        for chrom in hmm_results_chrom_dict:
            assert isinstance(hmm_results_chrom_dict[chrom], pd.DataFrame)
            # Add assertions about matrix shape or content if known

        for chrom in hmm_scores_chrom_dict:
            assert isinstance(hmm_scores_chrom_dict[chrom], pd.DataFrame)
            # Add assertions about matrix shape or content if known
