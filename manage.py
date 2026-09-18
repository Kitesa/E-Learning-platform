from django.utils.timezone import now
# Import your educational models here
# from your_app.models import Program, Application, ForumPost, UserProfile

def dashboard_callback(request, context):
    """
    Injects metrics for your educational ecosystem (Users, Programs, Forums, Notifications, Applications).
    """
    # Example queries (Swap with your actual models/aggregations)
    # active_students = UserProfile.objects.filter(role="student", is_active=True).count()
    # active_programs = Program.objects.filter(is_active=True).count()
    # total_applications = Application.objects.count()
    
    context.update({
        # High-level educational statistics
        "total_active_students": "1,234",
        "total_programs": "12",
        "total_applications_received": "3,456",
        
        # Chart Data Array (representing daily registration or application spikes over 31 days)
        "analytics_labels": [str(i) for i in range(1, 32)], 
        "analytics_data": [15, 28, 20, 55, 42, 31, 75, 48, 40, 85, 62, 50, 95, 78, 60, 110, 92, 70, 88, 64, 52, 105, 125, 90, 78, 92, 98, 112, 135, 118, 145],
        
        # Program enrollment volume sidebar breakdown
        "program_breakdown": [
            {"name": "Computer Science Degree", "count": "450 Students"},
            {"name": "Data Analytics Bootcamp", "count": "320 Students"},
            {"name": "UI/UX Design Certificate", "count": "280 Students"},
            {"name": "Digital Marketing Short Course", "count": "184 Students"},
        ],
        
        # Real-time alert/action tracking status percentages
        "application_review_status": 83,
        "forum_moderation_status": 89,
        "notification_delivery_status": 93,
    })
    
    return context
