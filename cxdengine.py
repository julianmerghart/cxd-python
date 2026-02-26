import hashlib
import time
import secrets
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class CxDNode:
    def __init__(self, node_id, federation_members):
        self.node_id = node_id
        self.federation = federation_members
        self.ledger = []

    def decrypt_and_validate(self, payload):
        try:
            vote_value = payload.get("vote")
            voter_id = payload.get("voter_id")
            location = payload.get("location")
            
            if location == "Cooper, TX":
                return vote_value
            return None
        finally:
            voter_id = "00000000"
            payload = None

    def reach_consensus(self, vote):
        threshold = (len(self.federation) // 2) + 1
        votes_received = 1 
        for peer in self.federation:
            if peer != self.node_id:
                votes_received += 1 
        
        if votes_received >= threshold:
            self.commit_to_ledger(vote)
            return True
        return False

    def commit_to_ledger(self, vote):
        entry = {
            "timestamp": time.time(),
            "vote": vote,
            "hash": hashlib.sha256(str(vote).encode()).hexdigest()
        }
        self.ledger.append(entry)

node = CxDNode(node_id="Node_A", federation_members=["Node_A", "Node_B", "Node_C", "Node_D"])

@app.route('/submit-vote', methods=['POST'])
def submit_vote():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    validated_vote = node.decrypt_and_validate(data)
    
    if validated_vote:
        success = node.reach_consensus(validated_vote)
        if success:
            return jsonify({"status": "success", "message": "Vote recorded"}), 200
    
    return jsonify({"status": "denied", "message": "Validation failed"}), 403

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
