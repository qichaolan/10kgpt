import logging
from sec_api import ExtractorApi, QueryApi, XbrlApi

MAX_TOKENS_CNT = 3000

class SEC:    
    def __init__(self, my_api_key):
        self.queryApi = QueryApi(api_key=my_api_key)
        self.extractorApi = ExtractorApi(api_key=my_api_key)
        self.xbrlApi = XbrlApi(api_key=my_api_key)

    def get_10K_urls(self, stock: str, start_date: str, end_date: str):
        query = {
            "query": { "query_string": { 
                "query": "ticker:" + stock +
                    " AND filedAt:{" + start_date + " TO " + end_date + "}" +
                    " AND formType:\"10-K\"" + 
                    " AND NOT formType:\"NT 10-K\"" + 
                    " AND NOT formType:\"10-K/A\""
                } },
            "from": "0",
            "size": "10",
            "sort": [{ "filedAt": { "order": "desc" } }]
            }

        response = self.queryApi.get_filings(query)

        # no more filings in search universe
        if not response["filings"]:
            logging.warning("No filings found for the given query.")
            return []

        return [filing["linkToFilingDetails"] for filing in response["filings"]]

    def __get_text_from_10K(self, filing_url: str, section: str):
        return self.extractorApi.get_section(filing_url, section, "text")

    # Financial Statements and Supplementary Data
    def get_section_8(self, filing_url: str):
        return self.__get_text_from_10K(filing_url, "8")

    # Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations
    def get_section_7(self, filing_url: str):
        return self.__get_text_from_10K(filing_url, "7")

    def access_financial_statements(self, filing_url: str):
        return self.xbrlApi.xbrl_to_json(htm_url=filing_url)

    def section_7_to_list(self, filing_url: str):
        text = self.get_section_7(filing_url)

        token_lst = []
        tokens = ""
        token_count = 0
        max_tokens = MAX_TOKENS_CNT

        for line in text.splitlines():
            line_token_count = len(line.split(" ")) 
            
            # skip line if it has less than 20 tokens
            if line_token_count < 20:
                continue
            
            # add line to current tokens if it does not exceed the maximum token count
            if token_count + line_token_count <= max_tokens:
                tokens += line
                token_count += line_token_count
            # if it exceeds the maximum token count, 
            # add the current tokens to the list and reset the token count and tokens
            else:
                token_lst.append(tokens)
                tokens = line
                token_count = line_token_count

        # add the final set of tokens to the list
        token_lst.append(tokens)

        return token_lst