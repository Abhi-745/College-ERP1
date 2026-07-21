from celery import shared_task
import time

@shared_task
def generate_daily_attendance_report():
    # Mock task to simulate generating a heavy report in the background
    print("Starting generation of daily attendance report...")
    time.sleep(5)  # Simulate a heavy DB query or file generation
    print("Daily attendance report generated successfully.")
    return "Report Generated"
