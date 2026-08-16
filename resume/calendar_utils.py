from datetime import datetime, timedelta

def generate_ics(job_title, company, interview_datetime, duration_minutes=60, notes=""):
    end_time = interview_datetime + timedelta(minutes=duration_minutes)

    dt_format = "%Y%m%dT%H%M%S"
    start_str = interview_datetime.strftime(dt_format)
    end_str = end_time.strftime(dt_format)
    now_str = datetime.now().strftime(dt_format)

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//AI Job Search Assistant//EN
BEGIN:VEVENT
UID:{now_str}@jobsearchassistant
DTSTAMP:{now_str}
DTSTART:{start_str}
DTEND:{end_str}
SUMMARY:Interview - {job_title} at {company}
DESCRIPTION:{notes}
LOCATION:{company}
BEGIN:VALARM
TRIGGER:-PT30M
ACTION:DISPLAY
DESCRIPTION:Interview reminder
END:VALARM
END:VEVENT
END:VCALENDAR"""

    return ics_content