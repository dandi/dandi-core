# dandi-core
Shared functionality and resources used by multiple components

## Developers information

### `assets/`

It was populated from the dandiarchive repository using `git subtree` mechanism.
This should be a complete history of events:

	git fetch http://github.com/dandi/dandiarchive master:dandiarchive_master
	git checkout dandiarchive_master
	git subtree split --prefix=web/src/assets -b subtree_split_assets
	git checkout master
	git subtree add --prefix=assets subtree_split_assets

Later updates should involve some additional commands to be done to pull in new
commits ;)
