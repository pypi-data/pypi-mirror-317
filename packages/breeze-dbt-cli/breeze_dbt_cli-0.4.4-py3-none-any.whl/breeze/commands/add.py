# breeze/commands/add.py

import typer
from typing import List, Optional
from breeze.models.model import add_test_to_model
from breeze.models.source import add_test_to_source

add_app = typer.Typer(
    help="""
Usage: breeze add [OPTIONS] COMMAND [ARGS]...

  Add commands to apply tests to models or sources.

  Use these commands to add dbt tests to models or sources, either at the
  model level or to specific columns.

Options:
  --help  Show this message and exit.

Commands:
  test  Add one or more tests to a model or source.
"""
)


@add_app.command()
def test(
    test_names: List[str] = typer.Argument(
        ..., help="The name(s) of the test(s) to add."
    ),
    model: Optional[str] = typer.Option(
        None, "--model", "-m", help="Model name to add the test(s) to."
    ),
    seed: Optional[str] = typer.Option(
        None, "--seed", "-e", help="Seed name to add the test(s) to."
    ),
    snapshot: Optional[str] = typer.Option(
        None, "--snapshot", "-n", help="Snapshot name to add the test(s) to."
    ),
    source: Optional[str] = typer.Option(
        None, "--source", "-s", help="Source name to add the test(s) to."
    ),
    columns: Optional[str] = typer.Option(
        None,
        "--columns",
        "-c",
        help="Comma-separated column names to add the test(s) to.",
    ),
):
    """
    Add one or more tests to a model or source.

    This command adds one or more tests to a specified model or source. If columns are provided, the tests are added to those columns.
    If no columns are provided, the tests are added at the model or source level.

    You must specify either a `--model`, `--seed`,`--snapshot`, or a `--source`, but not more than one.

    Options:
      - `test_names`: One or more test names to add (e.g., `not_null`, `unique`).
      - `--model`, `-m`: The model name to add the test(s) to.
      - `--seed`, `-e`: The seed name to add the test(s) to.
      - `--snapshot`, `-n`: The source name to add the test(s) to.
      - `--source`, `-s`: The source name to add the test(s) to.
      - `--columns`, `-c`: Comma-separated column names to add the test(s) to.

    Examples:
      - Add `unique` tests to `customer_id` and `email` columns in the `customers` model:

        \b
        breeze add test unique --model customers --columns "customer_id, email"

      - Add `not_null` and `accepted_values` tests to the `status_code` column in the `status` source:

        \b
        breeze add test not_null accepted_values --source status --columns status_code
    """
    # Ensure that either model or source is provided, but not both
    if (model is None and source is None and seed is None and snapshot is None) or (model and source and seed and snapshot):
        typer.echo("❌  Please provide either --model, --seed, --snapshot, or --source, but not more than one.")
        raise typer.Exit(code=1)

    # Parse the comma-separated columns into a list
    if columns:
        columns_list = [col.strip() for col in columns.split(",")]
    else:
        columns_list = None

    try:
        if model:
            resource_type = "model"
            target_name = model
            success = add_test_to_model(test_names, model, resource_type, columns_list)
        elif seed:
            resource_type = "seed"
            target_name = seed
            success = add_test_to_model(test_names, seed, resource_type, columns_list)
        elif snapshot:
            resource_type = "snapshot"
            target_name = snapshot
            success = add_test_to_model(test_names, snapshot, resource_type, columns_list)
        elif source:
            resource_type = "source"
            target_name = source
            success = add_test_to_source(test_names, source, columns_list)
        if success:
            tests_added = ", ".join(test_names)
            typer.echo(
                f"✅  Successfully added test(s) '{tests_added}' to {resource_type} '{target_name}'."
            )
        else:
            typer.echo(f"No changes made. Test(s) may already exist.")
    except Exception as e:
        typer.echo(f"❌  Failed to add test(s) to {target_name}: {e}")
