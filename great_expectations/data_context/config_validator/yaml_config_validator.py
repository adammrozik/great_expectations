from __future__ import annotations

import os
import traceback
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Tuple, Union, cast

from ruamel.yaml.comments import CommentedMap

from great_expectations.checkpoint import Checkpoint, SimpleCheckpoint
from great_expectations.core.usage_statistics.anonymizers.anonymizer import Anonymizer
from great_expectations.core.usage_statistics.anonymizers.datasource_anonymizer import (
    DatasourceAnonymizer,
)
from great_expectations.core.usage_statistics.usage_statistics import (
    UsageStatisticsHandler,
)
from great_expectations.core.yaml_handler import YAMLHandler
from great_expectations.data_context.store import Store
from great_expectations.data_context.types.base import (
    CheckpointConfig,
    DataContextConfig,
    datasourceConfigSchema,
)
from great_expectations.data_context.util import (
    instantiate_class_from_config,
    substitute_all_config_variables,
)
from great_expectations.datasource import DataConnector, Datasource
from great_expectations.rule_based_profiler import RuleBasedProfiler
from great_expectations.rule_based_profiler.config import RuleBasedProfilerConfig
from great_expectations.util import filter_properties_dict

if TYPE_CHECKING:
    from great_expectations.data_context import AbstractDataContext

yaml = YAMLHandler()


class YamlConfigValidator:
    TEST_YAML_CONFIG_SUPPORTED_STORE_TYPES = [
        "ExpectationsStore",
        "ValidationsStore",
        "HtmlSiteStore",
        "EvaluationParameterStore",
        "MetricStore",
        "SqlAlchemyQueryStore",
        "CheckpointStore",
        "ProfilerStore",
    ]
    TEST_YAML_CONFIG_SUPPORTED_DATASOURCE_TYPES = [
        "Datasource",
        "SimpleSqlalchemyDatasource",
    ]
    TEST_YAML_CONFIG_SUPPORTED_DATA_CONNECTOR_TYPES = [
        "InferredAssetFilesystemDataConnector",
        "ConfiguredAssetFilesystemDataConnector",
        "InferredAssetS3DataConnector",
        "ConfiguredAssetS3DataConnector",
        "InferredAssetAzureDataConnector",
        "ConfiguredAssetAzureDataConnector",
        "InferredAssetGCSDataConnector",
        "ConfiguredAssetGCSDataConnector",
        "InferredAssetSqlDataConnector",
        "ConfiguredAssetSqlDataConnector",
    ]
    TEST_YAML_CONFIG_SUPPORTED_CHECKPOINT_TYPES = [
        "Checkpoint",
        "SimpleCheckpoint",
    ]
    TEST_YAML_CONFIG_SUPPORTED_PROFILER_TYPES = [
        "RuleBasedProfiler",
    ]
    ALL_TEST_YAML_CONFIG_DIAGNOSTIC_INFO_TYPES = [
        "__substitution_error__",
        "__yaml_parse_error__",
        "__custom_subclass_not_core_ge__",
        "__class_name_not_provided__",
    ]
    ALL_TEST_YAML_CONFIG_SUPPORTED_TYPES = (
        TEST_YAML_CONFIG_SUPPORTED_STORE_TYPES
        + TEST_YAML_CONFIG_SUPPORTED_DATASOURCE_TYPES
        + TEST_YAML_CONFIG_SUPPORTED_DATA_CONNECTOR_TYPES
        + TEST_YAML_CONFIG_SUPPORTED_CHECKPOINT_TYPES
        + TEST_YAML_CONFIG_SUPPORTED_PROFILER_TYPES
    )

    def __init__(
        self,
        usage_stats_handler: UsageStatisticsHandler,
        runtime_environment: Dict,
        config_variables: Dict,
        data_context: AbstractDataContext,
    ):
        self._usage_stats_handler = usage_stats_handler
        self._runtime_environment = runtime_environment
        self._config_variables = config_variables
        self._data_context = data_context

    @property
    def usage_stats_handler(self):
        return self._usage_stats_handler

    @property
    def runtime_environment(self):
        return self._runtime_environment

    @property
    def config_variables(self):
        return self._config_variables

    @property

    # def synchronize_config(self, config_variables: Dict):
    #     """Synchronize configuration with caller."""
    #     self._config_variables = config_variables
    #
    #
    # def synchronize_then_test_yaml_config(
    #     self,
    #
    #     yaml_config: str,
    #     name: Optional[str] = None,
    #     class_name: Optional[str] = None,
    #     runtime_environment: Optional[dict] = None,
    #     pretty_print: bool = True,
    #     return_mode: Union[
    #         Literal["instantiated_class"], Literal["report_object"]
    #     ] = "instantiated_class",
    #     shorten_tracebacks: bool = False,
    # ):
    #     self.synchronize_config()
    #     self._test_yaml_config()
    #     raise NotImplementedError

    def test_yaml_config(
        self,
        yaml_config: str,
        name: Optional[str] = None,
        class_name: Optional[str] = None,
        runtime_environment: Optional[dict] = None,
        pretty_print: bool = True,
        return_mode: Union[
            Literal["instantiated_class"], Literal["report_object"]
        ] = "instantiated_class",
        shorten_tracebacks: bool = False,
    ):
        """Convenience method for testing yaml configs

        test_yaml_config is a convenience method for configuring the moving
        parts of a Great Expectations deployment. It allows you to quickly
        test out configs for system components, especially Datasources,
        Checkpoints, and Stores.

        For many deployments of Great Expectations, these components (plus
        Expectations) are the only ones you'll need.

        test_yaml_config is mainly intended for use within notebooks and tests.

        --Public API--

        --Documentation--
            https://docs.greatexpectations.io/docs/terms/data_context
            https://docs.greatexpectations.io/docs/guides/validation/checkpoints/how_to_configure_a_new_checkpoint_using_test_yaml_config

        Args:
            yaml_config: A string containing the yaml config to be tested
            name: (Optional) A string containing the name of the component to instantiate
            pretty_print: Determines whether to print human-readable output
            return_mode: Determines what type of object test_yaml_config will return.
                Valid modes are "instantiated_class" and "report_object"
            shorten_tracebacks:If true, catch any errors during instantiation and print only the
                last element of the traceback stack. This can be helpful for
                rapid iteration on configs in a notebook, because it can remove
                the need to scroll up and down a lot.

        Returns:
            The instantiated component (e.g. a Datasource)
            OR
            a json object containing metadata from the component's self_check method.
            The returned object is determined by return_mode.
        """
        if return_mode not in ["instantiated_class", "report_object"]:
            raise ValueError(f"Unknown return_mode: {return_mode}.")

        if runtime_environment is None:
            runtime_environment = {}

        runtime_environment = {
            **runtime_environment,
            **self.runtime_environment,
        }

        usage_stats_event_name: str = "data_context.test_yaml_config"

        config = self._test_yaml_config_prepare_config(
            yaml_config, runtime_environment, usage_stats_event_name
        )

        if "class_name" in config:
            class_name = config["class_name"]

        instantiated_class: Any = None
        usage_stats_event_payload: Dict[str, Union[str, List[str]]] = {}

        if pretty_print:
            print("Attempting to instantiate class from config...")
        try:
            if class_name in self.TEST_YAML_CONFIG_SUPPORTED_STORE_TYPES:
                (
                    instantiated_class,
                    usage_stats_event_payload,
                ) = self._test_instantiation_of_store_from_yaml_config(
                    name, class_name, config
                )
            elif class_name in self.TEST_YAML_CONFIG_SUPPORTED_DATASOURCE_TYPES:
                (
                    instantiated_class,
                    usage_stats_event_payload,
                ) = self._test_instantiation_of_datasource_from_yaml_config(
                    name, class_name, config
                )
            elif class_name in self.TEST_YAML_CONFIG_SUPPORTED_CHECKPOINT_TYPES:
                (
                    instantiated_class,
                    usage_stats_event_payload,
                ) = self._test_instantiation_of_checkpoint_from_yaml_config(
                    name, class_name, config
                )
            elif class_name in self.TEST_YAML_CONFIG_SUPPORTED_DATA_CONNECTOR_TYPES:
                (
                    instantiated_class,
                    usage_stats_event_payload,
                ) = self._test_instantiation_of_data_connector_from_yaml_config(
                    name, class_name, config, runtime_environment
                )
            elif class_name in self.TEST_YAML_CONFIG_SUPPORTED_PROFILER_TYPES:
                (
                    instantiated_class,
                    usage_stats_event_payload,
                ) = self._test_instantiation_of_profiler_from_yaml_config(
                    name, class_name, config
                )
            else:
                (
                    instantiated_class,
                    usage_stats_event_payload,
                ) = self._test_instantiation_of_misc_class_from_yaml_config(
                    name, config, runtime_environment, usage_stats_event_payload
                )

            self._usage_stats_handler.send_usage_message(
                event=usage_stats_event_name,
                event_payload=usage_stats_event_payload,
                success=True,
            )
            if pretty_print:
                print(
                    f"\tSuccessfully instantiated {instantiated_class.__class__.__name__}\n"
                )

            report_object: dict = instantiated_class.self_check(
                pretty_print=pretty_print
            )

            if return_mode == "instantiated_class":
                return instantiated_class

            return report_object

        except Exception as e:
            if class_name is None:
                usage_stats_event_payload[
                    "diagnostic_info"
                ] = usage_stats_event_payload.get("diagnostic_info", []) + [
                    "__class_name_not_provided__"
                ]
            elif (
                usage_stats_event_payload.get("parent_class") is None
                and class_name in self.ALL_TEST_YAML_CONFIG_SUPPORTED_TYPES
            ):
                # add parent_class if it doesn't exist and class_name is one of our supported core GE types
                usage_stats_event_payload["parent_class"] = class_name
            self._usage_stats_handler.send_usage_message(
                event=usage_stats_event_name,
                event_payload=usage_stats_event_payload,
                success=False,
            )
            if shorten_tracebacks:
                traceback.print_exc(limit=1)
            else:
                raise e

    def _test_yaml_config_prepare_config(
        self, yaml_config: str, runtime_environment: dict, usage_stats_event_name: str
    ) -> CommentedMap:
        """
        Performs variable substitution and conversion from YAML to CommentedMap.
        See `test_yaml_config` for more details.
        """
        try:
            substituted_config_variables: Union[
                DataContextConfig, dict
            ] = substitute_all_config_variables(
                self.config_variables,
                dict(os.environ),
            )

            substitutions: dict = {
                **substituted_config_variables,
                **dict(os.environ),
                **runtime_environment,
            }

            config_str_with_substituted_variables: Union[
                DataContextConfig, dict
            ] = substitute_all_config_variables(
                yaml_config,
                substitutions,
            )
        except Exception as e:
            usage_stats_event_payload: dict = {
                "diagnostic_info": ["__substitution_error__"],
            }
            self._usage_stats_handler.send_usage_message(
                event=usage_stats_event_name,
                event_payload=usage_stats_event_payload,
                success=False,
            )
            raise e

        try:
            config: CommentedMap = yaml.load(config_str_with_substituted_variables)
            return config

        except Exception as e:
            usage_stats_event_payload: dict = {
                "diagnostic_info": ["__yaml_parse_error__"],
            }
            self._usage_stats_handler.send_usage_message(
                event=usage_stats_event_name,
                event_payload=usage_stats_event_payload,
                success=False,
            )
            raise e

    def _test_instantiation_of_store_from_yaml_config(
        self, name: Optional[str], class_name: str, config: CommentedMap
    ) -> Tuple[Store, dict]:
        """
        Helper to create store instance and update usage stats payload.
        See `test_yaml_config` for more details.
        """
        print(f"\tInstantiating as a Store, since class_name is {class_name}")
        store_name: str = name or config.get("name") or "my_temp_store"
        instantiated_class = cast(
            Store,
            self._data_context._build_store_from_config(
                store_name=store_name,
                store_config=config,
            ),
        )
        store_name = instantiated_class.store_name or store_name
        self._data_context.config["stores"][store_name] = config

        anonymizer = Anonymizer(self.data_context_id)
        usage_stats_event_payload = anonymizer.anonymize(
            store_name=store_name, store_obj=instantiated_class
        )
        return instantiated_class, usage_stats_event_payload

    def _test_instantiation_of_datasource_from_yaml_config(
        self, name: Optional[str], class_name: str, config: CommentedMap
    ) -> Tuple[Datasource, dict]:
        """
        Helper to create datasource instance and update usage stats payload.
        See `test_yaml_config` for more details.
        """
        print(f"\tInstantiating as a Datasource, since class_name is {class_name}")
        datasource_name: str = name or config.get("name") or "my_temp_datasource"
        instantiated_class = cast(
            Datasource,
            self._data_context._instantiate_datasource_from_config_and_update_project_config(
                name=datasource_name,
                config=config,
                initialize=True,
            ),
        )

        anonymizer = Anonymizer(self._data_context.data_context_id)

        if class_name == "SimpleSqlalchemyDatasource":
            # Use the raw config here, defaults will be added in the anonymizer
            usage_stats_event_payload = anonymizer.anonymize(
                obj=instantiated_class, name=datasource_name, config=config
            )
        else:
            # Roundtrip through schema validation to remove any illegal fields add/or restore any missing fields.
            datasource_config = datasourceConfigSchema.load(instantiated_class.config)
            full_datasource_config = datasourceConfigSchema.dump(datasource_config)
            usage_stats_event_payload = anonymizer.anonymize(
                obj=instantiated_class,
                name=datasource_name,
                config=full_datasource_config,
            )
        return instantiated_class, usage_stats_event_payload

    def _test_instantiation_of_checkpoint_from_yaml_config(
        self, name: Optional[str], class_name: str, config: CommentedMap
    ) -> Tuple[Checkpoint, dict]:
        """
        Helper to create checkpoint instance and update usage stats payload.
        See `test_yaml_config` for more details.
        """
        print(f"\tInstantiating as a {class_name}, since class_name is {class_name}")

        checkpoint_name: str = name or config.get("name") or "my_temp_checkpoint"

        checkpoint_config: Union[CheckpointConfig, dict]

        checkpoint_config = CheckpointConfig.from_commented_map(commented_map=config)
        checkpoint_config = checkpoint_config.to_json_dict()
        checkpoint_config.update({"name": checkpoint_name})

        checkpoint_class_args: dict = filter_properties_dict(
            properties=checkpoint_config,
            delete_fields={"class_name", "module_name"},
            clean_falsy=True,
        )

        if class_name == "Checkpoint":
            instantiated_class = Checkpoint(data_context=self, **checkpoint_class_args)
        elif class_name == "SimpleCheckpoint":
            instantiated_class = SimpleCheckpoint(
                data_context=self, **checkpoint_class_args
            )
        else:
            raise ValueError(f'Unknown Checkpoint class_name: "{class_name}".')

        anonymizer: Anonymizer = Anonymizer(self._data_context.data_context_id)

        usage_stats_event_payload = anonymizer.anonymize(
            obj=instantiated_class, name=checkpoint_name, config=checkpoint_config
        )

        return instantiated_class, usage_stats_event_payload

    def _test_instantiation_of_data_connector_from_yaml_config(
        self,
        name: Optional[str],
        class_name: str,
        config: CommentedMap,
        runtime_environment: dict,
    ) -> Tuple[DataConnector, dict]:
        """
        Helper to create data connector instance and update usage stats payload.
        See `test_yaml_config` for more details.
        """
        print(f"\tInstantiating as a DataConnector, since class_name is {class_name}")
        data_connector_name: str = (
            name or config.get("name") or "my_temp_data_connector"
        )
        instantiated_class = instantiate_class_from_config(
            config=config,
            runtime_environment={
                **runtime_environment,
                **{
                    "root_directory": self._data_context.root_directory,
                },
            },
            config_defaults={},
        )

        anonymizer = Anonymizer(self._data_context.data_context_id)

        usage_stats_event_payload = anonymizer.anonymize(
            obj=instantiated_class, name=data_connector_name, config=config
        )
        return instantiated_class, usage_stats_event_payload

    def _test_instantiation_of_profiler_from_yaml_config(
        self, name: Optional[str], class_name: str, config: CommentedMap
    ) -> Tuple[RuleBasedProfiler, dict]:
        """
        Helper to create profiler instance and update usage stats payload.
        See `test_yaml_config` for more details.
        """
        print(f"\tInstantiating as a {class_name}, since class_name is {class_name}")

        profiler_name: str = name or config.get("name") or "my_temp_profiler"

        profiler_config: Union[
            RuleBasedProfilerConfig, dict
        ] = RuleBasedProfilerConfig.from_commented_map(commented_map=config)
        profiler_config = profiler_config.to_json_dict()
        profiler_config.update({"name": profiler_name})

        instantiated_class = instantiate_class_from_config(
            config=profiler_config,
            runtime_environment={"data_context": self},
            config_defaults={
                "module_name": "great_expectations.rule_based_profiler",
                "class_name": "RuleBasedProfiler",
            },
        )

        anonymizer: Anonymizer = Anonymizer(self._data_context.data_context_id)

        usage_stats_event_payload: dict = anonymizer.anonymize(
            obj=instantiated_class, name=profiler_name, config=profiler_config
        )

        return instantiated_class, usage_stats_event_payload

    def _test_instantiation_of_misc_class_from_yaml_config(
        self,
        name: Optional[str],
        config: CommentedMap,
        runtime_environment: dict,
        usage_stats_event_payload: dict,
    ) -> Tuple[Any, dict]:
        """
        Catch-all to cover all classes not covered in other `_test_instantiation` methods.
        Attempts to match config to the relevant class/parent and update usage stats payload.
        See `test_yaml_config` for more details.
        """
        print(
            "\tNo matching class found. Attempting to instantiate class from the raw config..."
        )
        instantiated_class = instantiate_class_from_config(
            config=config,
            runtime_environment={
                **runtime_environment,
                **{
                    "root_directory": self._data_context.root_directory,
                },
            },
            config_defaults={},
        )

        # If a subclass of a supported type, find the parent class and anonymize
        anonymizer: Anonymizer = Anonymizer(self._data_context.data_context_id)

        parent_class_from_object = anonymizer.get_parent_class(
            object_=instantiated_class
        )
        parent_class_from_config = anonymizer.get_parent_class(object_config=config)

        if parent_class_from_object is not None and parent_class_from_object.endswith(
            "Store"
        ):
            store_name: str = name or config.get("name") or "my_temp_store"
            store_name = instantiated_class.store_name or store_name
            usage_stats_event_payload = anonymizer.anonymize(
                store_name=store_name, store_obj=instantiated_class
            )
        elif parent_class_from_config is not None and parent_class_from_config.endswith(
            "Datasource"
        ):
            datasource_name: str = name or config.get("name") or "my_temp_datasource"
            if DatasourceAnonymizer.get_parent_class_v3_api(config=config):
                # Roundtrip through schema validation to remove any illegal fields add/or restore any missing fields.
                datasource_config = datasourceConfigSchema.load(
                    instantiated_class.config
                )
                full_datasource_config = datasourceConfigSchema.dump(datasource_config)
            else:
                # for v2 api
                full_datasource_config = config
            if parent_class_from_config == "SimpleSqlalchemyDatasource":
                # Use the raw config here, defaults will be added in the anonymizer
                usage_stats_event_payload = anonymizer.anonymize(
                    obj=instantiated_class, name=datasource_name, config=config
                )
            else:
                usage_stats_event_payload = anonymizer.anonymize(
                    obj=instantiated_class,
                    name=datasource_name,
                    config=full_datasource_config,
                )

        elif parent_class_from_config is not None and parent_class_from_config.endswith(
            "Checkpoint"
        ):
            checkpoint_name: str = name or config.get("name") or "my_temp_checkpoint"
            # Roundtrip through schema validation to remove any illegal fields add/or restore any missing fields.
            checkpoint_config: Union[CheckpointConfig, dict]
            checkpoint_config = CheckpointConfig.from_commented_map(
                commented_map=config
            )
            checkpoint_config = checkpoint_config.to_json_dict()
            checkpoint_config.update({"name": checkpoint_name})
            usage_stats_event_payload = anonymizer.anonymize(
                obj=checkpoint_config, name=checkpoint_name, config=checkpoint_config
            )

        elif parent_class_from_config is not None and parent_class_from_config.endswith(
            "DataConnector"
        ):
            data_connector_name: str = (
                name or config.get("name") or "my_temp_data_connector"
            )
            usage_stats_event_payload = anonymizer.anonymize(
                obj=instantiated_class, name=data_connector_name, config=config
            )

        else:
            # If class_name is not a supported type or subclass of a supported type,
            # mark it as custom with no additional information since we can't anonymize
            usage_stats_event_payload[
                "diagnostic_info"
            ] = usage_stats_event_payload.get("diagnostic_info", []) + [
                "__custom_subclass_not_core_ge__"
            ]

        return instantiated_class, usage_stats_event_payload
