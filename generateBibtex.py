import json
import os

json_folder = "./json/paper_info"
outfile = "references.bib"


with open(outfile, 'w') as f:
    f.write("\n")
    for filename in os.listdir(json_folder):
        if filename.endswith(".json"):
            print("Working on {}".format(filename))
            with open(os.path.join(json_folder, filename)) as j:
                citation = json.load(j)
                # field_list = ['Authors',
                #               'Publication date',
                #               'Journal',
                #               'Volume',
                #               'Issue',
                #               'Pages',
                #               'Publisher',
                #               'Description']

                label = filename
                author = ""
                title = ""
                journal = ""
                volume = ""
                year = ""
                pages = ""

                try:
                    author = citation["Authors"]
                except Exception as e:
                    print("Could not find author")
                    print(e)

                try:
                    title = citation["title"]
                except Exception as e:
                    print("Could not find title")
                    print(e)

                try:
                    journal = citation["Journal"]
                except Exception as e:
                    print("Could not find Journal")
                    print(e)

                try:
                    volume = citation["Volume"]
                except Exception as e:
                    print("Could not find Volume")
                    print(e)

                try:
                    year = citation["Publication date"].split('/')[0]
                except Exception as e:
                    print("Could not find Publication date")
                    print(e)

                try:
                    pages = citation["Pages"]
                except Exception as e:
                    print("Could not find Pages")
                    print(e)

                longstring = """

                """
                bibtex_string = """
\n
@article{{
{0},
author={{{1}}},
title={{{2}}},
journal={{{3}}}
volume={{{4}}}
year={5},
pages={{{6}}}
}}
\n""".format(label, author, title, journal, volume, year, pages)

                f.write(bibtex_string)
