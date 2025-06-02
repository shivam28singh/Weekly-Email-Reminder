import requests
import pandas
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

response = requests.get("https://aijobs.net/");
soup = BeautifulSoup(response.text,"html.parser")

anchorTags = soup.find_all("a",class_="py-2")

prefix = "https://aijobs.net"
jobs_data = []
table_rows = ""
for aTag in anchorTags:
    url = prefix + aTag.get("href")
    company= aTag.find("span",class_="text-muted").text
    idx = company.find('\xa0')
    if(idx != -1):
        company = company[:idx]

    title = aTag.find("h5",class_="text-body-emphasis").text
    idx = title.find('\xa0')
    if(idx != -1):
        title = title[:idx]

    location = aTag.find("span",class_="text-break").text

    keywords = ""
    keywordResultset = aTag.find_all("span",class_="text-bg-light")
    for keyword in keywordResultset:
        keywords += keyword.text
        keywords += ', '
    keywords = keywords[:-1]

    jobs_data.append({
        "company":company,
        "title": title,
        "location":location,
        "keywords":keywords
    })

    table_rows += f"""
    <tr>
        <td><a href="{url}">{company}</a></td>
        <td>{title}</td>
        <td>{location}</td>
        <td>{keywords}</td>
    </tr>
    """

df = pandas.DataFrame(jobs_data)
print(df)

emailBody = """
<html>
<head>
<title> Job Opportunity </title>
<style>
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }}
    th {{
        background-color: #f2f2f2;
    }}
    tr:nth-child(even) {{
        background-color: #f9f9f9;
    }}
</style>
</head>
<body>
   <h2>Hi {userName},</h2>
   <p>We have curated a list of opportunities which you might be interested in. Please have a look!</p>
   
   <table>
       <thead>
           <tr>
               <th>Company</th>
               <th>Title</th>
               <th>Location</th>
               <th>Keywords</th>
           </tr>
       </thead>
       <tbody>
           {table_rows}
       </tbody>
   </table>
</body>
</html>
"""
     
emailBody = emailBody.format(userName="shivam",table_rows = table_rows)
print(emailBody)
msg = MIMEText(emailBody,"html")
msg["Subject"] = "AI Jobs Opportunity"
msg["From"] = "shivamsingh280501@gmail.com"
msg["To"] = "shivam.hunter01@gmail.com"

smtp = smtplib.SMTP("smtp.gmail.com",587)
smtp.starttls()
smtp.login("shivamsingh280501@gmail.com",GOOGLE_PASSCODE)
smtp.sendmail(msg["From"],msg["To"],msg.as_string())
smtp.quit()