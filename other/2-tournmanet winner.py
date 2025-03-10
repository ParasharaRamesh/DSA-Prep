from collections import Counter

def tournamentWinner(competitions, results):
    teams = dict()

    #for result 1 is home victory 0 is away victory so we can just say result[i] - 1
    for match, result in zip(competitions, results):
        victor = match[result - 1]
        if victor not in teams:
            teams[victor] = 3
        else:
            teams[victor] += 3

    return Counter(teams).most_common(1)[0][0]