"""Sxolar command line interface.

Current commands relate solely to running queries based on config files,
primarily used for generating summaries of arXiv papers and sending emails
with the results.
"""

import argparse
from argparse import Namespace
from typing import List

from sxolar import Query
from sxolar.api.arxiv import SortBy, SortOrder
from sxolar.config import Config
from sxolar.summary import Section
from sxolar.util import gmail


def parse_args(args: List[str] = None) -> Namespace:
    """Parse command line arguments for the sxolar command line interface.

    Args:
        args: List[str], the list of command line arguments

    Returns:
        Namespace, the parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Command line interface for the sxolar package"
    )

    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command")

    # Add the query parser
    add_query_parser(subparsers=subparsers)

    # Add the summary parser
    add_summary_parser(subparsers=subparsers)

    # Parse args
    return parser.parse_args(args)


def add_query_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add a parser for the query command to the main parser."""

    # Parser for the query command
    query_parser = subparsers.add_parser("query", help="Run a query")
    query_parser.add_argument(
        "--value",
        type=str,
        help="Fully formatted query string, e.g. 'au:del maestro'. Optional. If "
        "specified, this will override the query specified in the configuration "
        "or in subsequent arguments.",
        required=False,
    )
    # Argument for list of authors
    query_parser.add_argument(
        "--authors",
        type=str,
        nargs="+",
        help="List of authors to search for. Optional. If specified, this will "
        "override the authors specified in the configuration or in subsequent "
        "arguments.",
        required=False,
    )
    # Argument for list of titles
    query_parser.add_argument(
        "--titles",
        type=str,
        nargs="+",
        help="List of titles to search for. Optional. If specified, this will "
        "override the titles specified in the configuration or in subsequent "
        "arguments.",
        required=False,
    )
    # Argument for list of abstracts
    query_parser.add_argument(
        "--abstracts",
        type=str,
        nargs="+",
        help="List of abstracts to search for. Optional. If specified, this will "
        "override the abstracts specified in the configuration or in subsequent "
        "arguments.",
        required=False,
    )
    # Argument for list of categories
    query_parser.add_argument(
        "--categories",
        type=str,
        nargs="+",
        help="List of categories to search for. Optional. If specified, this will "
        "override the categories specified in the configuration or in subsequent "
        "arguments.",
        required=False,
    )
    # Argument for list of topics
    query_parser.add_argument(
        "--alls",
        type=str,
        nargs="+",
        help="List of alls to search for. Optional. If specified, this will "
        "override the topics specified in the configuration or in subsequent "
        "arguments.",
        required=False,
    )
    # Argument for sort by
    query_parser.add_argument(
        "--sort-by",
        type=str,
        help="Sort by field. Optional. If specified, this will override the sort "
        "field specified in the configuration or in subsequent arguments.",
        required=False,
    )
    # Argument for max results
    query_parser.add_argument(
        "--max-results",
        type=int,
        help="Maximum number of results to return. Optional. If specified, this will "
        "override the maximum number of results specified in the configuration or "
        "in subsequent arguments.",
        required=False,
    )
    # Time filtering arguments
    query_parser.add_argument(
        "--trailing",
        type=int,
        help="Number of units to include in the trailing period. Optional. If "
        "specified, this will override the trailing period specified in the "
        "configuration or in subsequent arguments.",
        required=False,
    )
    # Filter authors argument, default false
    query_parser.add_argument(
        "--filter-authors",
        action="store_true",
        help="Filter the authors based on the query. Optional. If specified, "
             "this will filter search results for exact author matches. When used,"
             "it is required to use the --author argument. Further, "
             "it is strongly advised to increase the max results to get more "
             "accurate results.",
        required=False,
    )
    # Add verbose argument
    query_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose output. Optional.",
        required=False,
    )


def add_summary_parser(subparsers: argparse._SubParsersAction) -> None:
    """Add a parser for the summary command to the main parser."""

    # Parser for the summary command
    summary_parser = subparsers.add_parser("summary", help="Generate a summary")
    summary_parser.add_argument(
        "--name",
        type=str,
        help="Name of the summary to generate. Required.",
        required=True,
    )
    summary_parser.add_argument(
        "--output",
        type=str,
        choices=["print", "email"],
        help="Output file for the summary. Optional. If specified, this will override "
        "the output file specified in the configuration or in subsequent arguments.",
        default="print",
        required=False,
    )
    # Add argument for email from
    summary_parser.add_argument(
        "--email-from",
        type=str,
        help="Email address to send the summary from. Optional. Only required if "
        "sending the summary by email.",
        default="chalkdust@sxolar.org",
        required=False,
    )
    # Add argument for email to
    summary_parser.add_argument(
        "--email-to",
        type=str,
        nargs="+",
        help="Email address to send the summary to. Optional. Only required if "
        "sending the summary by email.",
        required=False,
    )
    # Add argument for email subject
    summary_parser.add_argument(
        "--email-subject",
        type=str,
        help="Email subject for the summary. Optional. Only required if sending the "
        "summary by email.",
        default="ArXiv Summary from sXolar",
        required=False,
    )
    # Add argument for gmail app password
    summary_parser.add_argument(
        "--gmail-app-password",
        type=str,
        help="Gmail app password for sending the email. Optional. Only required if "
        "sending the summary by email.",
        required=False,
    )
    # Add argument for config file
    summary_parser.add_argument(
        "--config",
        type=str,
        help="Path to the configuration file. Optional. If specified, this will "
        "override the configuration file specified in the configuration or in "
        "subsequent arguments.",
        required=False,
    )


def query(
    authors: List[str] = None,
    titles: List[str] = None,
    abstracts: List[str] = None,
    categories: List[str] = None,
    alls: List[str] = None,
    sort_by: SortBy = None,
    sort_order: SortOrder = None,
    max_results: int = None,
    trailing: int = None,
    value: str = None,
    filter_authors: bool = False,
    verbose: bool = False,
) -> None:
    """Run a query based on the command line arguments."""
    # Build query object
    if value is not None:
        query = Query(value=value)
    else:
        query = Query.from_combo(
            authors=authors,
            titles=titles,
            abstracts=abstracts,
            categories=categories,
            alls=alls,
        )

        if filter_authors and authors:
            if verbose:
                print(f"Will filter results based on authors: {authors}")
            query.filter_authors = authors

    if verbose:
        print(f"Query: {query.value}")

    # Build optional kwargs
    kwargs = {}
    for k, v in {
        "sort_by": sort_by,
        "sort_order": sort_order,
        "max_results": max_results,
        "trailing": trailing,
    }.items():
        if v is not None:
            kwargs[k] = v

    section = Section(
        name="Query Results",
        query=query,
        **kwargs,
    )

    # Run the query
    section.refresh()

    # Print the results
    print(section.to_text())


def summary(
    config_path: str,
    name: str,
    output: str = "print",
    email_from: str = "chalkdust@sxolar.org",
    email_to: List[str] = None,
    email_subject: str = "ArXiv Summary from sXolar",
    gmail_app_password: str = None,
) -> None:
    """Generate a summary based on the command line arguments."""
    # Load config
    try:
        config = Config.load(config_path)
    except Exception as e:
        raise ValueError(f"Error loading configuration file: {e}") from e

    # Get the summary associated to the name
    summary = config.summaries.get(name, None)
    if summary is None:
        raise ValueError(
            f"Summary not found: {name}, options are {list(config.summaries.keys())}"
        )

    # Refresh the summary
    summary.refresh()

    # Print the summary if that is the output
    if output == "print":
        print(summary.to_text())

    # Send the summary by email if that is the output
    elif output == "email":
        if email_to is None:
            raise ValueError("Email to address must be specified for email output")
        if gmail_app_password is None:
            # Check env var
            if gmail.EMAIL_APP_PASSWORD is None:
                raise ValueError("Gmail app password must be specified for email "
                                 "output, can be set as an environment variable "
                                 "$SXOLAR_EMAIL_APP_PASSWORD or specify it as the")
        body = summary.to_html()
        # Send email
        gmail.send_email(
            subject=email_subject,
            to=email_to,
            body=body,
            from_email=email_from,
            app_password=gmail_app_password,
            is_plain=False,
        )

    # Invalid output
    else:
        raise ValueError(f"Invalid output: {output}, options are print, email")


def main():
    """Main function for the sxolar command line interface."""
    args = parse_args()

    # Dispatch for different commands
    # Query command
    if args.command == "query":
        # Convert the sort by argument to a SortBy enum
        if args.sort_by is None:
            sort_by = None
        else:
            sort_by = {
                "relevance": SortBy.Relevance,
                "lastUpdatedDate": SortBy.LastUpdatedDate,
                "submittedDate": SortBy.SubmittedDate,
            }.get(args.sort_by, None)
            if sort_by is None:
                raise ValueError(
                    f"Invalid sort by argument: {args.sort_by}, options "
                    f"are relevance, lastUpdatedDate, submittedDate"
                )

        query(
            authors=args.authors,
            titles=args.titles,
            abstracts=args.abstracts,
            categories=args.categories,
            alls=args.alls,
            sort_by=sort_by,
            max_results=args.max_results,
            trailing=args.trailing,
            value=args.value,
            filter_authors=args.filter_authors,
            verbose=args.verbose,
        )

    # Summary command
    elif args.command == "summary":
        summary(
            config_path=args.config,
            name=args.name,
            output=args.output,
            email_from=args.email_from,
            email_to=args.email_to,
            email_subject=args.email_subject,
            gmail_app_password=args.gmail_app_password,
        )

    # Invalid command
    else:
        raise ValueError(f"Invalid command: {args.command}")


if __name__ == "__main__":
    main()
