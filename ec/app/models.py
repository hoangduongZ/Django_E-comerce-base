from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES=(
    ('DELL','DELL'),
    ('LENOVO','LENOVO'),
    ('HP','HP'),
    ('ASUS','ASUS'),
    ('MSI','MSI'),
    ('MACBOOK','MACBOOK'),
)

STATE_CHOICES = (
    ('Thai Binh', 'Thai Binh'),
    ('Ha Noi', 'Ha Noi'),
    ('Ho Chi Minh', 'Ho Chi Minh'),
    ('Da Nang', 'Da Nang'),
    ('Hai Phong', 'Hai Phong'),
    # Thêm các tỉnh thành khác vào đây
)

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.IntegerField()
    discounted_price = models.IntegerField()
    description = models.TextField()
    composition= models.TextField(default='')
    prodapp= models.TextField(default='')
    category = models.CharField(choices= CATEGORY_CHOICES, max_length=10)
    product_image = models.ImageField(upload_to='product')
    # Định nghĩa object thể hiện dưới dạng chuỗi trong Django Admin
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user =  models.ForeignKey(User, on_delete= models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    zipcode=  models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    # Định nghĩa object thể hiện dưới dạng chuỗi trong Django Admin
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivery','Delivery'),
    ('Cancel','Cancel'),
    ('Pending','Pending')
)
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length= 50,choices= STATUS_CHOICES, default="Pending")
    @property 
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)