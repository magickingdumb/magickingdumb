import requests

def get_github_code(hashtag):
    url = 'https://api.github.com/search/repositories'
    params = {'q': f'description:{hashtag}'}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        repositories = response.json()['items']
        if repositories:
            repository = repositories[0]
            repository_url = f'https://api.github.com/repos/{repository["full_name"]}/contents'
            response = requests.get(repository_url)
            if response.status_code == 200:
                contents = response.json()
                code = ''
                for file in contents:
                    if file['type'] == 'file':
                        file_url = file['download_url']
                        response = requests.get(file_url)
                        if response.status_code == 200:
                            code += response.text + '\n\n'
                return code
        else:
            return f'No repositories found with hashtag "{hashtag}" in their description.'
    else:
        return 'Error: could not retrieve repositories from GitHub API.'

# Example usage
hashtag = input('Enter a hashtag to search for on GitHub: ')
code = get_github_code(hashtag)
print(code)
