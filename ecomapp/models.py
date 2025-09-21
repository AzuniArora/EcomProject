from django.db import models

# Create your models here.

class Dummy(models.Model):
	fname=models.CharField(max_length=15)
	lname=models.CharField(max_length=15)

class faq(models.Model):
	que=models.TextField()
	ans=models.TextField()

class Category(models.Model):
	category_name=models.CharField(max_length=155,primary_key=True)

class products(models.Model):
     category_name=models.ForeignKey(Category,on_delete=models.CASCADE)
     Title=models.CharField(max_length=155,primary_key=True)
     Company=models.CharField(max_length=155)
     unit_price=models.DecimalField(max_digits=10,decimal_places=2)
     quantity=models.IntegerField()
     image=models.ImageField(upload_to="data",blank=True, null=True)
     description=models.TextField()

class Mycontact(models.Model):
	name=models.CharField(max_length=100)
	email=models.EmailField()
	message=models.TextField()
	phone_no=models.CharField(max_length=15)


class Register1(models.Model):
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	email=models.EmailField()
	password=models.CharField(max_length=100)
	retype_password=models.CharField(max_length=100)
	phone_no = models.CharField(max_length=15, null=True, blank=True, default=None)
	address = models.CharField(max_length=255, null=True, blank=True, default=None)
	landmark = models.CharField(max_length=255, null=True, blank=True, default=None)
	pincode = models.CharField(max_length=10, null=True, blank=True, default=None)
	house_flat_no = models.CharField(max_length=100, null=True, blank=True, default=None)



class Cart(models.Model):
	user = models.ForeignKey(Register1, on_delete= models.CASCADE)
	product = models.ForeignKey(products, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	added_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"(self.user.first_name)'s cart - (self.product.Title)"

	def total_price(self):
		return float(self.product.unit_price) * self.quantity



class Payment(models.Model):
	user = models.ForeignKey(Register1, on_delete=models.CASCADE)
	payment_id = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=10,decimal_places=2)
	status = models.CharField(max_length=20, choices=[("Success", "Success"), ("Failed", "Failed")])
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Payment {self.payment_id} - {self.status}"

class OrderItem(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(products, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

class ShippingAddress(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(Register1, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='Home')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
		

class ChatMessage(models.Model):
	user = models.CharField(max_length=100)
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)