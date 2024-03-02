from django.db.models import Count, Avg
from datetime import datetime

# Lấy năm hiện tại
from theses.models import Score, Student

current_year = datetime.now().year

# Tính tổng hợp điểm theo năm
score_statistics = Score.objects.filter(thesis__created_date__year=current_year).aggregate(
    total_scores=Count('id'),
    average_score=Avg('score')
)



participation_frequency = Student.objects.values('major__name').annotate(
    total_participants=Count('id')
)

