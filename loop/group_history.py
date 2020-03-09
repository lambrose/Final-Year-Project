from loop.models import GroupResults
from flask_login import current_user


class GroupHistory:

    def query_db(self):
        results = GroupResults.query.filter_by(user_id=current_user.id)
        return results

    def get_history(self):
        query = self.query_db()
        data = []
        # bootstrap icon values
        winner = "fas fa-check-circle green_icon"
        contained_the_winner = "fas fa-exclamation-circle blue_icon"
        loser = "fas fa-times-circle red_icon"
        # check all records in the group results database that corresponds to the logged in user
        for record in query:
            entry = [record.additive, record.multiplicative, record.borda, record.copeland, record.plurality_voting,
                     record.approval, record.least_misery, record.most_pleasure, record.average_without_misery]
            formatted_entry = [record.id, record.winner, record.author.first_name, record.author.last_name]
            for value in entry:
                # if the value is 2 then they get a green check
                if value == 2:
                    formatted_entry.append(winner)
                # if the value is 1 then they get a blue exclamation
                elif value == 1:
                    formatted_entry.append(contained_the_winner)
                # if the value is 0 then they get a red cross
                else:
                    formatted_entry.append(loser)
            formatted_entry.append(record.publish_date)
            data.append(formatted_entry)
        return data

    # this is used for the bar chart to monitor group results
    def get_rankings(self):
        query = self.query_db()
        data = []
        # check all records in the group results database that corresponds to the logged in user
        for record in query:
            entry = [record.additive, record.multiplicative, record.borda, record.copeland, record.plurality_voting,
                     record.approval, record.least_misery, record.most_pleasure, record.average_without_misery]
            data.append(entry)
        # for each algorithm add up all the values entries
        values = [sum(rating) for rating in zip(*data)]
        # then values are returned to be graphed
        return values
