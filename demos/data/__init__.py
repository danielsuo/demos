import pollster
import pprint

import pandas as pd

from .states import get_long_name


# Types
# - Polls
# - Demographic
# - Returns
class Source(object):
    def __init__(self, url):
        self.url = url


def run():
    api = pollster.Api()
    columns = [
        "state", "pollster", "pop", "vtype", "method", "begmm", "begdd",
        "begyy", "endmm", "enddd", "endyy", "trump", "clinton", "other",
        "undecided", "Begdate", "Enddate", "Middate"
    ]

    file = open("results.csv", "a")
    file.write("{}\n".format(",".join(columns)))

    results = pd.DataFrame(columns=columns)
    polls_seen = set()

    index = 0

    try:
        # Get all questions related to the 2016 presidential election
        questions = api.questions_get(tags="2016-president")
        for question in questions.items:

            # Ignore poll questions that aren't Trump vs. Clinton
            if "TrumpvClinton" not in question.slug:
                continue

            print("Question: {}".format(question.slug))

            poll_cursor = "0"

            # Grab all polls that contain this question
            while True:
                polls = api.polls_get(
                    question=question.slug, cursor=poll_cursor)

                if len(polls.items) == 0:
                    break

                poll_cursor = polls.next_cursor

                for poll in polls.items:

                    # Ignore this poll if we've seen it before
                    if poll.slug in polls_seen:
                        continue
                    polls_seen.add(poll.slug)

                    print("  Poll: {}".format(poll.slug))

                    # Grab all questions in a given poll (yes, this is circular)
                    for poll_question in poll.poll_questions:

                        if poll_question.question is None or "TrumpvClinton" not in poll_question.question.slug:
                            continue

                        print("    PollQuestion: {}".format(
                            poll_question.question.slug))

                        # TODO: look at examples where there's more than one subpopulation
                        pop = poll_question.sample_subpopulations[0]

                        result = pd.DataFrame(
                            None, index=[index], columns=columns)
                        result.state = poll_question.question.slug[3:5]
                        result.pollster = poll.survey_house
                        result.pop = pop.observations if pop.observations is not None else 1
                        result.vtype = pop.name
                        result.method = poll.mode
                        result.begmm = poll.start_date.month
                        result.begdd = poll.start_date.day
                        result.begyy = poll.start_date.year
                        result.endmm = poll.end_date.month
                        result.enddd = poll.end_date.day
                        result.endyy = poll.end_date.year

                        for response in pop.responses:
                            if response.pollster_label == "Clinton":
                                result.clinton = response.value
                            elif response.pollster_label == "Trump":
                                result.trump = response.value
                            elif response.pollster_label == "Undecided":
                                result.undecided = response.value

                        if result.clinton is None:
                            result.clinton = 0
                        if result.trump is None:
                            result.trump = 0
                        if result.undecided is None:
                            result.undecided = 0

                        result.other = 100 - result.clinton - result.trump - result.undecided

                        result.to_csv(file, header=False)
                        results.append(result)
                        index += 1

    except pollster.rest.ApiException as e:
        print(e)
        file.close()

    file.close()
    return results


__all__ = ["get_long_name"]
