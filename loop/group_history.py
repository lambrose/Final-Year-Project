from loop.models import GroupResults
from flask_login import current_user


class GroupHistory:

    def query_db(self):
        results = GroupResults.query.filter_by(user_id=current_user.id)
        return results

    def get_history(self):
        query = self.query_db()
        data = []
        winner = "fas fa-check-circle green_icon"
        contained_the_winner = "fas fa-exclamation-circle blue_icon"
        loser = "fas fa-times-circle red_icon"
        for record in query:
            entry = [record.additive, record.multiplicative, record.borda, record.copeland, record.plurality_voting,
                     record.approval, record.least_misery, record.most_pleasure, record.average_without_misery]
            formatted_entry = [record.winner, record.author.first_name, record.author.last_name]
            for s in entry:
                if s == 2:
                    formatted_entry.append(winner)
                elif s == 1:
                    formatted_entry.append(contained_the_winner)
                else:
                    formatted_entry.append(loser)
            formatted_entry.append(record.publish_date)
            data.append(formatted_entry)
        return data

    def get_rankings(self):
        query = self.query_db()
        data = []
        for record in query:
            ss = [record.additive, record.multiplicative, record.borda, record.copeland, record.plurality_voting,
                  record.approval, record.least_misery, record.most_pleasure, record.average_without_misery]
            data.append(ss)
        values = [sum(rating) for rating in zip(*data)]
        return values
