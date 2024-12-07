from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In_Review"),
    ("published", "Published"),
)

RATINGS = (
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid=ShortUUIDField(unique=True,length=10, max_length=20, prefix='cat', alphabet='abcdefghijklmnopqrstuvwxyz0123456789')
    title = models.CharField(max_length=255, default='Category Title')
    image = models.ImageField(upload_to='category', default= 'category.jpg')

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" height="50" width="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

class Tags(models.Model):
    pass
    
class Vendor(models.Model):
    vid=ShortUUIDField(unique=True,length=10, max_length=20, prefix='ven', alphabet='abcdefghijklmnopqrstuvwxyz0123456789')
    title = models.CharField(max_length=255, default='Shopify')
    image = models.ImageField(upload_to=user_directory_path,default= 'vendor.jpg')
    cover_image = models.ImageField(upload_to=user_directory_path,default= 'vendor.jpg')
    #description = models.TextField(null=True, blank=True, default='i am a vendor')
    description = RichTextUploadingField(null=True, blank=True, default='i am a vendor')

    address = models.CharField(max_length=100, default='123 Main Street, Nairobi.KE') 
    contact = models.CharField(max_length=100, default='+254745919342') 
    chat_resp_time = models.CharField(max_length=100, default='24/7')
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='7')
    warranty_period = models.CharField(max_length=100, default='100')


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" height="50" width="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid=ShortUUIDField(unique=True,length=10, max_length=20, prefix='prd', alphabet='abcdefghijklmnopqrstuvwxyz0123456789')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='product')

    title = models.CharField(max_length=255, default='Product Title')
    image = models.ImageField(upload_to=user_directory_path, default= 'product.jpg')
    #description = models.TextField(null=True, blank=True, default='This is a product description')
    description = RichTextUploadingField(null=True, blank=True, default='This is a product description')

    
    price = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default="2.99")

    #specification = models.TextField(null=True, blank=True)
    specification = RichTextUploadingField(null=True, blank=True)
    type = models.CharField(max_length=100, default='Organic', null=True, blank=True)
    stock_count = models.CharField(max_length=255, default='10',null=True, blank=True)
    life = models.CharField(max_length=255, default='100 days',null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add= False, null=True, blank=True)
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    tags = TaggableManager(blank=True)
    
    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review')

    status= models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)

    sku =ShortUUIDField(unique=True,length=4, max_length=10, prefix='sku', alphabet='0123456789')

    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" height="50" width="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.price/self.old_price )*100
        return new_price
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default= 'product.jpg')
    product = models.ForeignKey(Product, related_name ='p_images' , on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Images"


######################################## Cart,Order,Orderitems and Address ######################################
######################################## Cart,Order,Orderitems and Address ######################################
######################################## Cart,Order,Orderitems and Address ######################################
    
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS, max_length=30, default='processing')

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status= models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")
    total = models.DecimalField(max_digits=10, decimal_places=2, default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"
    

    def order_imag(self):
        return mark_safe('<img src="/media/%s" height="50" width="50" />' % (self.image))



######################################## Product Review,Wishlist, Address ######################################
######################################## Product Review,Wishlist, Address ######################################
######################################## Product Review,Wishlist, Address ######################################
######################################## Product Review,Wishlist, Address ######################################



class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices=RATINGS ,default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"


    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating
    

class Wishlist_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "wishlists"


    
    def __str__(self):
        return self.product.title
    
   
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)


class Transaction(models.Model):
    amount= models.DecimalField(max_digits=10, decimal_places=2)
    checkout_id = models.CharField(max_length=100,unique=True)
    mpesa_code = models.CharField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mpesa_code} - {self.amount} KSh"
    
