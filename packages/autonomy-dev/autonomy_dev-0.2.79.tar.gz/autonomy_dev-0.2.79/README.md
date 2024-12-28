# Project Status Badges

[![Code Quality](https://github.com/8ball030/auto_dev/actions/workflows/common_check.yaml/badge.svg)](https://github.com/8ball030/auto_dev/actions/workflows/common_check.yaml)


# Autonomy Dev

Tooling to speed up open-autonomy development.


## TLDR

```bash
# install 
pip install autonomy-dev[all]
```

```bash
# create a repo & a simple webserver agent
adev repo scaffold fun_new_hack && \
cd fun_new_hack && \
adev create author/cool_agent \
    -t eightballer/frontend_agent # type of template to use.
# sync to the local registry.
yes 'third_party' | autonomy packages lock

```

```bash
# run the agent and verify the endpoint

```


## Usage

There are a number of useful command tools available.

- Dev Tooling:
    A). linting `adev lint`
    B). formatting `adev fmt`
    C). dependency management `adev deps update`

- Scaffolding: Tooling to auto generate repositories and components.


### Create

- Templated agents for speedy proof of concept and getting started fast.


### Scaffolding of Components

#### Protocols

We provide tools to generate protocols components from specs.

```bash
adev create author/tmp_agent_name -t eightballer/base --force
cd tmp_agent_name
adev scaffold protocol ../specs/protocols/balances.yaml 
aea -s publish --push-missing
...
Starting Auto Dev v0.2.75 ...
Using 32 processes for processing
Setting log level to INFO
Creating agent tmp_agent_name from template eightballer/base
Executing command: ['poetry', 'run', 'autonomy', 'fetch', 'bafybeidohldv57m3jkc33zpgbxukaushmcibmt4ncnsnomd3pvpocxs3ui', '--alias', 'tmp_agent_name']
Command executed successfully.
Agent tmp_agent_name created successfully.
Starting Auto Dev v0.2.75 ...
Using 32 processes for processing
Setting log level to INFO
Read protocol specification: ../specs/protocols/balances.yaml
protolint version 0.50.0(d6a3250)
protolint version 0.50.0(d6a3250)
Updated: /home/eight/Projects/StationsStation/repos/capitalisation_station/tmp_agent_name/protocols/balances/custom_types.py
New protocol scaffolded at /home/eight/Projects/StationsStation/repos/capitalisation_station/tmp_agent_name/protocols/balances

...
# Tests can be run as well;
adev test -p packages/eightballer/protocols/balances
Testing path: `packages/eightballer/protocols/balances/` ⌛
Testing... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   0% -:--:--👌 - packages/eightballer/protocols/balances/
Testing... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:02
Testing completed successfully! ✅
```

#### Contracts

We can scaffold a new contract using the `adev scaffold contract` command. This will create a new directory with;
- open-aea contract component
    - open-aea contract component class 🎉
    - open-aea contract component function generation 🚧
    - open-aea contract component test generation 🚧


```bash
adev scaffold contract 0xc939df369C0Fc240C975A6dEEEE77d87bCFaC259 beyond_pricer \
      --block-explorer-api-key $BLOCK_EXPLORER_API_KEY \
      --block-explorer-url "https://api-goerli.arbiscan.io"
```


## Installation

```bash
pip install autonomy-dev[all]
```
## Release

```bash
checkout main
git pull
adev release
```



# Test Coverage
```plaintext
<!-- Pytest Coverage Comment:Begin -->
Name                             Stmts   Miss  Cover   Missing
--------------------------------------------------------------
auto_dev/__init__.py                 0      0   100%
auto_dev/base.py                    60     19    68%   66-88
auto_dev/check_dependencies.py     236    236     0%   28-452
auto_dev/cli.py                      4      1    75%   9
auto_dev/cli_executor.py            68     36    47%   33-61, 79, 83, 87-89, 92-94, 99-105
auto_dev/constants.py               25      0   100%
auto_dev/enums.py                   36      0   100%
auto_dev/exceptions.py               5      0   100%
auto_dev/fmt.py                     59     43    27%   16-17, 21-22, 27-45, 50, 60-61, 66-80, 85-97, 102-112
auto_dev/lint.py                     7      3    57%   13-27
auto_dev/local_fork.py              52     32    38%   32-33, 37-54, 58-95
auto_dev/test.py                    16     13    19%   4, 16-39
auto_dev/utils.py                  251    153    39%   76-77, 81, 94-101, 106-151, 167, 180-185, 204-228, 233, 240-242, 247, 252, 257-269, 276-281, 290-293, 298-318, 323-337, 342-348, 370-372, 381, 388-416
--------------------------------------------------------------
TOTAL                              819    536    35%
<!-- Pytest Coverage Comment:End -->
```
