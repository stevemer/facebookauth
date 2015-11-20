import facebook, requests, sys, json
from flask import Flask, request

app = Flask(__name__)

access_token = "CAACEdEose0cBAB4Bk2JLQiNTIJWTWTmcByP76elJkVTVTfzjT9LQdGKCjkSD571VJ5J6oLYTZAUNqJDtZBDsxr4qnUcLsEOPjgtZCOeElTOTbmSSEaZBErVQ94vvfF3ZBH65zBYZCZBBJmiLDroHNZC8XhUOxHY5SvSKK9g6uBAT30D3ME9gvteeL8XKrPupmuDjf8ltwAdhfsTB4A60Azvs"

@app.route('/')
def get_friends():
    return json.dumps(request.cookies)
    user = "me"

    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(user)

    friends = []

    r = graph.get_connections(profile['id'], 'friends')

    while True:
        try:
            friends.extend(r['data'])
            r = requests.request("GET", r['paging']['next'], params={"access_token": access_token}).json()
        except KeyError as e:
            # no more pagination, we have it all
            break
    return json.dumps(friends)

if __name__ == "__main__":
    app.run(debug=True)
