import csv
import os
import pyrankvote
from pyrankvote import Candidate, Ballot

NUMBER_OF_WINNERS = 2

# Process all CSV files in directory.
script_folder = os.path.dirname(os.path.realpath(__file__))
for path in os.listdir(script_folder):
  if path.endswith(".csv"):

    print("Processing results for %s." % path)
    
    # Read all ballots from the CSV file.
    ballots = []
    with open(os.path.join(script_folder, path)) as f:
      reader = csv.reader(f)
      first_row = True
      for row in reader:
        if first_row:
          first_row = False
          continue
        # Skip timestamp and user.
        ballots.append(row[2:])

    # Create Candidate objects for every proposal.
    proposals = {}
    for ballot in ballots:
      for proposal in ballot:
        if proposal not in proposals:
          proposals[proposal] = Candidate(proposal)

    # Create Ballot objects for every ballot.
    processed_ballots = []
    for ballot in ballots:
      ranked = []
      for proposal in ballot:
        ranked.append(proposals[proposal])
        processed_ballots.append(Ballot(ranked_candidates=ranked))

    # Print election results.
    election_result = pyrankvote.single_transferable_vote(proposals.values(),
        processed_ballots, number_of_seats=NUMBER_OF_WINNERS)
    print(election_result)