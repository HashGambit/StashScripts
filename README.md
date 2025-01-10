# How to add to Stash

go to Settings > Plugins > Available Plugins > Add Source

Source URL
```
https://hashgambit.github.io/StashScripts/stable/index.yml
```

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
