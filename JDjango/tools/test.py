# # def __str__(self):
# {str_msg}

# # def get_absolute_url(self):
# #     from django.urls import reverse
# #     return reverse('', args=[])

# def save(self, *args, **kwargs):
#     # 注意：bulk_create()和update()不会触发save()
#     super().save(*args, **kwargs) # 确保对象正确写入数据库