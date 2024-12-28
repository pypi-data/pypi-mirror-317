import json

import click
import pyperclip

from .utils.adapters.data_warehouses.bigquery import BigQueryAdapter
from .utils.adapters.data_warehouses.snowflake import SnowflakeAdapter
from .utils.helpers import (
    init_connectors,
    package_command_output,
    print_packaged_command_output,
    run_and_capture,
)


def get_orchestrator_data(orchestrator_connector, asset):
    # Split the asset key into a list of strings
    asset_key = asset.split("/")

    # Get data
    query = f"""
    query AssetByKey {{
      assetOrError(assetKey: {{path: {json.dumps(asset_key)}}}) {{
        __typename
        ... on Asset {{
          definition {{
            description
            computeKind
            autoMaterializePolicy{{
              policyType
            }}
            freshnessPolicy{{
              maximumLagMinutes
              cronSchedule
            }}
            isPartitioned
            dependedByKeys{{
              path
            }}
            dependencyKeys{{
              path
            }}
          }}
          assetMaterializations(limit: 1){{
            timestamp
            metadataEntries{{
              __typename
              ... on FloatMetadataEntry{{
                label
                description
                floatValue
              }}
              ... on IntMetadataEntry{{
                label
                description
                intValue
              }}
              ... on JsonMetadataEntry{{
                label
                description
                jsonString
              }}
              ... on BoolMetadataEntry{{
                label
                description
                boolValue
              }}
              ... on MarkdownMetadataEntry{{
                label
                description
                mdStr
              }}
              ... on PathMetadataEntry{{
                label
                description
                path
              }}
              ... on NotebookMetadataEntry{{
                label
                description
                path
              }}
              ... on PythonArtifactMetadataEntry{{
                label
                description
                module
                name
              }}
              ... on TextMetadataEntry{{
                label
                description
                text
              }}
              ... on UrlMetadataEntry{{
                label
                description
                url
              }}
              ... on PipelineRunMetadataEntry{{
                label
                description
                runId
              }}
              ... on AssetMetadataEntry{{
                label
                description
                assetKey{{
                  path
                }}
              }}
              ... on NullMetadataEntry{{
                label
                description
              }}
            }}
          }}
        }}
        ... on AssetNotFoundError {{
          message
        }}
      }}
    }}
    """

    result = orchestrator_connector.execute(query)

    # Initialize the return dictionary with some default values
    data = {
        "description": None,
        "computeKind": None,
        "policyType": None,
        "maximumLagMinutes": None,
        "cronSchedule": None,
        "isPartitioned": None,
        "dependedByKeys": None,
        "dependencyKeys": None,
        "metadataEntries": {},
    }

    # Check for assetOrError and whether it's an Asset
    if (
        "data" in result
        and "assetOrError" in result["data"]
        and result["data"]["assetOrError"]["__typename"] == "Asset"
    ):
        asset_info = result["data"]["assetOrError"]

        # Get Definition attributes
        if "definition" in asset_info:
            definition = asset_info["definition"]
            data["description"] = definition.get("description")
            data["computeKind"] = definition.get("computeKind")

            auto_materialize_policy = definition.get("autoMaterializePolicy")
            if auto_materialize_policy is not None:
                data["policyType"] = auto_materialize_policy.get("policyType")

            freshness_policy = definition.get("freshnessPolicy")
            if freshness_policy is not None:
                data["maximumLagMinutes"] = freshness_policy.get("maximumLagMinutes")
                data["cronSchedule"] = freshness_policy.get("cronSchedule")

            data["isPartitioned"] = definition.get("isPartitioned")
            data["dependedByKeys"] = [
                d.get("path") for d in definition.get("dependedByKeys", [])
            ]
            data["dependencyKeys"] = [
                d.get("path") for d in definition.get("dependencyKeys", [])
            ]

        # Get metadataEntries attributes
        if (
            "assetMaterializations" in asset_info
            and asset_info["assetMaterializations"]
        ):
            first_materialization = asset_info["assetMaterializations"][0]
            metadata_entries = first_materialization.get("metadataEntries", [])

            for entry in metadata_entries:
                label = entry.get("label")
                for typename, value in entry.items():
                    if (
                        typename.endswith("Value")
                        or typename.endswith("String")
                        or typename == "path"
                        or typename == "module"
                        or typename == "name"
                        or typename == "url"
                        or typename == "runId"
                    ):
                        data["metadataEntries"][label] = value

    return data


def get_data_warehouse_data(data_warehouse_connector, asset):
    asset = asset.lower()  # Make sure the asset name is lower case
    dataset_name = asset.split("/")[0]  # Get the last section after splitting by '/'
    asset_name = asset.split("/")[-1]  # Get the last section after splitting by '/'

    sql = None
    if isinstance(data_warehouse_connector, SnowflakeAdapter):
        sql = f"""select
                lower(table_schema) as table_schema,
                lower(table_type) as table_type,
                created,
                last_altered

            from information_schema.tables 
            where lower(table_name) = '{asset_name}'
            """
    elif isinstance(data_warehouse_connector, BigQueryAdapter):
        sql = f"""select
                table_schema,
                table_type,
                creation_time as created,
                null as last_altered

            from `{data_warehouse_connector.config['project']}.{dataset_name}.INFORMATION_SCHEMA.TABLES`
            WHERE LOWER(table_name) = '{asset_name}'
        """

    result, description = data_warehouse_connector.execute(sql)
    data_warehouse_connector.close()

    # Debug prints
    if result is not None and isinstance(result, list) and isinstance(result[0], dict):
        result_dict = result[0]
        return {
            "table_schema": result_dict.get("table_schema"),
            "table_type": result_dict.get("table_type"),
            "created": result_dict.get("created"),
            "last_altered": result_dict.get("last_altered"),
        }


def show_asset(
    asset, orchestrator=None, io_manager=None, data_warehouse=None, configs_dir=None
):
    orchestrator_connector, io_manager_connector, data_warehouse_connector = (
        init_connectors(orchestrator, io_manager, data_warehouse, configs_dir)
    )

    orchestrator_data = (
        get_orchestrator_data(orchestrator_connector, asset)
        if orchestrator_connector
        else None
    )
    data_warehouse_data = (
        get_data_warehouse_data(data_warehouse_connector, asset)
        if data_warehouse_connector
        else None
    )

    data = {
        "Orchestrator Attributes": orchestrator_data,
        "Data Warehouse Attributes": data_warehouse_data,
    }

    # Package and output asset information
    packaged_command_output = package_command_output("show", data)

    return packaged_command_output


@click.command()
@click.argument("asset", required=True)
@click.option(
    "--orchestrator", default=None, help="Orchestrator service provider to use"
)
@click.option("--io_manager", default=None, help="IO manager service provider to use")
@click.option(
    "--data-warehouse", default=None, help="Data warehouse service provider to use"
)
@click.option(
    "--output",
    default="terminal",
    help="Destination for command output. Options include `terminal` (default) for standard output, `json` to format output as JSON, or `copy` to copy the output to the clipboard.",
)
@click.option(
    "--configs-dir",
    default=None,
    help="Which directory to look in for the connectors.yml file. If not set, DAMN will look in the `~/.damn/` directory",
)
def show(asset, orchestrator, io_manager, data_warehouse, output, configs_dir):
    """Show details for a specific asset"""
    packaged_command_output = show_asset(
        asset, orchestrator, io_manager, data_warehouse, configs_dir
    )

    if output == "json":
        print(packaged_command_output)
    elif output == "copy":
        print_output = run_and_capture(
            print_packaged_command_output, packaged_command_output
        )
        markdown_output = print_output.replace("\x1b[36m- ", "- ").replace(
            "\x1b[0m", ""
        )  # Removing the color codes
        pyperclip.copy(markdown_output)
    else:
        print_packaged_command_output(packaged_command_output)

