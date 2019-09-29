"""
This implement custom errors used across the project
"""


class UserNotSubscribedException(Exception):
    pass


class AnswerNotFoundException(Exception):
    def __init__(self, invalid_answers, max_index):
        super(AnswerNotFoundException, self).__init__()
        self.invalid_answers = ", ".join(invalid_answers)
        self.max_index = max_index


class AlreadyVotedException(Exception):
    pass


class SurveyNotFoundException(Exception):
    def __init__(self, survey_id):
        super(SurveyNotFoundException, self).__init__()
        self.survey_id = survey_id


class InvalidSurveyIdException(Exception):
    def __init__(self, survey_id):
        super(InvalidSurveyIdException, self).__init__()
        self.survey_id = survey_id


class CommandSyntaxException(Exception):
    pass
