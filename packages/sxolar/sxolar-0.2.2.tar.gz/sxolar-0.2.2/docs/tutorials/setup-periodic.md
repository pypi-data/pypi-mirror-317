# Tutorial: Setup Periodic Search

This tutorial demonstrates how to set up periodic searches using the `sxolar` library. Periodic searches allow users to
automatically retrieve search results at regular intervals and receive email summaries of the results. This feature is
useful for staying up-to-date with the latest research in a specific field or topic.

!!! note "Prerequisites"

    Before proceeding with this tutorial, make sure you have a [GitHub](https://github.com) account, have set up email 
    access using the instructions in the [Setup Email Access](setup-email.md) tutorial. Further, this tutorial assumes 
    that you have a configuration file with the desired search queries. If you do not have a configuration file, refer 
    to the [Simple Summary](simple-summary.md) or [Config Files](../user-guide/config-files.md) tutorials for more 
    information.

## Create New GitHub Repository

To set up periodic searches, we will create a new GitHub repository to store the configuration file and other related
files. We will use GitHub Actions to trigger the periodic searches and send email summaries of the search results
for free.

1. Go to [GitHub](https://github.com) and log in to your account.
2. Click on the "+" icon in the top right corner and select "New repository".
3. Enter a name for the repository, e.g., `sxolar-searches`.
4. Add a description if desired.
5. Choose whether the repository should be public or private.
6. Click on "Create repository".
7. Clone the repository to your local machine using the following command:

```bash
git clone  
```

### Shortcut: Use Template Repository

If you prefer, you can use the [sxolar-template-run](https://github.com/JWKennington/sxolar-template-run)
repository as a template to set up periodic searches. This repository contains a pre-configured GitHub Actions
workflow that triggers periodic searches and sends email summaries of the search results. You can customize the
configuration file and other settings as needed.

## Add Configuration File

Next, we will add the configuration file with the desired search queries to the GitHub repository. The configuration
file should be in the YAML format and contain the search queries that you want to run periodically.

Example configuration file (`config.yaml`):

```yaml
GWaves:
  - name: "LIGO / VIRGO Papers Past Month"
    authors: [
      "The LIGO Scientific Collaboration",
      "The Virgo Collaboration",
    ]
    filter_authors: True
    # Set the maximum number of results to 1000 to ensure we
    # get a large enough sample of papers such that some are
    # from the past 4 weeks
    max_results: 1000
    trailing:
      num: 4
      unit: "weeks"
```

## Set Up GitHub Actions Workflow

To trigger periodic searches and send email summaries of the search results, we will create a GitHub Actions workflow
in the repository. The workflow will run the search queries defined in the configuration file at regular intervals
and send email summaries of the search results using the `sxolar` library.

The workflow will need to do the following:

1. Install the `sxolar` library.
2. Run the search queries defined in the configuration file.
3. Send email summaries of the search results.

Thanks to the [command line api](../user-guide/command-line-api.md) of `sxolar`, we can combine
the steps 2 and 3 into a single command. The below is an example of a GitHub Actions workflow that triggers periodic
searches and sends email summaries of the search results:

```yaml
name: Example Sxolar Run
on:
  # Uncomment the below to also run on pushes, as a way to test
  #  push:
  #      branches:
  #      - main
  schedule:
    # Run Weekly on Sunday at 8am EST (1pm UTC)
    # For more detail on cron syntax, see https://crontab.guru/
    - cron: '0 13 * * 0'

jobs:
  MySummary:
    # Setup the minimal environment: linux and python 3.11
    name: UNIX Build (${{ matrix.python-version }}, ${{ matrix.os }})
    runs-on: ${{ matrix.os }}
    defaults:
      run:
        shell: bash -l {0}
    strategy:
      fail-fast: false
      max-parallel: 4
      matrix:
        os: [ "ubuntu-latest" ]
        python-version: [ "3.11" ]

    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      # Install the necessary dependencies (sxolar)
      - name: Install sxolar
        run: |
          pip install sxolar

      # Run the summary using the command line and config file
      - name: Run GWaves
        run: |
          sxolar summary --config configs/gwaves.yml \
            --name GWaves \
            --email-to myrecipient@gmail.com \
            --email-from myemail@gmail.com \
            --email-subject "Sxolar Weekly Digest: GWwaves" \
            --gmail-app-password "${{ secrets.SXOLARGMAILAPPPASSWORD }}" \
            --output email
```
