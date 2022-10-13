from common import Component
from common import helpers
from clean_data import CleanData
import requests
import pickle
import json
import os

__all__ = ['GetJiraTicketDetails']

class GetJiraTicketDetails(Component):
    def __init__(self,
                 userid,
                 token,
                 project_name,
                 request_type,
                 file_location,
                 resolved_from_range='0d',
                 resolved_to_range='30d',
                 **kwargs):
        super().__init__(**kwargs)
        self.userid = userid
        self.token = token
        self.project_name = project_name
        self.request_type = request_type
        self.resolved_from_range = resolved_from_range
        self.resolved_to_range = resolved_to_range
        self.file_location = file_location
        self.kwargs = kwargs

    def _run(self):
        self.logger.info(f"Fetching details from Jira for last {self.resolved_from_range} to {self.resolved_to_range}")
        if not self.project_name and self.request_type and self.userid and self.token:
            self.logger.error("Please input all mandatory fields")
            return 1
        if not os.path.exists(self.file_location):
            self.logger.error(f"Seems {self.file_location} does not exists or KMP user is unable to access it")
            return 1

        request_string = f"search?jql=project='{self.project_name}'and'Customer Request Type'='{self.request_type}'" \
                         f"and resolved < -{self.resolved_from_range} and resolved > -{self.resolved_to_range}"

        '''request_string = f"search?jql=project='{self.project_name}'and'Flow Execution Component'='{self.request_type}'" \
        f"and resolved < -{self.resolved_from_range} and resolved > -{self.resolved_to_range}"'''

        resp, err = self._call_jira(request_string)
        if err:
            self.logger.error(f"Failed to get info because of error: {err}")
            return 1
        ticket_info = json.loads(resp)
        issues = ticket_info['issues']
        self.logger.info(f"Parsing and cleaning the fetched data ... ")
        err = self._parse_json_response(issues, self.file_location)
        if err:
            self.logger.error(f"Failed to get info because of parsing error: {err}")
            return 1

        total_no_of_tickets = ticket_info['total']
        tickets_fetched = ticket_info['maxResults'] + ticket_info['startAt']

        while tickets_fetched < total_no_of_tickets:
            self.logger.info(f"So far Fetched {tickets_fetched} tickets, Fetching next 100")
            resp, err = self._call_jira(request_string, start_at=tickets_fetched, max_results=100)
            if err:
                self.logger.error(f"Failed to get info because of error: {err}")
                return 1
            ticket_info = json.loads(resp)
            issues = ticket_info['issues']
            err = self._parse_json_response(issues, self.file_location)
            if err:
                self.logger.error(f"Failed to get info because of parsing error: {err}")
                return 1
            tickets_fetched = ticket_info['maxResults'] + ticket_info['startAt']

        with open(self.file_location, "r") as f:
            print(f.read())

    def _call_jira(self, request_string, start_at=0, max_results=50):
        session = helpers.JiraConnect(self.userid, self.token)
        if not (start_at == 0 and max_results == 50):
            request_string=f"{request_string}&startAt={start_at}&maxResults={max_results}"
        return session.get(request_string)

    @staticmethod
    def _parse_json_response(issues, file_location):
        ticket_description = ""
        for issue in issues:
            cleandata = CleanData()
            ticket_number = issue['key']
            ticket_summary = cleandata.apply_all_cleaning(issue['fields']['summary'])
            if (issue['fields']['description']) :
                ticket_description = cleandata.apply_all_cleaning(issue['fields']['description'])
            ticket_solution = issue['fields']['customfield_16815']

            if ticket_solution is None:
                ticket_solution = "cancelled"

            ticket_solution = cleandata.apply_all_cleaning(ticket_solution)

            ticket_details = (ticket_number, ticket_summary, ticket_description, ticket_solution)
            #ticket_details  = (x.encode('utf-8', 'ignore') for x in ticket_details)
            #ticket_details_string = str(b'&tag&'.join(ticket_details))
            try:
                with open(file_location,"a") as f:
                    f.write(','.join(ticket_details))
                    f.write("\n")
            except Exception as e:
                return str(e)