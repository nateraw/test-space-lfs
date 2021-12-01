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

- define our git config
- add the spaces repo as a remote called `hf`
- Fetch the remote to get the history - Since we defined `GIT_LFS_SKIP_SMUDGE` as 1, we'll just download ref files, not the actual LFS files.
- Rebase the history from the remote (spaces repo) to the local (GitHub) repo
- Push up to the Hugging Face Spaces repo

---

## Step 3 - Add LFS Files

...todo...