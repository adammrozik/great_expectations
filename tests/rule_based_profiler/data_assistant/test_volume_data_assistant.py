import os
from typing import Any, Callable, Dict, List, Optional, Tuple, cast
from unittest import mock

import altair as alt
import nbconvert
import nbformat
import pytest
from freezegun import freeze_time

from great_expectations import DataContext
from great_expectations.core import ExpectationConfiguration, ExpectationSuite
from great_expectations.core.batch import Batch
from great_expectations.core.usage_statistics.events import UsageStatsEvents
from great_expectations.execution_engine.execution_engine import MetricDomainTypes
from great_expectations.rule_based_profiler.config import RuleBasedProfilerConfig
from great_expectations.rule_based_profiler.data_assistant import (
    DataAssistant,
    VolumeDataAssistant,
)
from great_expectations.rule_based_profiler.helpers.cardinality_checker import (
    CardinalityLimitMode,
)
from great_expectations.rule_based_profiler.helpers.util import (
    get_validator_with_expectation_suite,
)
from great_expectations.rule_based_profiler.types import (
    FULLY_QUALIFIED_PARAMETER_NAME_ATTRIBUTED_VALUE_KEY,
    INFERRED_SEMANTIC_TYPE_KEY,
    Domain,
    ParameterNode,
    SemanticDomainTypes,
)
from great_expectations.rule_based_profiler.types.altair import AltairDataTypes
from great_expectations.rule_based_profiler.types.data_assistant_result import (
    DataAssistantResult,
    VolumeDataAssistantResult,
)
from great_expectations.rule_based_profiler.types.data_assistant_result.plot_result import (
    PlotResult,
)
from great_expectations.util import deep_filter_properties_iterable
from great_expectations.validator.validator import Validator
from tests.render.test_util import load_notebook_from_path
from tests.test_utils import find_strings_in_nested_obj


@pytest.fixture
def quentin_expected_metrics_by_domain() -> Dict[Domain, Dict[str, Any]]:
    expected_metrics_by_domain: Dict[Domain, Dict[str, Any]] = {
        Domain(domain_type=MetricDomainTypes.TABLE, rule_name="table_rule",): {
            "$parameter.table_row_count": {
                "value": [
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                    10000,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [10000],
                    "562969eaef9c843cb4531aecbc13bbcb": [10000],
                    "569a4a80bf434c888593c651dbf2f157": [10000],
                    "f6c389dcef63c1f214c30f66b66945c0": [10000],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [10000],
                    "e20c38f98b9830a40b851939ca7189d4": [10000],
                    "f2e4d3da6556638b55df8ce509b094c2": [10000],
                    "44c1b1947c9049e7db62c5320dde4c63": [10000],
                    "47157bdaf05a7992473cd699cabaef74": [10000],
                    "08085632aff9ce4cebbb8023049e1aec": [10000],
                    "bb54e4fa3906387218be10cff631a7c2": [10000],
                    "58ce3b40d384eacd9bad7d916eb8f705": [10000],
                    "0327cfb13205ec8512e1c28e438ab43b": [10000],
                    "0808e185a52825d22356de2fe00a8f5f": [10000],
                    "90bb41c1fbd7c71c05dbc8695320af71": [10000],
                    "6c7e43619fe5e6963e8159cc84a28321": [10000],
                    "976b121b46db6967854b9c1a6628396b": [10000],
                    "9e58d3c72c7006b6f5800b623fbc9818": [10000],
                    "ce5f02ac408b7b5c500050190f549736": [10000],
                    "bb81456ec79522bf02f34b02762f95e0": [10000],
                    "b20800a7faafd2808d6c888577a2ba1d": [10000],
                    "33d910f95326c0c7dfe7536d1cfeba51": [10000],
                    "61e4931d87cb627df2a19b8bc5819b7b": [10000],
                    "3692b23382fd4734215465251290c65b": [10000],
                    "eff8910cddcdff62e4741243099240d5": [10000],
                    "f67d274202366f6b976414c950ca14bd": [10000],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [10000],
                    "73612fdabd337d5a8279acc30ce22d00": [10000],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [10000],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [10000],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [10000],
                    "940576153c66af14a949fd19aedd5f5b": [10000],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [10000],
                    "57c04d62ada3a102248b48f34c755159": [10000],
                    "816b147dcf3305839f723a131b9ad6af": [10000],
                    "84000630d1b69a0fe870c94fb26a32bc": [10000],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "table.row_count",
                        "domain_kwargs": {},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "pickup_datetime",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "pickup_datetime": SemanticDomainTypes.TEXT,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    9979,
                    9965,
                    9974,
                    9979,
                    9976,
                    9980,
                    9983,
                    9974,
                    9974,
                    9968,
                    9972,
                    9977,
                    9973,
                    9977,
                    9976,
                    9984,
                    9977,
                    9970,
                    9977,
                    9975,
                    9976,
                    9981,
                    9973,
                    9976,
                    9982,
                    9981,
                    9945,
                    9955,
                    9941,
                    9953,
                    9973,
                    9955,
                    9962,
                    9970,
                    9977,
                    9969,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [9979],
                    "562969eaef9c843cb4531aecbc13bbcb": [9965],
                    "569a4a80bf434c888593c651dbf2f157": [9974],
                    "f6c389dcef63c1f214c30f66b66945c0": [9979],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [9976],
                    "e20c38f98b9830a40b851939ca7189d4": [9980],
                    "f2e4d3da6556638b55df8ce509b094c2": [9983],
                    "44c1b1947c9049e7db62c5320dde4c63": [9974],
                    "47157bdaf05a7992473cd699cabaef74": [9974],
                    "08085632aff9ce4cebbb8023049e1aec": [9968],
                    "bb54e4fa3906387218be10cff631a7c2": [9972],
                    "58ce3b40d384eacd9bad7d916eb8f705": [9977],
                    "0327cfb13205ec8512e1c28e438ab43b": [9973],
                    "0808e185a52825d22356de2fe00a8f5f": [9977],
                    "90bb41c1fbd7c71c05dbc8695320af71": [9976],
                    "6c7e43619fe5e6963e8159cc84a28321": [9984],
                    "976b121b46db6967854b9c1a6628396b": [9977],
                    "9e58d3c72c7006b6f5800b623fbc9818": [9970],
                    "ce5f02ac408b7b5c500050190f549736": [9977],
                    "bb81456ec79522bf02f34b02762f95e0": [9975],
                    "b20800a7faafd2808d6c888577a2ba1d": [9976],
                    "33d910f95326c0c7dfe7536d1cfeba51": [9981],
                    "61e4931d87cb627df2a19b8bc5819b7b": [9973],
                    "3692b23382fd4734215465251290c65b": [9976],
                    "eff8910cddcdff62e4741243099240d5": [9982],
                    "f67d274202366f6b976414c950ca14bd": [9981],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [9945],
                    "73612fdabd337d5a8279acc30ce22d00": [9955],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [9941],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [9953],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [9973],
                    "940576153c66af14a949fd19aedd5f5b": [9955],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [9962],
                    "57c04d62ada3a102248b48f34c755159": [9970],
                    "816b147dcf3305839f723a131b9ad6af": [9977],
                    "84000630d1b69a0fe870c94fb26a32bc": [9969],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "pickup_datetime"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "dropoff_datetime",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "dropoff_datetime": SemanticDomainTypes.TEXT,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    9979,
                    9977,
                    9972,
                    9979,
                    9984,
                    9977,
                    9985,
                    9977,
                    9971,
                    9976,
                    9975,
                    9972,
                    9972,
                    9967,
                    9973,
                    9976,
                    9986,
                    9982,
                    9982,
                    9978,
                    9974,
                    9984,
                    9977,
                    9975,
                    9975,
                    9973,
                    9968,
                    9964,
                    9939,
                    9965,
                    9966,
                    9978,
                    9970,
                    9967,
                    9976,
                    9971,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [9979],
                    "562969eaef9c843cb4531aecbc13bbcb": [9977],
                    "569a4a80bf434c888593c651dbf2f157": [9972],
                    "f6c389dcef63c1f214c30f66b66945c0": [9979],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [9984],
                    "e20c38f98b9830a40b851939ca7189d4": [9977],
                    "f2e4d3da6556638b55df8ce509b094c2": [9985],
                    "44c1b1947c9049e7db62c5320dde4c63": [9977],
                    "47157bdaf05a7992473cd699cabaef74": [9971],
                    "08085632aff9ce4cebbb8023049e1aec": [9976],
                    "bb54e4fa3906387218be10cff631a7c2": [9975],
                    "58ce3b40d384eacd9bad7d916eb8f705": [9972],
                    "0327cfb13205ec8512e1c28e438ab43b": [9972],
                    "0808e185a52825d22356de2fe00a8f5f": [9967],
                    "90bb41c1fbd7c71c05dbc8695320af71": [9973],
                    "6c7e43619fe5e6963e8159cc84a28321": [9976],
                    "976b121b46db6967854b9c1a6628396b": [9986],
                    "9e58d3c72c7006b6f5800b623fbc9818": [9982],
                    "ce5f02ac408b7b5c500050190f549736": [9982],
                    "bb81456ec79522bf02f34b02762f95e0": [9978],
                    "b20800a7faafd2808d6c888577a2ba1d": [9974],
                    "33d910f95326c0c7dfe7536d1cfeba51": [9984],
                    "61e4931d87cb627df2a19b8bc5819b7b": [9977],
                    "3692b23382fd4734215465251290c65b": [9975],
                    "eff8910cddcdff62e4741243099240d5": [9975],
                    "f67d274202366f6b976414c950ca14bd": [9973],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [9968],
                    "73612fdabd337d5a8279acc30ce22d00": [9964],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [9939],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [9965],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [9966],
                    "940576153c66af14a949fd19aedd5f5b": [9978],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [9970],
                    "57c04d62ada3a102248b48f34c755159": [9967],
                    "816b147dcf3305839f723a131b9ad6af": [9976],
                    "84000630d1b69a0fe870c94fb26a32bc": [9971],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "dropoff_datetime"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "passenger_count",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "passenger_count": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    8,
                    7,
                    7,
                    7,
                    7,
                    8,
                    6,
                    7,
                    7,
                    7,
                    7,
                    8,
                    7,
                    7,
                    7,
                    7,
                    7,
                    8,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                    7,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [7],
                    "562969eaef9c843cb4531aecbc13bbcb": [7],
                    "569a4a80bf434c888593c651dbf2f157": [7],
                    "f6c389dcef63c1f214c30f66b66945c0": [7],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [7],
                    "e20c38f98b9830a40b851939ca7189d4": [7],
                    "f2e4d3da6556638b55df8ce509b094c2": [8],
                    "44c1b1947c9049e7db62c5320dde4c63": [7],
                    "47157bdaf05a7992473cd699cabaef74": [7],
                    "08085632aff9ce4cebbb8023049e1aec": [7],
                    "bb54e4fa3906387218be10cff631a7c2": [7],
                    "58ce3b40d384eacd9bad7d916eb8f705": [8],
                    "0327cfb13205ec8512e1c28e438ab43b": [6],
                    "0808e185a52825d22356de2fe00a8f5f": [7],
                    "90bb41c1fbd7c71c05dbc8695320af71": [7],
                    "6c7e43619fe5e6963e8159cc84a28321": [7],
                    "976b121b46db6967854b9c1a6628396b": [7],
                    "9e58d3c72c7006b6f5800b623fbc9818": [8],
                    "ce5f02ac408b7b5c500050190f549736": [7],
                    "bb81456ec79522bf02f34b02762f95e0": [7],
                    "b20800a7faafd2808d6c888577a2ba1d": [7],
                    "33d910f95326c0c7dfe7536d1cfeba51": [7],
                    "61e4931d87cb627df2a19b8bc5819b7b": [7],
                    "3692b23382fd4734215465251290c65b": [8],
                    "eff8910cddcdff62e4741243099240d5": [7],
                    "f67d274202366f6b976414c950ca14bd": [7],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [7],
                    "73612fdabd337d5a8279acc30ce22d00": [7],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [7],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [7],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [7],
                    "940576153c66af14a949fd19aedd5f5b": [7],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [7],
                    "57c04d62ada3a102248b48f34c755159": [7],
                    "816b147dcf3305839f723a131b9ad6af": [7],
                    "84000630d1b69a0fe870c94fb26a32bc": [7],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "passenger_count"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "trip_distance",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "trip_distance": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    1157,
                    1141,
                    1165,
                    1176,
                    1202,
                    1202,
                    1227,
                    1252,
                    1236,
                    1192,
                    1212,
                    1206,
                    1184,
                    1200,
                    1225,
                    1240,
                    1222,
                    1266,
                    1299,
                    1293,
                    1310,
                    1279,
                    1230,
                    1249,
                    1228,
                    1190,
                    1253,
                    1273,
                    1560,
                    1430,
                    1371,
                    1319,
                    1207,
                    1188,
                    1204,
                    1196,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [1157],
                    "562969eaef9c843cb4531aecbc13bbcb": [1141],
                    "569a4a80bf434c888593c651dbf2f157": [1165],
                    "f6c389dcef63c1f214c30f66b66945c0": [1176],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [1202],
                    "e20c38f98b9830a40b851939ca7189d4": [1202],
                    "f2e4d3da6556638b55df8ce509b094c2": [1227],
                    "44c1b1947c9049e7db62c5320dde4c63": [1252],
                    "47157bdaf05a7992473cd699cabaef74": [1236],
                    "08085632aff9ce4cebbb8023049e1aec": [1192],
                    "bb54e4fa3906387218be10cff631a7c2": [1212],
                    "58ce3b40d384eacd9bad7d916eb8f705": [1206],
                    "0327cfb13205ec8512e1c28e438ab43b": [1184],
                    "0808e185a52825d22356de2fe00a8f5f": [1200],
                    "90bb41c1fbd7c71c05dbc8695320af71": [1225],
                    "6c7e43619fe5e6963e8159cc84a28321": [1240],
                    "976b121b46db6967854b9c1a6628396b": [1222],
                    "9e58d3c72c7006b6f5800b623fbc9818": [1266],
                    "ce5f02ac408b7b5c500050190f549736": [1299],
                    "bb81456ec79522bf02f34b02762f95e0": [1293],
                    "b20800a7faafd2808d6c888577a2ba1d": [1310],
                    "33d910f95326c0c7dfe7536d1cfeba51": [1279],
                    "61e4931d87cb627df2a19b8bc5819b7b": [1230],
                    "3692b23382fd4734215465251290c65b": [1249],
                    "eff8910cddcdff62e4741243099240d5": [1228],
                    "f67d274202366f6b976414c950ca14bd": [1190],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [1253],
                    "73612fdabd337d5a8279acc30ce22d00": [1273],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [1560],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [1430],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [1371],
                    "940576153c66af14a949fd19aedd5f5b": [1319],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [1207],
                    "57c04d62ada3a102248b48f34c755159": [1188],
                    "816b147dcf3305839f723a131b9ad6af": [1204],
                    "84000630d1b69a0fe870c94fb26a32bc": [1196],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "trip_distance"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "store_and_fwd_flag",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "store_and_fwd_flag": SemanticDomainTypes.TEXT,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                    2,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [2],
                    "562969eaef9c843cb4531aecbc13bbcb": [2],
                    "569a4a80bf434c888593c651dbf2f157": [2],
                    "f6c389dcef63c1f214c30f66b66945c0": [2],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [2],
                    "e20c38f98b9830a40b851939ca7189d4": [2],
                    "f2e4d3da6556638b55df8ce509b094c2": [2],
                    "44c1b1947c9049e7db62c5320dde4c63": [2],
                    "47157bdaf05a7992473cd699cabaef74": [2],
                    "08085632aff9ce4cebbb8023049e1aec": [2],
                    "bb54e4fa3906387218be10cff631a7c2": [2],
                    "58ce3b40d384eacd9bad7d916eb8f705": [2],
                    "0327cfb13205ec8512e1c28e438ab43b": [2],
                    "0808e185a52825d22356de2fe00a8f5f": [2],
                    "90bb41c1fbd7c71c05dbc8695320af71": [2],
                    "6c7e43619fe5e6963e8159cc84a28321": [2],
                    "976b121b46db6967854b9c1a6628396b": [2],
                    "9e58d3c72c7006b6f5800b623fbc9818": [2],
                    "ce5f02ac408b7b5c500050190f549736": [2],
                    "bb81456ec79522bf02f34b02762f95e0": [2],
                    "b20800a7faafd2808d6c888577a2ba1d": [2],
                    "33d910f95326c0c7dfe7536d1cfeba51": [2],
                    "61e4931d87cb627df2a19b8bc5819b7b": [2],
                    "3692b23382fd4734215465251290c65b": [2],
                    "eff8910cddcdff62e4741243099240d5": [2],
                    "f67d274202366f6b976414c950ca14bd": [2],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [2],
                    "73612fdabd337d5a8279acc30ce22d00": [2],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [2],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [2],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [2],
                    "940576153c66af14a949fd19aedd5f5b": [2],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [2],
                    "57c04d62ada3a102248b48f34c755159": [2],
                    "816b147dcf3305839f723a131b9ad6af": [2],
                    "84000630d1b69a0fe870c94fb26a32bc": [2],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "store_and_fwd_flag"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "payment_type",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "payment_type": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                    4,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [4],
                    "562969eaef9c843cb4531aecbc13bbcb": [4],
                    "569a4a80bf434c888593c651dbf2f157": [4],
                    "f6c389dcef63c1f214c30f66b66945c0": [4],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [4],
                    "e20c38f98b9830a40b851939ca7189d4": [4],
                    "f2e4d3da6556638b55df8ce509b094c2": [4],
                    "44c1b1947c9049e7db62c5320dde4c63": [4],
                    "47157bdaf05a7992473cd699cabaef74": [4],
                    "08085632aff9ce4cebbb8023049e1aec": [4],
                    "bb54e4fa3906387218be10cff631a7c2": [4],
                    "58ce3b40d384eacd9bad7d916eb8f705": [4],
                    "0327cfb13205ec8512e1c28e438ab43b": [4],
                    "0808e185a52825d22356de2fe00a8f5f": [4],
                    "90bb41c1fbd7c71c05dbc8695320af71": [4],
                    "6c7e43619fe5e6963e8159cc84a28321": [4],
                    "976b121b46db6967854b9c1a6628396b": [4],
                    "9e58d3c72c7006b6f5800b623fbc9818": [4],
                    "ce5f02ac408b7b5c500050190f549736": [4],
                    "bb81456ec79522bf02f34b02762f95e0": [4],
                    "b20800a7faafd2808d6c888577a2ba1d": [4],
                    "33d910f95326c0c7dfe7536d1cfeba51": [4],
                    "61e4931d87cb627df2a19b8bc5819b7b": [4],
                    "3692b23382fd4734215465251290c65b": [4],
                    "eff8910cddcdff62e4741243099240d5": [4],
                    "f67d274202366f6b976414c950ca14bd": [4],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [4],
                    "73612fdabd337d5a8279acc30ce22d00": [4],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [4],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [4],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [4],
                    "940576153c66af14a949fd19aedd5f5b": [4],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [4],
                    "57c04d62ada3a102248b48f34c755159": [4],
                    "816b147dcf3305839f723a131b9ad6af": [4],
                    "84000630d1b69a0fe870c94fb26a32bc": [4],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "payment_type"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "fare_amount",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "fare_amount": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    153,
                    148,
                    161,
                    156,
                    153,
                    161,
                    168,
                    176,
                    169,
                    170,
                    199,
                    184,
                    187,
                    201,
                    202,
                    178,
                    170,
                    184,
                    238,
                    253,
                    248,
                    246,
                    246,
                    252,
                    259,
                    267,
                    296,
                    797,
                    1500,
                    813,
                    575,
                    575,
                    571,
                    568,
                    552,
                    588,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [153],
                    "562969eaef9c843cb4531aecbc13bbcb": [148],
                    "569a4a80bf434c888593c651dbf2f157": [161],
                    "f6c389dcef63c1f214c30f66b66945c0": [156],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [153],
                    "e20c38f98b9830a40b851939ca7189d4": [161],
                    "f2e4d3da6556638b55df8ce509b094c2": [168],
                    "44c1b1947c9049e7db62c5320dde4c63": [176],
                    "47157bdaf05a7992473cd699cabaef74": [169],
                    "08085632aff9ce4cebbb8023049e1aec": [170],
                    "bb54e4fa3906387218be10cff631a7c2": [199],
                    "58ce3b40d384eacd9bad7d916eb8f705": [184],
                    "0327cfb13205ec8512e1c28e438ab43b": [187],
                    "0808e185a52825d22356de2fe00a8f5f": [201],
                    "90bb41c1fbd7c71c05dbc8695320af71": [202],
                    "6c7e43619fe5e6963e8159cc84a28321": [178],
                    "976b121b46db6967854b9c1a6628396b": [170],
                    "9e58d3c72c7006b6f5800b623fbc9818": [184],
                    "ce5f02ac408b7b5c500050190f549736": [238],
                    "bb81456ec79522bf02f34b02762f95e0": [253],
                    "b20800a7faafd2808d6c888577a2ba1d": [248],
                    "33d910f95326c0c7dfe7536d1cfeba51": [246],
                    "61e4931d87cb627df2a19b8bc5819b7b": [246],
                    "3692b23382fd4734215465251290c65b": [252],
                    "eff8910cddcdff62e4741243099240d5": [259],
                    "f67d274202366f6b976414c950ca14bd": [267],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [296],
                    "73612fdabd337d5a8279acc30ce22d00": [797],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [1500],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [813],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [575],
                    "940576153c66af14a949fd19aedd5f5b": [575],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [571],
                    "57c04d62ada3a102248b48f34c755159": [568],
                    "816b147dcf3305839f723a131b9ad6af": [552],
                    "84000630d1b69a0fe870c94fb26a32bc": [588],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "fare_amount"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "extra",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "extra": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    6,
                    6,
                    6,
                    5,
                    6,
                    4,
                    5,
                    7,
                    6,
                    7,
                    6,
                    6,
                    8,
                    10,
                    12,
                    12,
                    10,
                    11,
                    12,
                    14,
                    13,
                    16,
                    12,
                    13,
                    12,
                    15,
                    14,
                    10,
                    11,
                    10,
                    13,
                    12,
                    11,
                    10,
                    11,
                    10,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [6],
                    "562969eaef9c843cb4531aecbc13bbcb": [6],
                    "569a4a80bf434c888593c651dbf2f157": [6],
                    "f6c389dcef63c1f214c30f66b66945c0": [5],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [6],
                    "e20c38f98b9830a40b851939ca7189d4": [4],
                    "f2e4d3da6556638b55df8ce509b094c2": [5],
                    "44c1b1947c9049e7db62c5320dde4c63": [7],
                    "47157bdaf05a7992473cd699cabaef74": [6],
                    "08085632aff9ce4cebbb8023049e1aec": [7],
                    "bb54e4fa3906387218be10cff631a7c2": [6],
                    "58ce3b40d384eacd9bad7d916eb8f705": [6],
                    "0327cfb13205ec8512e1c28e438ab43b": [8],
                    "0808e185a52825d22356de2fe00a8f5f": [10],
                    "90bb41c1fbd7c71c05dbc8695320af71": [12],
                    "6c7e43619fe5e6963e8159cc84a28321": [12],
                    "976b121b46db6967854b9c1a6628396b": [10],
                    "9e58d3c72c7006b6f5800b623fbc9818": [11],
                    "ce5f02ac408b7b5c500050190f549736": [12],
                    "bb81456ec79522bf02f34b02762f95e0": [14],
                    "b20800a7faafd2808d6c888577a2ba1d": [13],
                    "33d910f95326c0c7dfe7536d1cfeba51": [16],
                    "61e4931d87cb627df2a19b8bc5819b7b": [12],
                    "3692b23382fd4734215465251290c65b": [13],
                    "eff8910cddcdff62e4741243099240d5": [12],
                    "f67d274202366f6b976414c950ca14bd": [15],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [14],
                    "73612fdabd337d5a8279acc30ce22d00": [10],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [11],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [10],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [13],
                    "940576153c66af14a949fd19aedd5f5b": [12],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [11],
                    "57c04d62ada3a102248b48f34c755159": [10],
                    "816b147dcf3305839f723a131b9ad6af": [11],
                    "84000630d1b69a0fe870c94fb26a32bc": [10],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "extra"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "mta_tax",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "mta_tax": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    4,
                    3,
                    3,
                    3,
                    3,
                    4,
                    3,
                    3,
                    3,
                    3,
                    4,
                    4,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    4,
                    4,
                    3,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [3],
                    "562969eaef9c843cb4531aecbc13bbcb": [3],
                    "569a4a80bf434c888593c651dbf2f157": [3],
                    "f6c389dcef63c1f214c30f66b66945c0": [3],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [3],
                    "e20c38f98b9830a40b851939ca7189d4": [3],
                    "f2e4d3da6556638b55df8ce509b094c2": [3],
                    "44c1b1947c9049e7db62c5320dde4c63": [3],
                    "47157bdaf05a7992473cd699cabaef74": [3],
                    "08085632aff9ce4cebbb8023049e1aec": [3],
                    "bb54e4fa3906387218be10cff631a7c2": [3],
                    "58ce3b40d384eacd9bad7d916eb8f705": [3],
                    "0327cfb13205ec8512e1c28e438ab43b": [4],
                    "0808e185a52825d22356de2fe00a8f5f": [3],
                    "90bb41c1fbd7c71c05dbc8695320af71": [3],
                    "6c7e43619fe5e6963e8159cc84a28321": [3],
                    "976b121b46db6967854b9c1a6628396b": [3],
                    "9e58d3c72c7006b6f5800b623fbc9818": [4],
                    "ce5f02ac408b7b5c500050190f549736": [3],
                    "bb81456ec79522bf02f34b02762f95e0": [3],
                    "b20800a7faafd2808d6c888577a2ba1d": [3],
                    "33d910f95326c0c7dfe7536d1cfeba51": [3],
                    "61e4931d87cb627df2a19b8bc5819b7b": [4],
                    "3692b23382fd4734215465251290c65b": [4],
                    "eff8910cddcdff62e4741243099240d5": [3],
                    "f67d274202366f6b976414c950ca14bd": [3],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [3],
                    "73612fdabd337d5a8279acc30ce22d00": [3],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [3],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [3],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [3],
                    "940576153c66af14a949fd19aedd5f5b": [3],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [3],
                    "57c04d62ada3a102248b48f34c755159": [4],
                    "816b147dcf3305839f723a131b9ad6af": [4],
                    "84000630d1b69a0fe870c94fb26a32bc": [3],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "mta_tax"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "tip_amount",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "tip_amount": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    532,
                    530,
                    539,
                    573,
                    574,
                    559,
                    557,
                    567,
                    576,
                    555,
                    600,
                    601,
                    535,
                    597,
                    601,
                    596,
                    612,
                    606,
                    579,
                    595,
                    608,
                    591,
                    599,
                    606,
                    572,
                    576,
                    560,
                    469,
                    466,
                    558,
                    539,
                    530,
                    503,
                    505,
                    515,
                    522,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [532],
                    "562969eaef9c843cb4531aecbc13bbcb": [530],
                    "569a4a80bf434c888593c651dbf2f157": [539],
                    "f6c389dcef63c1f214c30f66b66945c0": [573],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [574],
                    "e20c38f98b9830a40b851939ca7189d4": [559],
                    "f2e4d3da6556638b55df8ce509b094c2": [557],
                    "44c1b1947c9049e7db62c5320dde4c63": [567],
                    "47157bdaf05a7992473cd699cabaef74": [576],
                    "08085632aff9ce4cebbb8023049e1aec": [555],
                    "bb54e4fa3906387218be10cff631a7c2": [600],
                    "58ce3b40d384eacd9bad7d916eb8f705": [601],
                    "0327cfb13205ec8512e1c28e438ab43b": [535],
                    "0808e185a52825d22356de2fe00a8f5f": [597],
                    "90bb41c1fbd7c71c05dbc8695320af71": [601],
                    "6c7e43619fe5e6963e8159cc84a28321": [596],
                    "976b121b46db6967854b9c1a6628396b": [612],
                    "9e58d3c72c7006b6f5800b623fbc9818": [606],
                    "ce5f02ac408b7b5c500050190f549736": [579],
                    "bb81456ec79522bf02f34b02762f95e0": [595],
                    "b20800a7faafd2808d6c888577a2ba1d": [608],
                    "33d910f95326c0c7dfe7536d1cfeba51": [591],
                    "61e4931d87cb627df2a19b8bc5819b7b": [599],
                    "3692b23382fd4734215465251290c65b": [606],
                    "eff8910cddcdff62e4741243099240d5": [572],
                    "f67d274202366f6b976414c950ca14bd": [576],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [560],
                    "73612fdabd337d5a8279acc30ce22d00": [469],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [466],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [558],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [539],
                    "940576153c66af14a949fd19aedd5f5b": [530],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [503],
                    "57c04d62ada3a102248b48f34c755159": [505],
                    "816b147dcf3305839f723a131b9ad6af": [515],
                    "84000630d1b69a0fe870c94fb26a32bc": [522],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "tip_amount"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "tolls_amount",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "tolls_amount": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    20,
                    24,
                    28,
                    24,
                    21,
                    25,
                    23,
                    26,
                    24,
                    19,
                    24,
                    26,
                    22,
                    26,
                    20,
                    27,
                    27,
                    23,
                    31,
                    27,
                    28,
                    32,
                    23,
                    26,
                    27,
                    29,
                    20,
                    19,
                    22,
                    30,
                    27,
                    22,
                    21,
                    22,
                    16,
                    20,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [20],
                    "562969eaef9c843cb4531aecbc13bbcb": [24],
                    "569a4a80bf434c888593c651dbf2f157": [28],
                    "f6c389dcef63c1f214c30f66b66945c0": [24],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [21],
                    "e20c38f98b9830a40b851939ca7189d4": [25],
                    "f2e4d3da6556638b55df8ce509b094c2": [23],
                    "44c1b1947c9049e7db62c5320dde4c63": [26],
                    "47157bdaf05a7992473cd699cabaef74": [24],
                    "08085632aff9ce4cebbb8023049e1aec": [19],
                    "bb54e4fa3906387218be10cff631a7c2": [24],
                    "58ce3b40d384eacd9bad7d916eb8f705": [26],
                    "0327cfb13205ec8512e1c28e438ab43b": [22],
                    "0808e185a52825d22356de2fe00a8f5f": [26],
                    "90bb41c1fbd7c71c05dbc8695320af71": [20],
                    "6c7e43619fe5e6963e8159cc84a28321": [27],
                    "976b121b46db6967854b9c1a6628396b": [27],
                    "9e58d3c72c7006b6f5800b623fbc9818": [23],
                    "ce5f02ac408b7b5c500050190f549736": [31],
                    "bb81456ec79522bf02f34b02762f95e0": [27],
                    "b20800a7faafd2808d6c888577a2ba1d": [28],
                    "33d910f95326c0c7dfe7536d1cfeba51": [32],
                    "61e4931d87cb627df2a19b8bc5819b7b": [23],
                    "3692b23382fd4734215465251290c65b": [26],
                    "eff8910cddcdff62e4741243099240d5": [27],
                    "f67d274202366f6b976414c950ca14bd": [29],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [20],
                    "73612fdabd337d5a8279acc30ce22d00": [19],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [22],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [30],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [27],
                    "940576153c66af14a949fd19aedd5f5b": [22],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [21],
                    "57c04d62ada3a102248b48f34c755159": [22],
                    "816b147dcf3305839f723a131b9ad6af": [16],
                    "84000630d1b69a0fe870c94fb26a32bc": [20],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "tolls_amount"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "improvement_surcharge",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "improvement_surcharge": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [3],
                    "562969eaef9c843cb4531aecbc13bbcb": [3],
                    "569a4a80bf434c888593c651dbf2f157": [3],
                    "f6c389dcef63c1f214c30f66b66945c0": [3],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [3],
                    "e20c38f98b9830a40b851939ca7189d4": [3],
                    "f2e4d3da6556638b55df8ce509b094c2": [3],
                    "44c1b1947c9049e7db62c5320dde4c63": [3],
                    "47157bdaf05a7992473cd699cabaef74": [3],
                    "08085632aff9ce4cebbb8023049e1aec": [3],
                    "bb54e4fa3906387218be10cff631a7c2": [3],
                    "58ce3b40d384eacd9bad7d916eb8f705": [3],
                    "0327cfb13205ec8512e1c28e438ab43b": [3],
                    "0808e185a52825d22356de2fe00a8f5f": [3],
                    "90bb41c1fbd7c71c05dbc8695320af71": [3],
                    "6c7e43619fe5e6963e8159cc84a28321": [3],
                    "976b121b46db6967854b9c1a6628396b": [3],
                    "9e58d3c72c7006b6f5800b623fbc9818": [3],
                    "ce5f02ac408b7b5c500050190f549736": [3],
                    "bb81456ec79522bf02f34b02762f95e0": [3],
                    "b20800a7faafd2808d6c888577a2ba1d": [3],
                    "33d910f95326c0c7dfe7536d1cfeba51": [3],
                    "61e4931d87cb627df2a19b8bc5819b7b": [3],
                    "3692b23382fd4734215465251290c65b": [3],
                    "eff8910cddcdff62e4741243099240d5": [3],
                    "f67d274202366f6b976414c950ca14bd": [3],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [3],
                    "73612fdabd337d5a8279acc30ce22d00": [3],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [3],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [3],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [3],
                    "940576153c66af14a949fd19aedd5f5b": [3],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [3],
                    "57c04d62ada3a102248b48f34c755159": [3],
                    "816b147dcf3305839f723a131b9ad6af": [3],
                    "84000630d1b69a0fe870c94fb26a32bc": [3],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "improvement_surcharge"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "total_amount",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "total_amount": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    898,
                    884,
                    905,
                    942,
                    953,
                    945,
                    969,
                    966,
                    973,
                    972,
                    1043,
                    1000,
                    942,
                    1016,
                    1016,
                    1012,
                    1026,
                    1044,
                    1047,
                    1077,
                    1073,
                    1070,
                    1068,
                    1060,
                    1037,
                    1036,
                    1060,
                    1387,
                    2018,
                    1440,
                    1154,
                    1153,
                    1154,
                    1161,
                    1154,
                    1164,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [898],
                    "562969eaef9c843cb4531aecbc13bbcb": [884],
                    "569a4a80bf434c888593c651dbf2f157": [905],
                    "f6c389dcef63c1f214c30f66b66945c0": [942],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [953],
                    "e20c38f98b9830a40b851939ca7189d4": [945],
                    "f2e4d3da6556638b55df8ce509b094c2": [969],
                    "44c1b1947c9049e7db62c5320dde4c63": [966],
                    "47157bdaf05a7992473cd699cabaef74": [973],
                    "08085632aff9ce4cebbb8023049e1aec": [972],
                    "bb54e4fa3906387218be10cff631a7c2": [1043],
                    "58ce3b40d384eacd9bad7d916eb8f705": [1000],
                    "0327cfb13205ec8512e1c28e438ab43b": [942],
                    "0808e185a52825d22356de2fe00a8f5f": [1016],
                    "90bb41c1fbd7c71c05dbc8695320af71": [1016],
                    "6c7e43619fe5e6963e8159cc84a28321": [1012],
                    "976b121b46db6967854b9c1a6628396b": [1026],
                    "9e58d3c72c7006b6f5800b623fbc9818": [1044],
                    "ce5f02ac408b7b5c500050190f549736": [1047],
                    "bb81456ec79522bf02f34b02762f95e0": [1077],
                    "b20800a7faafd2808d6c888577a2ba1d": [1073],
                    "33d910f95326c0c7dfe7536d1cfeba51": [1070],
                    "61e4931d87cb627df2a19b8bc5819b7b": [1068],
                    "3692b23382fd4734215465251290c65b": [1060],
                    "eff8910cddcdff62e4741243099240d5": [1037],
                    "f67d274202366f6b976414c950ca14bd": [1036],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [1060],
                    "73612fdabd337d5a8279acc30ce22d00": [1387],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [2018],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [1440],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [1154],
                    "940576153c66af14a949fd19aedd5f5b": [1153],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [1154],
                    "57c04d62ada3a102248b48f34c755159": [1161],
                    "816b147dcf3305839f723a131b9ad6af": [1154],
                    "84000630d1b69a0fe870c94fb26a32bc": [1164],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "total_amount"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": "congestion_surcharge",
            },
            details={
                INFERRED_SEMANTIC_TYPE_KEY: {
                    "congestion_surcharge": SemanticDomainTypes.NUMERIC,
                },
            },
            rule_name="categorical_columns_rule",
        ): {
            "$parameter.column_distinct_values_count": {
                "value": [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1,
                    3,
                    3,
                    4,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    4,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                    3,
                ],
                "attributed_value": {
                    "c92d0679f769ac83fef2bb5eaac5d12a": [0],
                    "562969eaef9c843cb4531aecbc13bbcb": [0],
                    "569a4a80bf434c888593c651dbf2f157": [0],
                    "f6c389dcef63c1f214c30f66b66945c0": [0],
                    "c4fe9afce1cf3e83eb8518a9f5abc754": [0],
                    "e20c38f98b9830a40b851939ca7189d4": [0],
                    "f2e4d3da6556638b55df8ce509b094c2": [0],
                    "44c1b1947c9049e7db62c5320dde4c63": [0],
                    "47157bdaf05a7992473cd699cabaef74": [0],
                    "08085632aff9ce4cebbb8023049e1aec": [0],
                    "bb54e4fa3906387218be10cff631a7c2": [0],
                    "58ce3b40d384eacd9bad7d916eb8f705": [0],
                    "0327cfb13205ec8512e1c28e438ab43b": [1],
                    "0808e185a52825d22356de2fe00a8f5f": [3],
                    "90bb41c1fbd7c71c05dbc8695320af71": [3],
                    "6c7e43619fe5e6963e8159cc84a28321": [4],
                    "976b121b46db6967854b9c1a6628396b": [3],
                    "9e58d3c72c7006b6f5800b623fbc9818": [3],
                    "ce5f02ac408b7b5c500050190f549736": [3],
                    "bb81456ec79522bf02f34b02762f95e0": [3],
                    "b20800a7faafd2808d6c888577a2ba1d": [3],
                    "33d910f95326c0c7dfe7536d1cfeba51": [3],
                    "61e4931d87cb627df2a19b8bc5819b7b": [3],
                    "3692b23382fd4734215465251290c65b": [3],
                    "eff8910cddcdff62e4741243099240d5": [4],
                    "f67d274202366f6b976414c950ca14bd": [3],
                    "7b3ce20a8e8cf3097bb9df270a7ae63a": [3],
                    "73612fdabd337d5a8279acc30ce22d00": [3],
                    "ad2ad2a70c3e0bf94ddef3f893e92291": [3],
                    "8ce0d477f610ea18e2ea4fbbb46de857": [3],
                    "ff5a6cc031dd2c98b8bccd4766af38c1": [3],
                    "940576153c66af14a949fd19aedd5f5b": [3],
                    "ab05b4fb82e37c8cf5b1ac40d0a37fe9": [3],
                    "57c04d62ada3a102248b48f34c755159": [3],
                    "816b147dcf3305839f723a131b9ad6af": [3],
                    "84000630d1b69a0fe870c94fb26a32bc": [3],
                },
                "details": {
                    "metric_configuration": {
                        "metric_name": "column.distinct_values.count",
                        "domain_kwargs": {"column": "congestion_surcharge"},
                        "metric_value_kwargs": None,
                        "metric_dependencies": None,
                    },
                    "num_batches": 36,
                },
            }
        },
    }
    return expected_metrics_by_domain


@pytest.fixture
def quentin_expected_rule_based_profiler_configuration() -> Callable:
    def _profiler_config(
        name: str, exclude_column_names: Optional[List[str]] = None
    ) -> RuleBasedProfilerConfig:
        exclude_column_names = exclude_column_names or []
        expected_rule_based_profiler_config: RuleBasedProfilerConfig = RuleBasedProfilerConfig(
            config_version=1.0,
            name=name,
            variables={"random_seed": None},
            rules={
                "table_rule": {
                    "variables": {
                        "false_positive_rate": 0.05,
                        "quantile_statistic_interpolation_method": "auto",
                        "estimator": "bootstrap",
                        "n_resamples": 9999,
                        "include_estimator_samples_histogram_in_details": False,
                        "truncate_values": {
                            "lower_bound": 0,
                        },
                        "round_decimals": 0,
                    },
                    "domain_builder": {
                        "class_name": "TableDomainBuilder",
                        "module_name": "great_expectations.rule_based_profiler.domain_builder.table_domain_builder",
                    },
                    "parameter_builders": [
                        {
                            "replace_nan_with_zero": True,
                            "name": "table_row_count",
                            "module_name": "great_expectations.rule_based_profiler.parameter_builder.metric_multi_batch_parameter_builder",
                            "enforce_numeric_metric": True,
                            "class_name": "MetricMultiBatchParameterBuilder",
                            "reduce_scalar_metric": True,
                            "metric_name": "table.row_count",
                        },
                    ],
                    "expectation_configuration_builders": [
                        {
                            "max_value": "$parameter.table_row_count_range.value[1]",
                            "validation_parameter_builder_configs": [
                                {
                                    "replace_nan_with_zero": True,
                                    "name": "table_row_count_range",
                                    "module_name": "great_expectations.rule_based_profiler.parameter_builder.numeric_metric_range_multi_batch_parameter_builder",
                                    "truncate_values": "$variables.truncate_values",
                                    "enforce_numeric_metric": True,
                                    "n_resamples": "$variables.n_resamples",
                                    "class_name": "NumericMetricRangeMultiBatchParameterBuilder",
                                    "estimator": "$variables.estimator",
                                    "reduce_scalar_metric": True,
                                    "metric_name": "table.row_count",
                                    "metric_multi_batch_parameter_builder_name": "table_row_count",
                                    "metric_domain_kwargs": "$domain.domain_kwargs",
                                    "false_positive_rate": "$variables.false_positive_rate",
                                    "quantile_statistic_interpolation_method": "$variables.quantile_statistic_interpolation_method",
                                    "random_seed": "$variables.random_seed",
                                    "include_estimator_samples_histogram_in_details": "$variables.include_estimator_samples_histogram_in_details",
                                    "round_decimals": "$variables.round_decimals",
                                    "evaluation_parameter_builder_configs": [
                                        {
                                            "enforce_numeric_metric": True,
                                            "replace_nan_with_zero": True,
                                            "name": "table_row_count",
                                            "class_name": "MetricMultiBatchParameterBuilder",
                                            "evaluation_parameter_builder_configs": None,
                                            "metric_value_kwargs": None,
                                            "module_name": "great_expectations.rule_based_profiler.parameter_builder.metric_multi_batch_parameter_builder",
                                            "metric_domain_kwargs": None,
                                            "reduce_scalar_metric": True,
                                            "metric_name": "table.row_count",
                                        }
                                    ],
                                },
                            ],
                            "expectation_type": "expect_table_row_count_to_be_between",
                            "module_name": "great_expectations.rule_based_profiler.expectation_configuration_builder.default_expectation_configuration_builder",
                            "meta": {
                                "profiler_details": "$parameter.table_row_count_range.details"
                            },
                            "class_name": "DefaultExpectationConfigurationBuilder",
                            "min_value": "$parameter.table_row_count_range.value[0]",
                        },
                    ],
                },
                "categorical_columns_rule": {
                    "variables": {
                        "mostly": 1.0,
                        "strict_min": False,
                        "strict_max": False,
                        "false_positive_rate": 0.05,
                        "quantile_statistic_interpolation_method": "auto",
                        "estimator": "bootstrap",
                        "n_resamples": 9999,
                        "include_estimator_samples_histogram_in_details": False,
                        "truncate_values": {
                            "lower_bound": 0.0,
                        },
                        "round_decimals": 1,
                    },
                    "domain_builder": {
                        "allowed_semantic_types_passthrough": ["logic"],
                        "class_name": "CategoricalColumnDomainBuilder",
                        "cardinality_limit_mode": {
                            "name": "REL_100",
                            "max_proportion_unique": 1.0,
                            "metric_name_defining_limit": "column.unique_proportion",
                        },
                        "module_name": "great_expectations.rule_based_profiler.domain_builder.categorical_column_domain_builder",
                        "exclude_column_names": sorted(
                            [
                                "id",
                            ]
                            + exclude_column_names
                        ),
                        "exclude_column_name_suffixes": ["_id"],
                        "exclude_semantic_types": ["binary", "currency", "identifier"],
                    },
                    "parameter_builders": [
                        {
                            "metric_domain_kwargs": "$domain.domain_kwargs",
                            "replace_nan_with_zero": True,
                            "name": "column_distinct_values_count",
                            "module_name": "great_expectations.rule_based_profiler.parameter_builder.metric_multi_batch_parameter_builder",
                            "enforce_numeric_metric": True,
                            "class_name": "MetricMultiBatchParameterBuilder",
                            "reduce_scalar_metric": True,
                            "metric_name": "column.distinct_values.count",
                        },
                    ],
                    "expectation_configuration_builders": [
                        {
                            "min_value": "$parameter.column_distinct_values_count_range.value[0]",
                            "class_name": "DefaultExpectationConfigurationBuilder",
                            "module_name": "great_expectations.rule_based_profiler.expectation_configuration_builder.default_expectation_configuration_builder",
                            "meta": {
                                "profiler_details": "$parameter.column_distinct_values_count_range.details"
                            },
                            "expectation_type": "expect_column_unique_value_count_to_be_between",
                            "max_value": "$parameter.column_distinct_values_count_range.value[1]",
                            "strict_min": "$variables.strict_min",
                            "strict_max": "$variables.strict_max",
                            "column": "$domain.domain_kwargs.column",
                            "validation_parameter_builder_configs": [
                                {
                                    "class_name": "NumericMetricRangeMultiBatchParameterBuilder",
                                    "metric_domain_kwargs": "$domain.domain_kwargs",
                                    "metric_multi_batch_parameter_builder_name": "column_distinct_values_count",
                                    "estimator": "$variables.estimator",
                                    "false_positive_rate": "$variables.false_positive_rate",
                                    "name": "column_distinct_values_count_range",
                                    "round_decimals": "$variables.round_decimals",
                                    "reduce_scalar_metric": True,
                                    "metric_name": "column.distinct_values.count",
                                    "enforce_numeric_metric": True,
                                    "quantile_statistic_interpolation_method": "$variables.quantile_statistic_interpolation_method",
                                    "replace_nan_with_zero": True,
                                    "n_resamples": "$variables.n_resamples",
                                    "module_name": "great_expectations.rule_based_profiler.parameter_builder.numeric_metric_range_multi_batch_parameter_builder",
                                    "include_estimator_samples_histogram_in_details": "$variables.include_estimator_samples_histogram_in_details",
                                    "truncate_values": "$variables.truncate_values",
                                    "evaluation_parameter_builder_configs": [
                                        {
                                            "enforce_numeric_metric": True,
                                            "replace_nan_with_zero": True,
                                            "name": "column_distinct_values_count",
                                            "class_name": "MetricMultiBatchParameterBuilder",
                                            "evaluation_parameter_builder_configs": None,
                                            "metric_value_kwargs": None,
                                            "module_name": "great_expectations.rule_based_profiler.parameter_builder.metric_multi_batch_parameter_builder",
                                            "metric_domain_kwargs": "$domain.domain_kwargs",
                                            "reduce_scalar_metric": True,
                                            "metric_name": "column.distinct_values.count",
                                        }
                                    ],
                                },
                            ],
                        },
                    ],
                },
            },
        )
        return expected_rule_based_profiler_config

    return _profiler_config


@pytest.fixture
def quentin_expected_expectation_suite(
    quentin_expected_rule_based_profiler_configuration,
) -> Callable:
    def _expectation_suite(name: str) -> ExpectationSuite:
        expected_expect_table_row_count_to_be_between_expectation_configuration: ExpectationConfiguration = ExpectationConfiguration(
            **{
                "expectation_type": "expect_table_row_count_to_be_between",
                "kwargs": {
                    "min_value": 10000,
                    "max_value": 10000,
                },
                "meta": {
                    "profiler_details": {
                        "metric_configuration": {
                            "metric_name": "table.row_count",
                            "domain_kwargs": {},
                            "metric_value_kwargs": None,
                            "metric_dependencies": None,
                        },
                        "num_batches": 36,
                    },
                },
            },
        )

        expected_expect_column_unique_value_count_to_be_between_expectation_configuration_list: List[
            ExpectationConfiguration
        ] = [
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "pickup_datetime"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 9983,
                        "strict_min": False,
                        "column": "pickup_datetime",
                        "min_value": 9945,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "dropoff_datetime"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 9985,
                        "strict_min": False,
                        "column": "dropoff_datetime",
                        "min_value": 9958,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "passenger_count"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 8,
                        "strict_min": False,
                        "column": "passenger_count",
                        "min_value": 7,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "trip_distance"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 1430,
                        "strict_min": False,
                        "column": "trip_distance",
                        "min_value": 1159,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "store_and_fwd_flag"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 2,
                        "strict_min": False,
                        "column": "store_and_fwd_flag",
                        "min_value": 2,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "payment_type"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 4,
                        "strict_min": False,
                        "column": "payment_type",
                        "min_value": 4,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "fare_amount"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 813,
                        "strict_min": False,
                        "column": "fare_amount",
                        "min_value": 153,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "extra"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 15,
                        "strict_min": False,
                        "column": "extra",
                        "min_value": 5,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "mta_tax"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 4,
                        "strict_min": False,
                        "column": "mta_tax",
                        "min_value": 3,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "tip_amount"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 608,
                        "strict_min": False,
                        "column": "tip_amount",
                        "min_value": 469,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "tolls_amount"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 31,
                        "strict_min": False,
                        "column": "tolls_amount",
                        "min_value": 18,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "improvement_surcharge"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 3,
                        "strict_min": False,
                        "column": "improvement_surcharge",
                        "min_value": 3,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "total_amount"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 1440,
                        "strict_min": False,
                        "column": "total_amount",
                        "min_value": 898,
                    },
                }
            ),
            ExpectationConfiguration(
                **{
                    "meta": {
                        "profiler_details": {
                            "metric_configuration": {
                                "metric_name": "column.distinct_values.count",
                                "domain_kwargs": {"column": "congestion_surcharge"},
                                "metric_value_kwargs": None,
                                "metric_dependencies": None,
                            },
                            "num_batches": 36,
                        }
                    },
                    "expectation_type": "expect_column_unique_value_count_to_be_between",
                    "kwargs": {
                        "strict_max": False,
                        "max_value": 4,
                        "strict_min": False,
                        "column": "congestion_surcharge",
                        "min_value": 0,
                    },
                }
            ),
        ]

        expected_expectation_configurations: List[ExpectationConfiguration] = (
            [
                expected_expect_table_row_count_to_be_between_expectation_configuration,
            ]
            + expected_expect_column_unique_value_count_to_be_between_expectation_configuration_list
        )

        expectation_suite_name: str = "my_suite"

        expected_expectation_suite: ExpectationSuite = ExpectationSuite(
            expectation_suite_name=expectation_suite_name,
        )

        expectation_configuration: ExpectationConfiguration
        for expectation_configuration in expected_expectation_configurations:
            expected_expectation_suite._add_expectation(
                expectation_configuration=expectation_configuration,
                send_usage_event=False,
            )

        expected_expectation_suite_meta: Dict[str, Any] = {
            "citations": [
                {
                    "citation_date": "2019-09-26T13:42:41.000000Z",
                    "profiler_config": quentin_expected_rule_based_profiler_configuration(
                        name=name
                    ).to_json_dict(),
                    "comment": "Suite created by Rule-Based Profiler with the configuration included.",
                }
            ]
        }

        expected_expectation_suite.meta = expected_expectation_suite_meta

        return expected_expectation_suite

    return _expectation_suite


@pytest.fixture
def bobby_volume_data_assistant_result(
    bobby_columnar_table_multi_batch_deterministic_data_context: DataContext,
) -> VolumeDataAssistantResult:
    context: DataContext = bobby_columnar_table_multi_batch_deterministic_data_context

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    data_assistant_result: DataAssistantResult = context.assistants.volume.run(
        batch_request=batch_request
    )

    return cast(VolumeDataAssistantResult, data_assistant_result)


@pytest.fixture
def quentin_explicit_instantiation_result_actual_time(
    quentin_columnar_table_multi_batch_data_context,
    set_consistent_seed_within_numeric_metric_range_multi_batch_parameter_builder,
) -> Tuple[Validator, VolumeDataAssistantResult]:
    context: DataContext = quentin_columnar_table_multi_batch_data_context

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    validator: Validator = get_validator_with_expectation_suite(
        data_context=context,
        batch_list=None,
        batch_request=batch_request,
        expectation_suite_name=None,
        expectation_suite=None,
        component_name="volume_data_assistant",
        persist=False,
    )
    assert len(validator.batches) == 36

    data_assistant_name: str = "test_volume_data_assistant"

    data_assistant: DataAssistant = VolumeDataAssistant(
        name=data_assistant_name,
        validator=validator,
    )

    data_assistant_result: DataAssistantResult = data_assistant.run()

    return validator, cast(VolumeDataAssistantResult, data_assistant_result)


@pytest.fixture
@freeze_time("09/26/2019 13:42:41")
def quentin_explicit_instantiation_result_frozen_time(
    quentin_columnar_table_multi_batch_data_context,
    set_consistent_seed_within_numeric_metric_range_multi_batch_parameter_builder,
) -> Tuple[Validator, VolumeDataAssistantResult]:
    context: DataContext = quentin_columnar_table_multi_batch_data_context

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    validator: Validator = get_validator_with_expectation_suite(
        data_context=context,
        batch_list=None,
        batch_request=batch_request,
        expectation_suite_name=None,
        expectation_suite=None,
        component_name="volume_data_assistant",
        persist=False,
    )
    assert len(validator.batches) == 36

    data_assistant_name: str = "test_volume_data_assistant"

    data_assistant: DataAssistant = VolumeDataAssistant(
        name=data_assistant_name,
        validator=validator,
    )

    data_assistant_result: DataAssistantResult = data_assistant.run()

    return validator, cast(VolumeDataAssistantResult, data_assistant_result)


@pytest.fixture
def quentin_implicit_invocation_result_actual_time(
    quentin_columnar_table_multi_batch_data_context,
    set_consistent_seed_within_numeric_metric_range_multi_batch_parameter_builder,
):
    context: DataContext = quentin_columnar_table_multi_batch_data_context

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    data_assistant_result: DataAssistantResult = context.assistants.volume.run(
        batch_request=batch_request
    )

    return cast(VolumeDataAssistantResult, data_assistant_result)


@pytest.fixture
@freeze_time("09/26/2019 13:42:41")
def quentin_implicit_invocation_result_frozen_time(
    quentin_columnar_table_multi_batch_data_context,
    set_consistent_seed_within_numeric_metric_range_multi_batch_parameter_builder,
):
    context: DataContext = quentin_columnar_table_multi_batch_data_context

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    data_assistant_result: DataAssistantResult = context.assistants.volume.run(
        batch_request=batch_request
    )

    return cast(VolumeDataAssistantResult, data_assistant_result)


def run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
    context: DataContext,
    new_cell: str,
    implicit: bool,
):
    """
    To set this test up we:
    - create a suite
    - write code (as a string) for creating a VolumeDataAssistantResult
    - add a new cell to the notebook that was passed to this method
    - write both cells to ipynb file

    We then:
    - load the notebook back from disk
    - execute the notebook (Note: this will raise various errors like
      CellExecutionError if any cell in the notebook fails)
    """
    root_dir: str = context.root_directory

    expectation_suite_name: str = "test_suite"
    context.create_expectation_suite(
        expectation_suite_name=expectation_suite_name, overwrite_existing=True
    )

    notebook_path: str = os.path.join(root_dir, "run_volume_data_assistant.ipynb")

    notebook_code_initialization: str = """
    from typing import Optional, Union

    import uuid

    import great_expectations as ge
    from great_expectations.data_context import BaseDataContext
    from great_expectations.validator.validator import Validator
    from great_expectations.rule_based_profiler.data_assistant import (
        DataAssistant,
        VolumeDataAssistant,
    )
    from great_expectations.rule_based_profiler.types.data_assistant_result import DataAssistantResult
    from great_expectations.rule_based_profiler.helpers.util import get_validator_with_expectation_suite
    import great_expectations.exceptions as ge_exceptions

    context = ge.get_context()

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    """

    explicit_instantiation_code: str = """
    validator: Validator = get_validator_with_expectation_suite(
        data_context=context,
        batch_list=None,
        batch_request=batch_request,
        expectation_suite_name=None,
        expectation_suite=None,
        component_name="volume_data_assistant",
        persist=False,
    )

    data_assistant: DataAssistant = VolumeDataAssistant(
        name="test_volume_data_assistant",
        validator=validator,
    )

    data_assistant_result: DataAssistantResult = data_assistant.run()
    """

    implicit_invocation_code: str = """
    data_assistant_result: DataAssistantResult = context.assistants.volume.run(batch_request=batch_request)
    """

    notebook_code: str
    if implicit:
        notebook_code = notebook_code_initialization + implicit_invocation_code
    else:
        notebook_code = notebook_code_initialization + explicit_instantiation_code

    nb = nbformat.v4.new_notebook()
    nb["cells"] = []
    nb["cells"].append(nbformat.v4.new_code_cell(notebook_code))
    nb["cells"].append(nbformat.v4.new_code_cell(new_cell))

    # Write notebook to path and load it as NotebookNode
    with open(notebook_path, "w") as f:
        nbformat.write(nb, f)

    nb: nbformat.notebooknode.NotebookNode = load_notebook_from_path(
        notebook_path=notebook_path
    )

    # Run notebook
    ep: nbconvert.preprocessors.ExecutePreprocessor = (
        nbconvert.preprocessors.ExecutePreprocessor(timeout=180, kernel_name="python3")
    )
    ep.preprocess(nb, {"metadata": {"path": root_dir}})


def test_volume_data_assistant_result_serialization(
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
) -> None:
    volume_data_assistant_result_as_dict: dict = (
        bobby_volume_data_assistant_result.to_dict()
    )
    assert (
        set(volume_data_assistant_result_as_dict.keys())
        == DataAssistantResult.ALLOWED_KEYS
    )
    assert (
        bobby_volume_data_assistant_result.to_json_dict()
        == volume_data_assistant_result_as_dict
    )


@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
def test_volume_data_assistant_result_get_expectation_suite(
    mock_emit,
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
):
    expectation_suite_name: str = "my_suite"

    suite: ExpectationSuite = bobby_volume_data_assistant_result.get_expectation_suite(
        expectation_suite_name=expectation_suite_name
    )

    assert suite is not None and len(suite.expectations) > 0

    assert mock_emit.call_count == 1

    # noinspection PyUnresolvedReferences
    actual_events: List[unittest.mock._Call] = mock_emit.call_args_list
    assert (
        actual_events[-1][0][0]["event"]
        == UsageStatsEvents.DATA_ASSISTANT_RESULT_GET_EXPECTATION_SUITE.value
    )


def test_volume_data_assistant_result_batch_id_to_batch_identifier_display_name_map_coverage(
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
):
    metrics_by_domain: Optional[
        Dict[Domain, Dict[str, ParameterNode]]
    ] = bobby_volume_data_assistant_result.metrics_by_domain

    parameter_values_for_fully_qualified_parameter_names: Dict[str, ParameterNode]
    parameter_node: ParameterNode
    batch_id: str
    assert all(
        bobby_volume_data_assistant_result.batch_id_to_batch_identifier_display_name_map[
            batch_id
        ]
        is not None
        for parameter_values_for_fully_qualified_parameter_names in metrics_by_domain.values()
        for parameter_node in parameter_values_for_fully_qualified_parameter_names.values()
        for batch_id in (
            parameter_node[FULLY_QUALIFIED_PARAMETER_NAME_ATTRIBUTED_VALUE_KEY]
            if FULLY_QUALIFIED_PARAMETER_NAME_ATTRIBUTED_VALUE_KEY in parameter_node
            else {}
        ).keys()
    )


def test_volume_data_assistant_get_metrics_and_expectations_using_explicit_instantiation(
    quentin_explicit_instantiation_result_frozen_time,
    quentin_expected_metrics_by_domain,
    quentin_expected_expectation_suite,
    quentin_expected_rule_based_profiler_configuration,
):
    validator: Validator
    data_assistant_result: DataAssistantResult
    validator, data_assistant_result = quentin_explicit_instantiation_result_frozen_time

    data_assistant_name: str = "test_volume_data_assistant"

    expected_expectation_suite: ExpectationSuite = quentin_expected_expectation_suite(
        name=data_assistant_name
    )

    assert data_assistant_result.metrics_by_domain == quentin_expected_metrics_by_domain

    expectation_configuration: ExpectationConfiguration
    for expectation_configuration in data_assistant_result.expectation_configurations:
        if "profiler_details" in expectation_configuration.meta:
            expectation_configuration.meta["profiler_details"].pop(
                "estimation_histogram", None
            )

    assert (
        data_assistant_result.expectation_configurations
        == expected_expectation_suite.expectations
    )

    assert deep_filter_properties_iterable(
        properties=data_assistant_result.profiler_config.to_json_dict(),
        delete_fields={"random_seed"},
    ) == deep_filter_properties_iterable(
        properties=quentin_expected_rule_based_profiler_configuration(
            name=data_assistant_name,
        ).to_json_dict(),
        delete_fields={"random_seed"},
    )

    data_assistant_result.citation.pop("profiler_config", None)
    expected_expectation_suite.meta["citations"][0].pop("profiler_config", None)

    data_assistant_result.citation.pop("citation_date", None)
    expected_expectation_suite.meta["citations"][0].pop("citation_date", None)
    assert (
        data_assistant_result.citation
        == expected_expectation_suite.meta["citations"][0]
    )

    actual_expectation_suite: ExpectationSuite = (
        data_assistant_result.get_expectation_suite(expectation_suite_name="my_suite")
    )
    actual_expectation_suite.meta.pop("great_expectations_version", None)
    expected_expectation_suite.meta.pop("great_expectations_version", None)
    actual_expectation_suite.meta["citations"][0].pop("citation_date", None)
    expected_expectation_suite.meta["citations"][0].pop("citation_date", None)
    assert actual_expectation_suite == expected_expectation_suite


@freeze_time("09/26/2019 13:42:41")
def test_volume_data_assistant_get_metrics_and_expectations_using_implicit_invocation(
    quentin_implicit_invocation_result_frozen_time,
    quentin_expected_metrics_by_domain,
    quentin_expected_expectation_suite,
    quentin_expected_rule_based_profiler_configuration,
):
    data_assistant_result: DataAssistantResult = (
        quentin_implicit_invocation_result_frozen_time
    )

    registered_data_assistant_name: str = "volume_data_assistant"

    expected_expectation_suite: ExpectationSuite = quentin_expected_expectation_suite(
        name=registered_data_assistant_name
    )

    assert data_assistant_result.metrics_by_domain == quentin_expected_metrics_by_domain

    expectation_configuration: ExpectationConfiguration
    for expectation_configuration in data_assistant_result.expectation_configurations:
        if "profiler_details" in expectation_configuration.meta:
            expectation_configuration.meta["profiler_details"].pop(
                "estimation_histogram", None
            )

    assert (
        data_assistant_result.expectation_configurations
        == expected_expectation_suite.expectations
    )

    assert deep_filter_properties_iterable(
        properties=data_assistant_result.profiler_config.to_json_dict(),
        delete_fields={"random_seed"},
    ) == deep_filter_properties_iterable(
        properties=quentin_expected_rule_based_profiler_configuration(
            name=registered_data_assistant_name
        ).to_json_dict(),
        delete_fields={"random_seed"},
    )

    data_assistant_result.citation.pop("profiler_config", None)
    expected_expectation_suite.meta["citations"][0].pop("profiler_config", None)

    data_assistant_result.citation.pop("citation_date", None)
    expected_expectation_suite.meta["citations"][0].pop("citation_date", None)
    assert (
        data_assistant_result.citation
        == expected_expectation_suite.meta["citations"][0]
    )

    actual_expectation_suite: ExpectationSuite = (
        data_assistant_result.get_expectation_suite(expectation_suite_name="my_suite")
    )
    actual_expectation_suite.meta.pop("great_expectations_version", None)
    expected_expectation_suite.meta.pop("great_expectations_version", None)
    actual_expectation_suite.meta["citations"][0].pop("citation_date", None)
    expected_expectation_suite.meta["citations"][0].pop("citation_date", None)
    assert actual_expectation_suite == expected_expectation_suite


@freeze_time("09/26/2019 13:42:41")
def test_volume_data_assistant_get_metrics_and_expectations_using_implicit_invocation_with_domain_type_directives(
    quentin_columnar_table_multi_batch_data_context,
    set_consistent_seed_within_numeric_metric_range_multi_batch_parameter_builder,
    quentin_expected_metrics_by_domain,
    quentin_expected_expectation_suite,
    quentin_expected_rule_based_profiler_configuration,
):
    context: DataContext = quentin_columnar_table_multi_batch_data_context

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    exclude_column_names: List[str] = [
        "dropoff_datetime",
        "store_and_fwd_flag",
        "extra",
        "congestion_surcharge",
    ]
    data_assistant_result: DataAssistantResult = context.assistants.volume.run(
        batch_request=batch_request,
        # include_column_names=include_column_names,
        exclude_column_names=exclude_column_names,
        # include_column_name_suffixes=include_column_name_suffixes,
        # exclude_column_name_suffixes=exclude_column_name_suffixes,
        # semantic_type_filter_module_name=semantic_type_filter_module_name,
        # semantic_type_filter_class_name=semantic_type_filter_class_name,
        # include_semantic_types=include_semantic_types,
        # exclude_semantic_types=exclude_semantic_types,
        # allowed_semantic_types_passthrough=allowed_semantic_types_passthrough,
        cardinality_limit_mode=CardinalityLimitMode.REL_100,
        # max_unique_values=max_unique_values,
        # max_proportion_unique=max_proportion_unique,
        # column_value_uniqueness_rule={
        #     "success_ratio": 0.8,
        # },
        # column_value_nullity_rule={
        # },
        # column_value_nonnullity_rule={
        # },
        # numeric_columns_rule={
        #     "false_positive_rate": 0.1,
        #     "random_seed": 43792,
        # },
        # datetime_columns_rule={
        #     "truncate_values": {
        #         "lower_bound": 0,
        #         "upper_bound": 4481049600,  # Friday, January 1, 2112 0:00:00
        #     },
        #     "round_decimals": 0,
        # },
        # text_columns_rule={
        #     "strict_min": True,
        #     "strict_max": True,
        #     "success_ratio": 0.8,
        # },
        # categorical_columns_rule={
        #     "false_positive_rate": 0.1,
        #     "round_decimals": 3,
        # },
    )

    column_name: str
    expected_excluded_domains: List[Domain] = [
        Domain(
            domain_type=MetricDomainTypes.COLUMN,
            domain_kwargs={
                "column": column_name,
            },
        )
        for column_name in exclude_column_names
    ]

    domain_key: Domain

    # noinspection PyTypeChecker
    quentin_expected_metrics_by_domain = dict(
        filter(
            lambda element: not any(
                element[0].is_superset(other=domain_key)
                for domain_key in expected_excluded_domains
            ),
            quentin_expected_metrics_by_domain.items(),
        )
    )

    registered_data_assistant_name: str = "volume_data_assistant"

    expected_expectation_suite: ExpectationSuite = quentin_expected_expectation_suite(
        name=registered_data_assistant_name
    )

    assert data_assistant_result.metrics_by_domain == quentin_expected_metrics_by_domain

    expectation_configuration: ExpectationConfiguration

    expected_expectation_suite.expectations = [
        expectation_configuration
        for expectation_configuration in expected_expectation_suite.expectations
        if not (
            expectation_configuration.kwargs
            and expectation_configuration.kwargs.get("column") in exclude_column_names
        )
    ]

    for expectation_configuration in data_assistant_result.expectation_configurations:
        if "profiler_details" in expectation_configuration.meta:
            expectation_configuration.meta["profiler_details"].pop(
                "estimation_histogram", None
            )

    assert (
        data_assistant_result.expectation_configurations
        == expected_expectation_suite.expectations
    )

    data_assistant_result_profiler_config_as_json_dict: dict = (
        deep_filter_properties_iterable(
            properties=data_assistant_result.profiler_config.to_json_dict(),
            delete_fields={"random_seed"},
        )
    )
    quentin_expected_rule_based_profiler_configuration_as_json_dict: dict = (
        deep_filter_properties_iterable(
            properties=quentin_expected_rule_based_profiler_configuration(
                name=registered_data_assistant_name,
                exclude_column_names=exclude_column_names,
            ).to_json_dict(),
            delete_fields={"random_seed"},
        )
    )
    data_assistant_result_profiler_config_as_json_dict["rules"][
        "categorical_columns_rule"
    ]["domain_builder"]["exclude_column_names"] = sorted(
        data_assistant_result_profiler_config_as_json_dict["rules"][
            "categorical_columns_rule"
        ]["domain_builder"]["exclude_column_names"]
    )
    quentin_expected_rule_based_profiler_configuration_as_json_dict["rules"][
        "categorical_columns_rule"
    ]["domain_builder"]["exclude_column_names"] = sorted(
        quentin_expected_rule_based_profiler_configuration_as_json_dict["rules"][
            "categorical_columns_rule"
        ]["domain_builder"]["exclude_column_names"]
    )
    assert (
        data_assistant_result_profiler_config_as_json_dict
        == quentin_expected_rule_based_profiler_configuration_as_json_dict
    )

    data_assistant_result.citation.pop("profiler_config", None)
    expected_expectation_suite.meta["citations"][0].pop("profiler_config", None)

    data_assistant_result.citation.pop("citation_date", None)
    expected_expectation_suite.meta["citations"][0].pop("citation_date", None)
    assert (
        data_assistant_result.citation
        == expected_expectation_suite.meta["citations"][0]
    )

    actual_expectation_suite: ExpectationSuite = (
        data_assistant_result.get_expectation_suite(expectation_suite_name="my_suite")
    )
    actual_expectation_suite.meta.pop("great_expectations_version", None)
    expected_expectation_suite.meta.pop("great_expectations_version", None)
    actual_expectation_suite.meta["citations"][0].pop("citation_date", None)
    expected_expectation_suite.meta["citations"][0].pop("citation_date", None)
    assert actual_expectation_suite == expected_expectation_suite


def test_volume_data_assistant_get_metrics_and_expectations_using_implicit_invocation_with_variables_directives(
    quentin_columnar_table_multi_batch_data_context,
):
    context: DataContext = quentin_columnar_table_multi_batch_data_context

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    data_assistant_result: DataAssistantResult = context.assistants.volume.run(
        batch_request=batch_request,
        # include_column_names=include_column_names,
        # exclude_column_names=exclude_column_names,
        # include_column_name_suffixes=include_column_name_suffixes,
        # exclude_column_name_suffixes=exclude_column_name_suffixes,
        # semantic_type_filter_module_name=semantic_type_filter_module_name,
        # semantic_type_filter_class_name=semantic_type_filter_class_name,
        # include_semantic_types=include_semantic_types,
        # exclude_semantic_types=exclude_semantic_types,
        # allowed_semantic_types_passthrough=allowed_semantic_types_passthrough,
        # cardinality_limit_mode=CardinalityLimitMode.REL_100,
        # max_unique_values=max_unique_values,
        # max_proportion_unique=max_proportion_unique,
        # column_value_uniqueness_rule={
        #     "success_ratio": 0.8,
        # },
        # column_value_nullity_rule={
        # },
        # column_value_nonnullity_rule={
        # },
        # numeric_columns_rule={
        #     "false_positive_rate": 0.1,
        #     "random_seed": 43792,
        # },
        # datetime_columns_rule={
        #     "truncate_values": {
        #         "lower_bound": 0,
        #         "upper_bound": 4481049600,  # Friday, January 1, 2112 0:00:00
        #     },
        #     "round_decimals": 0,
        # },
        # text_columns_rule={
        #     "strict_min": True,
        #     "strict_max": True,
        #     "success_ratio": 0.8,
        # },
        categorical_columns_rule={
            "false_positive_rate": 0.1,
            # "round_decimals": 3,
        },
    )
    assert (
        data_assistant_result.profiler_config.rules["categorical_columns_rule"][
            "variables"
        ]["false_positive_rate"]
        == 1.0e-1
    )


def test_volume_data_assistant_execution_time_within_proper_bounds_using_explicit_instantiation(
    quentin_explicit_instantiation_result_actual_time,
):
    validator: Validator
    data_assistant_result: DataAssistantResult
    validator, data_assistant_result = quentin_explicit_instantiation_result_actual_time

    # Execution time (in seconds) must have non-trivial value.
    assert data_assistant_result.execution_time > 0.0


def test_volume_data_assistant_execution_time_within_proper_bounds_using_implicit_invocation(
    quentin_implicit_invocation_result_actual_time,
):
    data_assistant_result: DataAssistantResult = (
        quentin_implicit_invocation_result_actual_time
    )

    # Execution time (in seconds) must have non-trivial value.
    assert data_assistant_result.execution_time > 0.0


def test_volume_data_assistant_batch_id_order_consistency_in_attributed_metrics_by_domain_using_explicit_instantiation(
    quentin_explicit_instantiation_result_actual_time,
):
    validator: Validator
    data_assistant_result: DataAssistantResult
    validator, data_assistant_result = quentin_explicit_instantiation_result_actual_time
    metrics_by_domain: Optional[
        Dict[Domain, Dict[str, ParameterNode]]
    ] = data_assistant_result.metrics_by_domain

    batch: Batch
    expected_batch_ids: List[str] = [batch.id for batch in validator.batches.values()]

    parameter_values_for_fully_qualified_parameter_names: Dict[str, ParameterNode]
    fully_qualified_parameter_name: str
    parameter_node: ParameterNode
    assert all(
        list(parameter_node[FULLY_QUALIFIED_PARAMETER_NAME_ATTRIBUTED_VALUE_KEY].keys())
        == expected_batch_ids
        for parameter_values_for_fully_qualified_parameter_names in metrics_by_domain.values()
        for fully_qualified_parameter_name, parameter_node in parameter_values_for_fully_qualified_parameter_names.items()
    )


def test_volume_data_assistant_plot_descriptive_notebook_execution_fails(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    context: DataContext = bobby_columnar_table_multi_batch_deterministic_data_context

    new_cell: str = (
        "data_assistant_result.plot_metrics(this_is_not_a_real_parameter=True)"
    )

    with pytest.raises(nbconvert.preprocessors.CellExecutionError):
        run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
            context=context,
            new_cell=new_cell,
            implicit=False,
        )

    with pytest.raises(nbconvert.preprocessors.CellExecutionError):
        run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
            context=context,
            new_cell=new_cell,
            implicit=True,
        )


def test_volume_data_assistant_plot_descriptive_notebook_execution(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    context: DataContext = bobby_columnar_table_multi_batch_deterministic_data_context

    new_cell: str = "data_assistant_result.plot_metrics()"

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


def test_volume_data_assistant_plot_prescriptive_notebook_execution(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    context: DataContext = bobby_columnar_table_multi_batch_deterministic_data_context

    new_cell: str = "data_assistant_result.plot_expectations_and_metrics()"

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


def test_volume_data_assistant_plot_descriptive_theme_notebook_execution(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    context: DataContext = bobby_columnar_table_multi_batch_deterministic_data_context

    theme = {"font": "Comic Sans MS"}

    new_cell: str = f"data_assistant_result.plot_metrics(theme={theme})"

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


def test_volume_data_assistant_plot_prescriptive_theme_notebook_execution(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    context: DataContext = bobby_columnar_table_multi_batch_deterministic_data_context

    theme = {"font": "Comic Sans MS"}

    new_cell: str = (
        f"data_assistant_result.plot_expectations_and_metrics(theme={theme})"
    )

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


def test_volume_data_assistant_plot_returns_proper_dict_repr_of_table_domain_chart(
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
) -> None:
    plot_result: PlotResult = bobby_volume_data_assistant_result.plot_metrics()

    table_domain_chart: dict = plot_result.charts[0].to_dict()
    assert find_strings_in_nested_obj(table_domain_chart, ["Table Row Count per Batch"])


def test_volume_data_assistant_plot_returns_proper_dict_repr_of_column_domain_chart(
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
) -> None:
    plot_result: PlotResult = bobby_volume_data_assistant_result.plot_metrics()

    column_domain_charts: List[dict] = [p.to_dict() for p in plot_result.charts[1:]]
    assert len(column_domain_charts) == 18  # One for each column present

    columns: List[str] = [
        "VendorID",
        "pickup_datetime",
        "dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "RatecodeID",
        "store_and_fwd_flag",
        "PULocationID",
        "DOLocationID",
        "payment_type",
        "fare_amount",
        "extra",
        "mta_tax",
        "tip_amount",
        "tolls_amount",
        "improvement_surcharge",
        "total_amount",
        "congestion_surcharge",
    ]
    assert find_strings_in_nested_obj(column_domain_charts, columns)


def test_volume_data_assistant_plot_include_column_names_filters_output(
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
) -> None:
    include_column_names: List[str] = ["VendorID", "pickup_datetime"]
    plot_result: PlotResult = bobby_volume_data_assistant_result.plot_metrics(
        include_column_names=include_column_names
    )

    column_domain_charts: List[dict] = [p.to_dict() for p in plot_result.charts[1:]]
    assert len(column_domain_charts) == 2  # Normally 18 without filtering
    assert find_strings_in_nested_obj(column_domain_charts, include_column_names)


def test_volume_data_assistant_plot_exclude_column_names_filters_output(
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
) -> None:
    exclude_column_names: List[str] = ["VendorID", "pickup_datetime"]
    plot_result: PlotResult = bobby_volume_data_assistant_result.plot_metrics(
        exclude_column_names=exclude_column_names
    )

    column_domain_charts: List[dict] = [p.to_dict() for p in plot_result.charts[1:]]
    assert len(column_domain_charts) == 16  # Normally 18 without filtering
    assert not find_strings_in_nested_obj(column_domain_charts, exclude_column_names)


def test_volume_data_assistant_plot_include_and_exclude_column_names_raises_error(
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
) -> None:
    with pytest.raises(ValueError) as e:
        bobby_volume_data_assistant_result.plot_metrics(
            include_column_names=["VendorID"], exclude_column_names=["pickup_datetime"]
        )

    assert "either use `include_column_names` or `exclude_column_names`" in str(e.value)


def test_volume_data_assistant_plot_custom_theme_overrides(
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
) -> None:
    font: str = "Comic Sans MS"
    title_color: str = "#FFA500"
    title_font_size: int = 48
    point_size: int = 1000
    y_axis_label_color: str = "red"
    y_axis_label_angle: int = 180
    x_axis_title_color: str = "brown"

    theme: Dict[str, Any] = {
        "font": font,
        "title": {
            "color": title_color,
            "fontSize": title_font_size,
        },
        "point": {"size": point_size},
        "axisY": {
            "labelColor": y_axis_label_color,
            "labelAngle": y_axis_label_angle,
        },
        "axisX": {"titleColor": x_axis_title_color},
    }
    plot_result: PlotResult = (
        bobby_volume_data_assistant_result.plot_expectations_and_metrics(theme=theme)
    )

    # ensure a config has been added to each chart
    assert all(
        not isinstance(chart.config, alt.utils.schemapi.UndefinedType)
        for chart in plot_result.charts
    )

    # ensure the theme elements were updated for each chart
    assert all(chart.config.font == font for chart in plot_result.charts)
    assert all(
        chart.config.title["color"] == title_color for chart in plot_result.charts
    )
    assert all(
        chart.config.title["fontSize"] == title_font_size
        for chart in plot_result.charts
    )
    assert all(chart.config.point["size"] == point_size for chart in plot_result.charts)
    assert all(
        chart.config.axisY["labelColor"] == y_axis_label_color
        for chart in plot_result.charts
    )
    assert all(
        chart.config.axisY["labelAngle"] == y_axis_label_angle
        for chart in plot_result.charts
    )
    assert all(
        chart.config.axisX["titleColor"] == x_axis_title_color
        for chart in plot_result.charts
    )


def test_volume_data_assistant_plot_return_tooltip(
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
) -> None:
    plot_result: PlotResult = (
        bobby_volume_data_assistant_result.plot_expectations_and_metrics()
    )

    expected_tooltip: List[alt.Tooltip] = [
        alt.Tooltip(
            **{
                "field": "column",
                "format": "",
                "title": "Column",
                "type": AltairDataTypes.NOMINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "month",
                "format": "",
                "title": "Month",
                "type": AltairDataTypes.ORDINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "name",
                "format": "",
                "title": "Name",
                "type": AltairDataTypes.ORDINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "year",
                "format": "",
                "title": "Year",
                "type": AltairDataTypes.ORDINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "min_value",
                "format": ",",
                "title": "Min Value",
                "type": AltairDataTypes.QUANTITATIVE.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "max_value",
                "format": ",",
                "title": "Max Value",
                "type": AltairDataTypes.QUANTITATIVE.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "strict_min",
                "format": "",
                "title": "Strict Min",
                "type": AltairDataTypes.NOMINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "strict_max",
                "format": "",
                "title": "Strict Max",
                "type": AltairDataTypes.NOMINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "column_distinct_values_count",
                "format": ",",
                "title": "Column Distinct Values Count",
                "type": AltairDataTypes.QUANTITATIVE.value,
            }
        ),
    ]

    single_column_return_chart: alt.LayerChart = plot_result.charts[2]
    layer_1: alt.Chart = single_column_return_chart.layer[1]
    actual_tooltip: List[alt.Tooltip] = layer_1.encoding.tooltip

    assert actual_tooltip == expected_tooltip


def test_volume_data_assistant_metrics_plot_descriptive_non_sequential_notebook_execution(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    context: DataContext = bobby_columnar_table_multi_batch_deterministic_data_context

    new_cell: str = "data_assistant_result.plot_metrics(sequential=False)"

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


def test_volume_data_assistant_metrics_and_expectations_plot_descriptive_non_sequential_notebook_execution(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    context: DataContext = bobby_columnar_table_multi_batch_deterministic_data_context

    new_cell: str = (
        "data_assistant_result.plot_expectations_and_metrics(sequential=False)"
    )

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_volume_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


def test_volume_data_assistant_plot_non_sequential(
    bobby_volume_data_assistant_result: VolumeDataAssistantResult,
) -> None:
    sequential: bool = False
    plot_metrics_result: PlotResult = bobby_volume_data_assistant_result.plot_metrics(
        sequential=sequential
    )

    assert all([chart.mark == "bar" for chart in plot_metrics_result.charts])

    plot_expectations_result: PlotResult = (
        bobby_volume_data_assistant_result.plot_metrics(sequential=sequential)
    )

    assert all([chart.mark == "bar" for chart in plot_expectations_result.charts])
