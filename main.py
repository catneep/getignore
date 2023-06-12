import argparse
import glob
import json
import os
import requests
import sys
import tempfile

from dataclasses import dataclass

@dataclass(frozen= True, order= False)
class ApiResult:
  name: str
  path: str
  url: str

def _create_tmp() -> str:
  tmp = tempfile.gettempdir()
  sub_dir = os.path.join(tmp, 'gitig-fetch')
  os.makedirs(sub_dir, exist_ok= True)
  return sub_dir

def store_in_cache(name: str, content: str):
  sub_dir = _create_tmp()

  # Create and store a file in the subdirectory
  tmp_file = os.path.join(sub_dir, f'{name}.txt')
  with open(tmp_file, 'w') as file:
    file.write(content)


def search_in_cache(lookup: str) -> str | None:
  sub_dir = _create_tmp()
  results = glob.glob(os.path.join(sub_dir, f'{lookup}.txt')) # TODO: Fix
  content = None
  if not results:
    return None

  if len(results) == 1:
    with open(results[0], 'r') as file:
      content = file.read()

  return content

def get_raw_content(url) -> str | None:
  response = requests.get(url)
  if response.status_code == 200:
    return response.text

  return None


def list_files(user, repo, path) -> tuple:
  results = list()

  url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"
  response = requests.get(url)
  
  if response.status_code == 200:
    items = json.loads(response.text)
    for item in items:
      if item['type'] == 'file':
        results.append(
          ApiResult(
            name= item['name'].replace('.gitignore', ''),
            path= item['path'],
            url= item['download_url'],
          )
        )

  else:
    print(f"Failed to get files from repo: {response.status_code}")

  return tuple(results)

def find_similar_strings(lookup_term: str, items: set) -> tuple:
  similars = list()
  for item in items: #ApiResults
    # Handle exact match
    if (lookup_term.strip().lower() == item.name.lower()):
      return tuple([item])

    if (lookup_term.strip().lower() in item.name.lower()):
      similars.append(item)

  return tuple(similars)


if __name__ == "__main__":
  # Parse command line arguments
  parser = argparse.ArgumentParser(
    description= 'Retrieve a gitignore template from GitHub'
  )
  parser.add_argument("name", help="name to filter files by")
  parser.add_argument("-c", action="store_true", help='fetch from "community"')
  parser.add_argument("-g", action="store_true", help='fetch from "global"')
  parser.add_argument("-r", action="store_true", help='fetch from root (default)')
  parser.add_argument("-l", action="store_true", help='fetch from local cache')
  args = parser.parse_args()

  # Then do stuff
  user = 'github'
  repo = 'gitignore'
  results = None

  if args.l:
    cache_result = search_in_cache(args.name)
    if cache_result:
      print(cache_result)
      sys.exit(0)

  if args.c:
    results = list_files(user, repo, 'community')
  elif args.g:
    results = list_files(user, repo, 'Global')
  else:
    results = list_files(user, repo, '')

  if not results:
    print('# Error retrieving gitignore')
    sys.exit(1)

  similar = find_similar_strings(lookup_term= args.name, items= results)
  if (not similar):
    print('# Error retrieving gitignore')
    sys.exit(1)

  ## Doesn't handle multiple results :(
  # Save in cache
  content = get_raw_content(similar[0].url)
  store_in_cache(name= similar[0].name, content= content)
  print(content)
