from flask import Blueprint, json, request, render_template
from app.extensions import post_action_to_database, get_latests_actions_from_database
from app.webhook.models import Action

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    print("received request")
    json_data = json.loads(request.data)
    print(json_data)
    if request.is_json:
        json_data = json.loads(request.data)
        storeActionToDatabase(json_data)
    else:
        return {}, 400
    return {}, 200


@webhook.route('/monitor')
def monitor():
    documents = get_latests_actions_from_database()
    return render_template('index.html', documents=documents)





def storeActionToDatabase(json_data):
    if 'action' in json_data and json_data['action'] == 'opened':
        from_branch = json_data['pull_request']['head']['ref']
        to_branch = json_data['pull_request']['base']['ref']
        author = json_data['pull_request']['user']['login']
        action = "PULL_REQUEST"
        request_id = json_data['pull_request']['id']
        new_action =  Action(request_id=request_id, author=author,from_branch=from_branch, to_branch=to_branch, action=action)
        post_action_to_database(new_action)
    elif 'action' in json_data and json_data['action'] == 'closed' and json_data['pull_request']['merged_at'] != None:
        from_branch = json_data['pull_request']['head']['ref']
        to_branch = json_data['pull_request']['base']['ref']
        author = json_data['pull_request']['merged_by']['login']
        action = "MERGE"
        request_id = json_data['pull_request']['id']
        new_action = Action(request_id=request_id, author=author,from_branch=from_branch, to_branch=to_branch, action=action)
        post_action_to_database(new_action)
    elif 'action' not in json_data:
        author = json_data['head_commit']['author']['name']
        ref_value=json_data['ref']
        extracted_value=ref_value.split('/')[-1]
        to_branch = extracted_value
        from_branch = None
        action = "PUSH"
        request_id = json_data['head_commit']['id']
        new_action = Action(request_id=request_id, author=author,from_branch=from_branch, to_branch=to_branch, action=action)
        post_action_to_database(new_action)