=======
# SharedProcessors


## AFSAuth

The AFSAuth prcoessor performs AFS authentication by obtaining an AFS token.
This function is performed by spawning shell processes.

In order to prevent the need of multiple overrides in development environments the following environment variables need to be set:
* KEYTABNAME
* PRINCIPAL

```shell
export KEYTABNAME='/path/to/keytab'
export PRINCIPAL='foo@OX.AC.UK'
```

## AFSDeauth

The AFSDeauth processor performs deauthorization by performing unlog and kdestory.

## FSFileProvider

