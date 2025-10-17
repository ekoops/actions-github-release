#!/usr/bin/env python3

from github import Github
import os
import re

# Try to get options from enviroment and from inputs as fallback
wanted_release = os.getenv('type', os.getenv('INPUT_TYPE'))
repository = os.getenv('repository', os.getenv('INPUT_REPOSITORY'))
token = os.getenv('token', os.getenv('INPUT_TOKEN', None))

filter = os.getenv('INPUT_FILTER', None)
filter_regex = None
if filter is not None:
    filter_regex = re.compile(filter)

# Init class
G = Github(token) if token else Github()
repo = G.get_repo(repository)
releases = repo.get_releases()

# Output formatting function
def output(release):
    outfile = open(os.getenv('GITHUB_OUTPUT'), 'w')
    outfile.write(f'release={release.tag_name}\n')
    outfile.write(f'release_id={release.id}\n')
    assets = release.get_assets()
    dl_url = assets[0].browser_download_url if assets.totalCount > 0 else '""'
    outfile.write(f'browser_download_url={dl_url}\n')
    outfile.close()

# Releases parsing
for release in releases:
    if filter_regex is not None and re.search(filter_regex, release.tag_name) is None:
        continue

    if wanted_release == 'stable':
        if release.prerelease == 0 and release.draft == 0:
            output(release)
            break
    elif wanted_release == 'prerelease':
        if release.prerelease == 1:
            output(release)
            break
    elif wanted_release == 'latest':
        output(release)
        break
    elif wanted_release == 'nodraft':
        if release.draft == 0:
            output(release)
            break
    else:
        print('Can\'t get release')
