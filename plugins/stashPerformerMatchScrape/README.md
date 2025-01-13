# Stash Matched Performer Scrape

This script updates performer data in Stash by matching and merging data from StashDB and ThePornDB(TPDB). It can update all performers in the collection or a single performer triggered by a `Performer.Create.Post` hook.

## Features

- Scrapes performer data from StashDB and ThePornDB.
- Merges data from both sources, prioritizing StashDB data if available.
- Adds or updates stash IDs from StashDB and ThePornDB.
- Supports updating all performers in the collection or a single performer via a hook.

## Configuration

Pulls the StashDB and ThePornDB API keys from the configured stash boxes in the stashapp:

## Updating All Performers

To update all performers in your Stash collection, run the `Scrape All Performers` task in the `Settings > Tasks` section.

## Performers Scraped Automatically

On a `Performer.Create.Post` the plugin will attempt to name match your created performer to both StashDB and ThePornDB. If a name match is made, it will scrape from one, or both sources, and merge the data into your newly created performer.

