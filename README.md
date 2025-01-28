# Ansible lookup plugin: SIS

An Ansible plugin for retrieving data about subjects taught at Charles University.

For more information about what lookup plugins are and how to use them,
see [Ansible Community Documentation](https://docs.ansible.com/ansible/latest/plugins/lookup.html).

## Getting started

You can try this plugin by setting up your environment with

```sh
poetry install
eval "$(poetry env activate)"
export ANSIBLE_LOOKUP_PLUGINS=./plugins/lookup
```

and running a sample playbook.

```console
$ ansible-playbook playground/test.yaml

PLAY [Test SIS lookup plugin] **************************************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [Inspect NSWI126] *********************************************************
ok: [localhost] => {
    "msg": {
        "4eu+": "ne",
        "anglický název": "Advanced Tools for Software Development and Monitoring",
        "další informace": "http://d3s.mff.cuni.cz/teaching/nswi126/",
        "e-kredity": "2",
        "fakulta": "Matematicko-fyzikální fakulta",
        "garant": "doc. RNDr. Pavel Parízek, Ph.D.",
        "jazyk výuky": "čeština",
        "je neslučitelnost pro": "NSWX126",
        "je záměnnost pro": "NSWX126",
        "kategorizace předmětu": "Informatika, >, Softwarové inženýrství",
        "kód": "NSWI126",
        "minimální obsazenost": "neomezen",
        "název": "Pokročilé nástroje pro vývoj a monitorování software",
        "platnost": "od 2023",
        "počet míst": "neomezen",
        "rozsah, examinace": "zimní s.:0/2, Z, [HT]",
        "semestr": "zimní",
        "stav předmětu": "vyučován",
        "třída": "Informatika Mgr. - volitelný",
        "virtuální mobilita / počet míst pro virtuální mobilitu": "ne",
        "vyučující": "doc. RNDr. Pavel Parízek, Ph.D.",
        "zajišťuje": "Katedra distribuovaných a spolehlivých systémů (32-KDSS)",
        "způsob výuky": "prezenční"
    }
}

TASK [Generate files for lecture notes] ****************************************
changed: [localhost] => (item=NDBI001)
changed: [localhost] => (item=NDBI025)
changed: [localhost] => (item=NSWI126)

PLAY RECAP *********************************************************************
localhost                  : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```

To use this plugin in your existing project, install its dependencies
(see [`pyproject.toml`](pyproject.toml)) and add the directory
[`plugins/lookup`](plugins/lookup/) to
[DEFAULT_LOOKUP_PLUGIN_PATH](https://docs.ansible.com/ansible/latest/plugins/lookup.html).

## Documentation

To view plugin's documentation, run following command:

```console
$ ansible-doc -t lookup sis
> LOOKUP [1msis[0m (/app/extension/plugins/lookup/sis.py)

  Get information about subjects taught at Charles University.

[1mOPTIONS[0m (red indicates it is required):

   [1m_terms[0m  subject codes
        type: string

[1mAUTHOR[0m: Petr Borňás <p@brns.cz>

[1mNAME[0m: sis

[1mEXAMPLES:[0m
- name: Inspect NSWI126
  debug: msg="{{ lookup('sis', 'NSWI126') }}"

[1mRETURN VALUES:[0m

   _list   information published about the subjects
        elements: dict
        type: list

```

