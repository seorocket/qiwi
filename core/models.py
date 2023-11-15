from django.db import models

class Task(models.Model):
    STATUS_CHOICES = (
        (1, 'Todo'),
        (2, 'In Progress'),
        (3, 'Done'),
    )
    qiwi_wallet = models.CharField(max_length=20)
    qiwi_pass = models.CharField(max_length=50)
    phones = models.TextField()
    amount = models.IntegerField('Сумма (₽)')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task for {self.qiwi_wallet} - {self.amount}"

class TaskLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    log_entry = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for Task {self.task.qiwi_wallet} - {self.timestamp}"