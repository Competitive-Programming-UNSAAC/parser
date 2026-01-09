import requests
import configparser
from datetime import datetime
import json
import os

config = configparser.ConfigParser()
config.read('Config')

judgeMode = config["Judge"]["mode"]
judgeHost = config["Judge"]["host"]
contestId = config["Judge"]["id"]
admin = config["Judge"]["admin"]
password = config["Judge"]["password"]

metadataDir = config["Metadata"]["path"]
problemsFile = config["Metadata"]["problems"]
submissionsFile = config["Metadata"]["submissions"]
contestantsFile = config["Metadata"]["contestants"]
judgementsFile = config["Metadata"]["judgements"]

contestDuration = config["Contest"]["duration"]
contestStart = config["Contest"]["start"]
contestFrozenTimeDuration = config["Contest"]["frozenTimeDuration"]
contestName = config["Contest"]["name"]
contestMode = config["Contest"]["mode"]

hashVeredict = {
    "AC" : "Accepted",
    "WA" : "Wrong Answer",
    "TLE" : "Wrong Answer",
    "MLE" : "Wrong Answer",
    "OLE" : "Wrong Answer",
    "RTE" : "Wrong Answer",
    "NO" : "Wrong Answer",
    "CE" : "Compilation Error"
}

verdicts = {
    "accepted": ["Accepted"],
    "wrongAnswerWithPenalty": ["Wrong answer"],
    "wrongAnswerWithoutPenalty": ["Compilation error"]
}

class ContestMetadata:
    duration = 0
    start = 0
    frozenTimeDuration = 0
    name = ""
    type = ""

    def __init__(self, start, duration, frozenTimeDuration, name, type):
        self.duration = duration
        self.start = start
        self.frozenTimeDuration = frozenTimeDuration
        self.name = name
        self.type = type

class Problem:
    index = ""
    def __init__(self, index):
        self.index = index


class Contestant:
    id = ""
    name = ""
    category = ""

    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

class Submission:
    timeSubmitted = 0
    contestantName = ""
    problemIndex = ""
    verdict = ""

    def __init__(self, timeSubmitted, contestantName, problemIndex, verdict):
        self.timeSubmitted = timeSubmitted
        self.contestantName = contestantName
        self.problemIndex = problemIndex
        self.verdict = verdict

def readJsonFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as stream:
        data = json.load(stream)
    return data

def getJsonFile(url):
    data = requests.get(url, auth=(admin, password))
    return data.json()

def getJsonMetadata(filepath, url):
    if judgeMode == "local":
        return readJsonFile(filepath)
    else:
        return getJsonFile(url)

def getContestMetadata():
    contestMetadata = ContestMetadata(contestStart, contestDuration, contestFrozenTimeDuration, contestName, contestMode)
    return contestMetadata.__dict__

def getProblems():
    filepath = os.path.join(metadataDir, problemsFile)
    url = f'http://{judgeHost}/api/v4/contests/{contestId}/problems'
    problemsJson = getJsonMetadata(filepath, url)

    problems = []
    problemsById = {}
    for problem in problemsJson:
        index = problem["short_name"]
        problemId = problem["probid"]
        problems.append(Problem(index))
        problemsById[problemId] = index

    return [p.__dict__ for p in problems], problemsById

def getContestants():
    filepath = os.path.join(metadataDir, contestantsFile)
    url = f'http://{judgeHost}/api/v4/contests/{contestId}/teams'
    contestantsJson = getJsonMetadata(filepath, url)

    contestants = []
    teamsById = {}
    for team in contestantsJson:
        id = team["id"]
        name = team["name"]
        category = team["affiliation"] # affiliation was used to put the team category
        hidden = team["hidden"]
        if hidden:
            continue
        if name is None:
            continue
        teamsById[id] = name
        contestants.append(Contestant(id, name, category))

    return [c.__dict__ for c in contestants], teamsById


def getVeredicts(runsByJudgementId):
    veredictsByJudgementId = {}
    for run in runsByJudgementId:
        verdict = run["judgement_type_id"]
        if verdict not in veredictsByJudgementId:
            veredictsByJudgementId[verdict] = 0
        veredictsByJudgementId[verdict] += 1

    return veredictsByJudgementId


def getFinalVeredict(veredicts):
    if len(veredicts) == 1:
        return hashVeredict[next(iter(veredicts))]
    return hashVeredict["WA"]

def getJudgements():
    filespathJudgements = os.path.join(metadataDir, judgementsFile)
    url = f'http://{judgeHost}/api/v4/contests/{contestId}/judgements'
    judgementsJson = getJsonMetadata(filespathJudgements, url)

    judgementsById = {}

    for judgement in judgementsJson:
        submissionId = judgement["submission_id"]
        if submissionId not in judgementsById:
            judgementsById[submissionId] = []
        judgementsById[submissionId].append(judgement)

    return judgementsById

def getSubmissions(teamsById, problemsById):
    filepathSubmissions = os.path.join(metadataDir, submissionsFile)
    url = f'http://{judgeHost}/api/v4/contests/{contestId}/submissions'
    submissionsJson = getJsonMetadata(filepathSubmissions, url)

    judgementsById = getJudgements()
    submissions = []

    for submission in submissionsJson:
        contestTime = submission["contest_time"]
        problemId = submission["problem_id"]
        teamId = int(submission["team_id"])
        submissionId = submission["id"]

        if submissionId not in judgementsById:
            continue

        time = datetime.strptime(contestTime, "%H:%M:%S.%f")
        hours = time.hour
        minutes = time.minute
        timeSubmitted = hours*60 + minutes

        contestantName = teamsById[teamId]

        problemIndex = problemsById[problemId]

        veredicts = getVeredicts(judgementsById[submissionId])
        verdict = getFinalVeredict(veredicts)

        submissions.append(Submission(timeSubmitted, contestantName, problemIndex, verdict))

    return [s.__dict__ for s in submissions]

def domjudgeScoreboard():
    contestMetadata = getContestMetadata()
    problems, problemsById = getProblems()
    contestants, teamsById = getContestants()
    submissions = getSubmissions(teamsById, problemsById)
    scoreboardJson = {
        "contestMetadata" : contestMetadata,
        "problems" : problems,
        "contestants" : contestants,
        "verdicts" : verdicts,
        "submissions" : submissions,

    }

    return scoreboardJson