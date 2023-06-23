import json
from utilities import *

sections = {}
# Opening JSON file
with open('info.json') as json_file:
    sections = json.load(json_file)

tex_string = r"""% This template is designed to offer an aesthetically pleasing resume that adheres to a formal and institutional tone, making it suitable for applications to companies and research centers requiring a high degree of professionalism. Navy blue has been chosen as the primary color to align with these objectives.
% The code is well-documented and annotated, allowing users to easily customize and modify it according to their needs. Please note that the template's content is meant to be humorous and should not be taken literally. We are grateful for your interest in using this template for your professional endeavors.
% Author: Christian Maria Giannetti

%----------------------------------------------------------------------------------------
%  Packages And Other Document Configurations
%----------------------------------------------------------------------------------------

\documentclass{resume} % Use the custom resume.cls style

% Document margins
\usepackage[left=0.75in,top=0.6in,right=0.75in,bottom=0.6in]{geometry}

% Color and hyperlink packages
\usepackage{xcolor}
\usepackage{hyperref}

% Footnote and margin adjustment packages
\usepackage{footnote}
\usepackage{changepage} 

% Fontawesome package for icons
\usepackage{fontawesome}

% Tabularx package for custom tables
\usepackage{tabularx}

% Define navyblue color
\definecolor{navyblue}{RGB}{0,54,123}

%----------------------------------------------------------------------------------------
%   Customizations
%----------------------------------------------------------------------------------------

% Define italicitem, bolditem, and plainitem commands
\newcommand{\italicitem}[1]{\item{\textit{#1}}}
\newcommand{\bolditem}[1]{\item{\textbf{#1}}}
\newcommand{\plainitem}[1]{\item{#1}}

% Define user-friendly link command for hyperlinks
\newcommand{\link}[2]{{\href{#1}{#2}}}

\newcommand{\entry}[2]{#1 & #2 \tabularnewline} % Defines an entry with two arguments: #1 for the first column and #2 for the second column

%----------------------------------------------------------------------------------------
%   Define envsection command for defining a new environment section
%----------------------------------------------------------------------------------------

\newcommand{\tableEnv}[2]{%
  \begin{rSection}{#1} % Begin rSection with the given name
    \begin{adjustwidth}{0.0in}{0.1in} % Set the left and right margins
      \begin{tabularx}{\linewidth}{@{} >{\bfseries}l @{\hspace{6ex}} X @{}}
        #2 % Print the content inside the tabularx environment
      \end{tabularx}
    \end{adjustwidth}
  \end{rSection}
}

%----------------------------------------------------------------------------------------
%   Begin document
%----------------------------------------------------------------------------------------

% Set name with navyblue color
"""
try:
    email = sections['Basic Info']['contact_info']['Email']
    email_link = sections['Basic Info']['contact_info']['Email_link']
except:
    email = 'abc@gmail.com'
    email_link = ''

try:
    contact = sections['Basic Info']['contact_info']['Phone']
except:
    contact = 'XXXXXXXXXX'

try:
    linkedin_link = sections['Basic Info']['contact_info']['Profile_link']
except:
    linkedin_link = ''

tex_string = tex_string + r"""
\name{\color{navyblue} """+sections['Basic Info']['name']+r"""}

\begin{document}

\printPersonalInfo{
  \personalInfo{\tag{E-mail}\info{"""+email+r"""} \tag{Telephone number}\info{+91-"""+contact+r"""}}
  \personalInfo{\tag{LinkedIn}\info{"""+linkedin_link+r"""}}
  }"""

if sections['Education']:
    tex_string = tex_string + r"""
%----------------------------------------------------------------------------------------
%   Education section
%----------------------------------------------------------------------------------------
    \begin{rSection}{Education}
    """

    #   % Master's degree entry
    for ed in sections['Education']:
        try:
            tex_string = tex_string + r"""
\begin{rSubsectionNoBullet}{\bf """+ed['1']+"""}{}{"""+ed['2']+"""}{"""+ed['3']+"""}
\end{rSubsectionNoBullet}
\hfill
"""     
        except:
            pass
    tex_string = tex_string + r"\end{rSection}"

if sections['Experience']:
    tex_string = tex_string + r"""
%----------------------------------------------------------------------------------------
%   Work experience section
%----------------------------------------------------------------------------------------

\begin{rSection}{Work experience}"""
    for ex in sections['Experience']:
        if 'experiences' in ex:
            print('entering company with multiple sections')
            company = ex['company']
            loc_ = None
            if 'location' in ex:
                loc_ = ex['location']
            for exx in ex['experiences']:
                print('......entering experience for that company')
                date_ = exx['date']
                position_ = exx['position']
                if (not loc_) and ('location' in exx):
                    loc_ = exx['location']
                else:
                    loc_ = ""
                tex_string = tex_string + r"""
\begin{rSubsection}{"""+company+"}{"+date_+"}{"+position_+r"}{"+loc_+"}"
                
                if 'description' in exx:
                    des_pts = improve_content("format this description for my resume in bullet points- " + ex['description']).split('\n')
                else:
                    des_pts = improve_content("generate my Experience description for my linkedin profile in bullet points - " + '. '.join(list(exx.values()))).split('\n')[:4]
                for pt in des_pts:
                    if len(pt)<5:
                        continue
                    pt = ' '.join(pt.split()[1:])
                    tex_string = tex_string + """
                    \item """+pt
                tex_string = tex_string + """
\end{rSubsection}"""
        else:
            print('entering company with single sections')
            company = ex['company']
            date_ = ex['date']
            position_ = ex['position']
            try:
                loc_ = ex['location']
            except:
                loc_ = ""
            tex_string = tex_string + r"""
\begin{rSubsection}{"""+company+"}"+ "{"+date_+"}{"+position_+"}{"+loc_+"}" 
            if 'description' in ex:
                des_pts = improve_content("format this description for my resume in bullet points- " + ex['description']).split('\n')
            else:
                des_pts = improve_content("generate my Experience description for my linkedin profile in bullet points - " + '. '.join(list(ex.values()))).split('\n')[:4]
            for pt in des_pts:
                if len(pt)<5:
                    continue
                pt = ' '.join(pt.split()[1:])
                tex_string = tex_string + """
                \item """+pt
            tex_string = tex_string + """
\end{rSubsection}"""
        
    tex_string = tex_string + r"""
\end{rSection}"""

# if sections['Volunteering'] or sections['Organizations']:
#     tex_string = tex_string + r"""%----------------------------------------------------------------------------------------
# %% Language proficiencies section
# %----------------------------------------------------------------------------------------

# \tableEnv{Language proficiencies}{
#     \entry{English}{Fluent in Shakespearean insults}
#     \entry{French}{Proficient in baguette related jokes}
# }"""

if sections['Skills']:
    tex_string = tex_string + r"""
%----------------------------------------------------------------------------------------
% Technical skills section
%----------------------------------------------------------------------------------------

\tableEnv{Skills}{
    \entry{Programming Languages/Tools}{"""+', '.join([x['1'] for x in sections['Skills']])+"""}
}"""

if sections['Projects']:
    tex_string = tex_string + r"""
%----------------------------------------------------------------------------------------
%%   Projects section
%----------------------------------------------------------------------------------------

\begin{rSection}{Projects}"""
    for project in sections['Projects']:
        date=''
        location=''
        if 'date' in project:
            date = project['date']
        if 'location' in project:
            location = project['location']
        tex_string = tex_string + r"""
    \begin{rSubsection}{"""+project['name']+r"}{"+date+"}{"+location+r"}{}"
        if 'description' in project:
            des_pts = improve_content("format this description for my resume in bullet points-  " + project['description']).split('\n')
        else:
            des_pts = improve_content("generate my Project work description for my linkedin profile in bullet points - " + '. '.join(list(project.values()))).split('\n')[:4]
        for pt in des_pts:
            if len(pt)<5:
                continue
            pt = ' '.join(pt.split()[1:])
            tex_string = tex_string + """
            \item """+pt
        tex_string = tex_string + """
    \end{rSubsection}"""

    tex_string = tex_string + r"""
    \end{rSection}
    """

if sections['Licenses & certifications']:
    tex_string = tex_string + r"""%----------------------------------------------------------------------------------------
% Most relevant projects section
%----------------------------------------------------------------------------------------

\begin{rSection}{Certifications}{"""
    for cert in sections['Licenses & certifications']:
        name = cert['1']
        site = cert['2']
        # time.sleep(5)
        # des = improve_content("One line description for the course - {} from {}".format(name, site))
        # time.sleep(5)
        tex_string = tex_string + "\n\item{$\sbullet[.65]$} "+"{} | {}".format(name, site)
    tex_string = tex_string + "\n}"

if sections['Honors & awards']:
    tex_string = tex_string + r"""
%----------------------------------------------------------------------------------------
% Organization section
%----------------------------------------------------------------------------------------

\tableEnv{Achievements}{
    \entry{Couch Potatoes Anonymous}{A support group for those addicted to binge-watching TV shows}
    \entry{Procrastinators' Club}{A group that will eventually get around to doing something, someday}
}"""

tex_string = tex_string + r"\end{document}\n"

with open('texfile.tex', 'w') as fout:
    fout.write(tex_string)