from django.db import models

# Create your models here.
#The choices may be cup level but if any thing better pls do change.
STAT_CHOICES= (
	('O','Open')
	('C','Completed')
	('L','Overdue')
	('N','Almost')
)
class Task(models.Model):

	subject        = models.CharField(max_length=100 , null=True , blank=True)
	description    = models.TextField(null=True , blank=True)
	creator        = models.ForeignKey(User , related_name = "tasks_assigned")
	creation_date  = models.DateTimeField (auto_now = True, editable = False)
	assignee    = models.ManyToManyField(User, related_name = "tasks")
	deadline       = models.DateTimeField(null=True , blank=True)
	status         = models.TextField(max_length=50,choices=STAT_CHOICES,default='OPEN')	
	department=models.ManyToManyField(Department, related_name = "tasks_dept")
	manager=models.ManyToManyField(User,related_name="tasks_monitored")

class Comment (models.Model):
    """Model to store a comment.

    Timestamp helps to order comments.
    Author can be used to select particular comments based on the author.
    """

    author = models.ForeignKey (User)
    comment_string = models.TextField ()
    time_stamp = models.DateTimeField (auto_now = True, editable = False)
