# HashGambit's Stash Scripts repository

This repository contains plugins, themes, userscripts and other utility scripts created by me or forked from other users.

The community StashScript repo can be found [on their github site](https://github.com/stashapp/CommunityScripts).

More extensive list of plugins and other projects for Stash is available [on the stashapp documentation site](https://docs.stashapp.cc/plugins).

## Plugins

### Installing via manager

Plugins can be installed and managed from the **Settings** > **Plugins** page.

Plugins are installed using the **Available Plugins** section. Use **Add Source** with the URL `https://hashgambit.github.io/StashScripts/stable/index.yml` to add this repo of plugins.

Installed plugins can be updated or uninstalled from the **Installed Plugins** section.


## Contributing

### Formatting

Formatting is enforced on all files. Follow this setup guide:

1. **[Yarn](https://yarnpkg.com/en/docs/install)** and **its dependencies** must be installed to run the formatting tools.
    ```sh
    yarn install --frozen-lockfile
    ```

2. **Python dependencies** must also be installed to format `py` files.
    ```sh
    pip install -r requirements.txt
    ```

#### Formatting non-`py` files

```sh
yarn run format
```

#### Formatting `py` files

`py` files are formatted using [`black`](https://pypi.org/project/black/).

```sh
yarn run format-py
```
