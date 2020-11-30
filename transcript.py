import subprocess
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import argparse


def get_name(course: str, code: str) -> str:
    url = f"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept={course}" \
          f"&course={code}"
    res = requests.get(url)
    html_page = res.content

    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    name = text[19][11:-23]
    formatted = []
    line = ""
    for word in name.split():
        if len(line) + len(word) < 40:
            line += f" {word}"
        else:
            formatted.append(line[1:])
            line = f" {word}"
    formatted.append(line[1:])

    name = "\\\\".join(formatted)
    return name


def raw_doc(data, name, add_col):
    return f"""\\documentclass{{article}}
\\usepackage[paper=letterpaper,left=20mm,right=20mm,top=3cm,bottom=2cm]{{geometry}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{fancyhdr}}
\\pagestyle{{fancy}}
\\usepackage{{longtable}}
\\usepackage{{makecell}}
\\usepackage[makeroom]{{cancel}}

\\lhead{{{name}}}
\\rhead{{University of British Columbia}}
\\renewcommand{{\\headrulewidth}}{{0.4pt}}

\\begin{{document}}
\\subsection*{{Unofficial Transcript of Records}}
    \\begin{{longtable}}{{{"|c" if add_col else ""}|l|c| c|  c|c |}}
    \\hline
    {"Course Name &" if add_col else ""}Course Code & Grade & Letter & Year of Study & Class Average\\\\\\hline\\hline
    {data}
 \\end{{longtable}}
\\end{{document}}"""


def generate_transcript(name, course_names, compile_pdf, data):
    rows = []

    with open(data, 'r') as f:
        raw_data = f.read()

    for line in tqdm(raw_data.split('\n')):
        values = line.split('\t')
        try:
            if values[2].strip() == '':
                print(f'{values[0]} has no grade. Ignoring.')
            else:
                if course_names:
                    rows.append(
                        f'\\thead{{{get_name(*values[0].split())}}}&{values[0]} & {values[2]} & {values[3]} & {values[7]} & {values[9]} \\\\ \\hline')
                else:
                    rows.append(f'{values[0]} & {values[2]} & {values[3]} & {values[7]} & {values[9]} \\\\ \\hline')
        except IndexError:
            print(f"Parse error in {line}. Ignoring.")

    rd = raw_doc('\n'.join(rows), name, course_names)

    with open("transcript.tex", 'w') as f:
        f.write(rd)

    if compile_pdf:
        subprocess.call(['pdflatex', 'transcript.tex'])
        subprocess.call(['rm', 'transcript.log', 'transcript.aux'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, help='Your full name')
    parser.add_argument('--data', type=str, default='mydata.txt',
                        help='Path to the text file containing your grades copied directly from the ssc.'
                             '\nDefaults to `mydata.txt`'
                             '\nSee https://github.com/tomginsberg/transcript-generator for more instructions')
    parser.add_argument('--compile', default=False, help='[flag] If passed compiles pdf with pdflatex',
                        action='store_true')
    parser.add_argument('--descriptive', default=False,
                        help='[flag] If passed add a column of course names fetched from UBC course catalogue',
                        action='store_true')
    args = parser.parse_args()
    generate_transcript(name=args.name, course_names=args.descriptive, compile_pdf=args.compile, data=args.data)
