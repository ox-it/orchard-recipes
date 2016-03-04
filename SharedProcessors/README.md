=======
# SharedProcessors


## AFSAuth

The AFSAuth prcoessor performs AFS authentication by obtaining an AFS token.
This function is performed by spawning shell processes.

There are two optional input variables:
*`auth_method`: the authentication method, defaulting to the only supported option keytab
*`aklog_path`: the path to aklog, default /usr/local/bin/aklog

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


The FSFileProvider processor requires 2 input variables:
* re_pattern
* path

The path variable should be set as a directory that contains the software to be packaged.
This directory is then listed and the regex provided in re_pattern is then performed on this list.

Items that match this list are then compared and the newest release is returned.
