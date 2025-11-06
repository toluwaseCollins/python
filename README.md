# Watch tower service helper scripts


## setup
* python -m venv my_env
* source my_env/bin/activate
* pip install -r requirements.txt


## Usage
1. Create token.txt file and place valid `watchtower-service` jwt token. "Include the `Bearer ` prevfix and ensure no new line or space after the token
2. create a `references.txt` file and insert the type of references to use for your query, one per line

Eachs script contains comments on usage