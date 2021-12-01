---
title: Test Space LFS
emoji: 🤗
colorFrom: blue
colorTo: red
sdk: streamlit
app_file: app.py
pinned: false
---


<div align="center">

<h1>Using LFS on Hugging Face Spaces</h1>

[![Generic badge](https://img.shields.io/badge/🤗-Open%20In%20Spaces-blue.svg)](https://huggingface.co/spaces/nateraw/test-space-lfs)
[![Github Badge](https://img.shields.io/github/stars/nateraw/test-space-lfs?style=social)](https://github.com/nateraw/test-space-lfs)
[![Template badge](https://img.shields.io/badge/🤗-Spaces%20Template-red.svg)](https://huggingface.co/spaces/nateraw/spaces-template)

</div>

**This repo shows you how to:**
  - Sync your GitHub repo with a Hugging Face Spaces repo so you only have to push your code on GitHub.
  - Use Hugging Face for LFS *instead* of GitHub for LFS (Because it's free!)

# Overview

Basically, the idea is that we're going to use one repo to push our code to, but we're going to use a Spaces repo to hold the LFS files. So, we'll have to interact with the 2nd repo ONLY when you need to upload large files. 

This has a few benefits:

1. GitHub charges you for LFS storage, Hugging Face currently doesn't
2. Your LFS files will be available instantly in your Spaces repo, so you don't have to wait to download them
3. If you were using GitHub for LFS, you'd have to sync your large files with HF too, which would lead to long wait times on GitHub actions runners.


## 
## Step 1 - Create a New Project from the Spaces Template

Use this template to create and sync a GitHub repo with a 🤗 Spaces repo:

[![Spaces Template](https://img.shields.io/badge/🤗-Spaces%20Template-red.svg)](https://huggingface.co/spaces/nateraw/spaces-template)


## Step 2 - Update the GitHub Actions Workflow

Because we'll be making changes to the git history in two places, we'll need to update the history from the GitHub repo to match any changes that were made in the Spaces repo.

So, we need to add a few lines to `.github/workflows/sync_to_hub.yml` file to account for this. 

By default, it'll look something like this...

```yaml
    - name: Push to hub
    env:
        HF_TOKEN: ${{ secrets.HF_TOKEN }}  # Uses a GitHub secret called HF_TOKEN which is just a HF API Token
    run: git push https://nateraw:$HF_TOKEN@huggingface.co/spaces/nateraw/test-space-lfs main
```

We make updates to the `run` section of the workflow to add the following:

```yaml
    - name: Push to hub
    env:
        HF_TOKEN: ${{ secrets.HF_TOKEN }}
        GIT_LFS_SKIP_SMUDGE: 1
    run: |
        git config --global user.email "naterawdata@gmail.com"
        git config --global user.name "nateraw"
        git remote add hf https://nateraw:$HF_TOKEN@huggingface.co/spaces/nateraw/test-space-lfs
        git fetch --all --prune
        git rebase hf/main
        git push https://nateraw:$HF_TOKEN@huggingface.co/spaces/nateraw/test-space-lfs main

```

Here, after we've checked out the GitHub repo via the generic actions/checkout workflow, we...

- Add `GIT_LFS_SKIP_SMUDGE` to the `env` section of the workflow. This makes it so we'll just download ref files, not the actual LFS files when updating the history.
- Define our git config - you should put your own info here, not mine!
- Add the spaces repo as a remote called `hf`
- Fetch the remote to get the history of the spaces repo.
- Rebase the history from the remote (spaces repo) to the local (GitHub) repo
- Push up to the Hugging Face Spaces repo

---

## Step 3 - Add LFS Files

To add LFS files to your Spaces repo, you can either clone the repo separately, or add it as a remote and checkout the main branch from there... I find cloning it separately is easier, and I usually just delete it when I'm done. (Or maybe I'm just too lazy to figure out the steps to the latter 😅)

```bash
git clone huggingface.co/spaces/nateraw/test-space-lfs
cd test-space-lfs
git lfs install
git add <some large file>
```

Check that the files are being tracked before commiting! they should show up under "Git LFS objects to be committed" and should have (LFS: ...) at the end, not (Git: ...)

``` 
git lfs status
```

If the above doesn't look right, make sure you've added the right pattern to your `.gitattributes` file. 

Once finished, commit your data and push it to the Spaces repo.

```
git commit -m "Add data"
git push -u origin main
```

## Limitations/Additional Thoughts

⚠️ Don't update code files in the Spaces repo directly. If you do, you'll run into merge conficts in the actions workflow, and you'll have a bad time.

My suggestion is to keep your LFS files in a subdirectory in your repo, so it's harder to screw things up.

TODO - look into using remote `hf` to add the files locally instead of a copy...the whole point of syncing GitHub to begin with was to avoid having 2 copies of the same thing, so we should really figure this out! (❤️ Contributions appreciated!)
