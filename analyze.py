'''
    @author: Qichao Lan
'''

#url = "https://www.sec.gov/Archives/edgar/data/1318605/000095017022000796/tsla-20211231.htm"
from sec import SEC
from chat import ChatGPT
from os import path
import argparse
import yaml
import sys
import argparse
import sys
import yaml

class FinancialStatementAnalyzer:
    """
    A tool for analyzing financial statements.
    """

    def __init__(self, key_yaml: str):
        """
        Initialize the analyzer with the API and chatbot keys from a YAML file.

        :param key_yaml: the file path to the YAML file containing the API and chatbot keys
        """
        try:
            with open(key_yaml, "r") as stream:
                data = yaml.safe_load(stream)
                self.SEC_API_KEY = data.get("SEC_API_KEY")
                self.CHATGPT_KEY = data.get("CHATGPT_KEY")
        except FileNotFoundError:
            print(f"Error: YAML file '{key_yaml}' not found.")
            sys.exit(-1)
        except yaml.YAMLError as exc:
            print(f"Error loading YAML: {exc}")
            sys.exit(-1)

        self.SEC_API = SEC(self.SEC_API_KEY)
        self.CHATGPT = ChatGPT(self.CHATGPT_KEY)

    def summarize_financial_statement(self, url: str) -> str:
        """
        Summarize a financial statement.

        :param url: the URL of the 10-K statement to summarize
        :return: a summary of the financial statement
        """
        summary = ""
        for tokens in self.SEC_API.section_7_to_list(url):
            summary += self.CHATGPT.summarize_financial_statements(tokens)
        return self.CHATGPT.finalize_statements(summary)

    @staticmethod
    def main(argv):
        """
            Main method for the financial statement analyzer tool
        """
        parser = argparse.ArgumentParser(description='Financial statement analysis tool.')
        parser.add_argument("-k", "--key", type=str, required=True, help="Path to YAML file with necessary keys")
        parser.add_argument("-u", "--url", type=str, required=True, help="URL of 10-K statement to analyze")

        args = parser.parse_args()
        if not path.exists(args.key):
            print("Invalid YAML file. Aborting.")
            exit(-1)
        
        analyze = FinancialStatementAnalyzer(args.key)
        print("\n########################################################\n")
        print(analyze.summarize_financial_statement(args.url))
        print("\n########################################################\n")

if __name__ == '__main__':
    exit(FinancialStatementAnalyzer.main(sys.argv[1:]))