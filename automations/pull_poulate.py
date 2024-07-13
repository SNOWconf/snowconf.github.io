#!/usr/bin/python3
# This script was based on https://gist.github.com/vmx/02d1ee691d681274b4387510f8e0b5f0
# and the parsing code comes from ChatGPT 
# This script is to get all the data from a pretalx endpoint that needs paging.
import argparse
import json
import sys
import urllib.request

edition = "2025"
token = "3948997e9eae1242ed70e27171662454decb3b8e"
url = "https://cfp.snowcon.info/api/events/test-2/"
state= "submitted" # Should be changed to "confirmed" in prod.

# URLs for submissions and answers endpoints
submissions_url = url + 'submissions/'
answers_url = url + 'answers/'


# `combined` is the final output, it's the combined result of all requests
combined = {
    'submissions': [],
    'answers': []
}

# Function to fetch data from a given URL and add to combined
def fetch_and_add(url, target_key, token):
    while url:
        print(f'{url}', file=sys.stderr)

        req = urllib.request.Request(url, headers={
            'Authorization': f'Token {token}'
        })

        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)

            if isinstance(data, dict) and 'results' in data:
                results = data['results']
            else:
                results = []

            combined[target_key].extend(results)

            url = data.get('next')

# Function to print speaker details in Hugo shortcode format
def print_speaker_details(speakers, answers, file):
    for speaker in speakers:
        answer = get_speaker_answer(speaker['code'], answers)
        bio_with_line_breaks = speaker.get("biography", "").replace("\r\n", "  ")
        file.write(f'{{{{< speaker img="{speaker.get("avatar", "")}" name="{speaker.get("name", "")}" title="{answer}" bio="{bio_with_line_breaks}" >}}}}\n\n')

# Function to get speaker's answer based on their code
def get_speaker_answer(code, answers):
    answer = next((ans['answer'] for ans in answers if ans.get('person') == code and ans['question']['id'] == 7), "")
    return answer

# Function to generate sessions.md file
def generate_sessions_markdown(submissions, answers, file):
    file.write("---\n")
    file.write('title: "Sessions"\n')
    file.write('menu: "Conference"\n')
    file.write('weight: 2\n')
    file.write("---\n\n")

    session_types = {
        "Keynote": [],
        "Talk": []
    }

    # Group sessions by type
    for submission in submissions:
        submission_type = submission.get("submission_type", {}).get("en", "")
        if submission_type in session_types:
            session_types[submission_type].append(submission)

    # Write Keynote and Talk sections with sessions
    for session_type, sessions in session_types.items():
        file.write(f'# {session_type}\n\n')
        for submission in sessions:
            code = submission.get('code', '')
            image = submission.get('image', '')
            speakers = submission.get('speakers', [])
            name = speakers[0].get('name', '') if speakers else ''
            title = get_speaker_answer(speakers[0]['code'], answers) if speakers else ''
            session_title = submission.get('title', '')
            url_name = name.replace(" ", "-")
            url = f"/{code}-{url_name}/"

            shortcode = (
                '{{{{< session img="{image}" url="{url}" name="{name}" '
                'title="{title}" session-title="{session_title}" >}}}}\n\n'
            ).format(
                image=image, url=url, name=name, title=title, session_title=session_title
            )

            file.write(shortcode)

# Fetch submissions data
fetch_and_add(submissions_url, 'submissions', token)

# Fetch answers data
fetch_and_add(answers_url, 'answers', token)

# Open speakers.md and sessions.md files in write mode
with open('speakers.md', 'w', encoding='utf-8') as speakers_file, \
     open('sessions.md', 'w', encoding='utf-8') as sessions_file:
    
    # Write speakers.md
    speakers_file.write("---\n")
    speakers_file.write('title: "Speakers"\n')
    speakers_file.write('menu: "Conference"\n')
    speakers_file.write('weight: 1\n')
    speakers_file.write("---\n\n")

    # Print Keynotes and Talks in speakers.md
    for session_type in ["Keynote", "Talk"]:
        speakers_file.write(f"# {session_type}\n\n")
        for submission in combined['submissions']:
            if submission.get("submission_type", {}).get("en", "") == session_type:
                speakers = submission.get("speakers", [])
                print_speaker_details(speakers, combined['answers'], speakers_file)

    # Generate sessions.md
    generate_sessions_markdown(combined['submissions'], combined['answers'], sessions_file)
