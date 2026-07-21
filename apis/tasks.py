from celery import shared_task
import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task
def generate_daily_attendance_report():
    print("Starting generation of daily attendance report...")
    time.sleep(5)  # Simulate a heavy DB query or file generation
    
    # Broadcast to WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'notification_message',
            'message': 'Daily attendance report has been generated successfully!'
        }
    )
    
    print("Daily attendance report generated and broadcasted successfully.")
    return "Report Generated"
