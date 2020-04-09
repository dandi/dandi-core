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

#### Updates

Ideally, following
[these instructions](https://lostechies.com/johnteague/2014/04/04/using-git-subtrees-to-split-a-repository/)
I should have kept splitting done in a separate repository.  Since it is
all here, I just added itself as a remote:

	git remote add --fetch self .

Now following steps could resplit (results in just adding new commits),
and then re-pull into master under `assets/`:

	git checkout dandiarchive_master
	git subtree split --prefix=web/src/assets -b subtree_split_assets
	git checkout master
	git subtree pull --prefix=assets self subtree_split_assets

