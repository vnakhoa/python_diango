


from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse, JsonResponse
from .models import Product, Order, OrderItem, Customer
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from django.core.paginator import Paginator
from .form import Register, Login, CreateProduct

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from django.contrib.auth.hashers import make_password


# 2. Exempt the view from CSRF checks
from django.views.decorators.csrf import csrf_exempt



from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets

from .serializers import GroupSerializer, UserSerializer

from rest_framework.views import APIView

class SnippetList(APIView):
    permission_classes = [permissions.IsAuthenticated]


    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Customer.objects.all()
        print('>>>>>>>get :', request.data)
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print('>>>>>>>post :', request.data)
        hashPass = make_password(str(request.data['password']))

        print('hashPass: ', hashPass )

        request.data['password'] = hashPass
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SnippetDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserSerializer(snippet)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





#Form
# from django.contrib.auth.forms import UserCreationForm

#chuyển hướng khi vào trang
def redirect_home(request):
    return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('home') 

def register(request):
    if request.method == 'POST':
        form = Register(request.POST)
        context = {'form': form}

        print(">>>>>>>>>> requesst >>>>>>>: ", form)
        if form.is_valid():
            print(">>>>>>>>>> POST IS_VALID >>>>>>>: ", request.POST)
            user = form.save(commit=False)  # chưa lưu dữ liệu vào cơ sở dữ liệu ngay, để băm password

            user.set_password(request.POST['password'])
            user.save() #Lưu chính thức
            return redirect('home') # Chuyển hướng sau khi lưu thành công
        else:
            print('Không VALID thông tin người dùng')
    else:
        form = Register()
        context = {'form': form}
    return render(request, "app/register.html", context)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        form = Login(request.POST)
        context = {'form': form}

        print(">>>>>>>>>> POST IS_VALID >>>>>>>: ", request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            print("user đăng nhập")
            # return redirect('home')  # Chuyển hướng sau khi lưu thành công
            return HttpResponse('đã đăng nhập')
        else:
            print("user KHÔNG đăng nhập")
            return HttpResponse('Tên đăng nhập hoặc mật khẩu không đúng')
    else:
        form = Login()
        context = {'form': form}
    return render(request, "app/login.html", context)



# Create your views here.
def homepage(request):
    #Tất cả products
    product = Product.objects.all()


    # Số lượng sản phẩm trên mỗi trang
    items_per_page = 3   
    # Tạo một đối tượng Paginator
    paginator = Paginator(product, items_per_page)
    # Lấy số trang từ tham số truyền vào hoặc mặc định là trang đầu tiên
    page_number = request.GET.get('page', 1)
    # Lấy các sản phẩm cho trang cụ thể
    page_products = paginator.get_page(page_number)

    print(">>>>>>>>>>>>>>>>>>>>>KHÔNG ngoài: ", page_products,"   ; ", page_number, "   ; ",paginator )

    if request.GET :
        if request.GET.get('search', None):
            print(">>>>>>>>>>>>>>>>>>>>> CÓ: ", request.GET)
            search = request.GET['search']
            product = Product.objects.filter(product__icontains = search)
            return render(request, "app/search.html",{"product": product}) 
        #####
        return render(request, 'app/home.html', {'product': page_products})    
    else:
        print(">>>>>>>>>>>>>>>>>>>>>KHÔNG: " )
        return render(request, "app/home.html",{"product": page_products})     




def cart_view(request, product_id):
    product = Product.objects.get(pk = product_id)
    print(">>>>>>>>>> product_id", product)
    return render(request, "app/home.html",{"product": [product]}) 


def add_to_cart(request):
    if(request.user.is_authenticated == False) :
        return redirect('login')
    else:
        if(request.method == "POST"):
            product_id = request.POST['id']
            print('>>>>>>>>>: productID', product_id)

            order, created = Order.objects.get_or_create(customer = request.user)
            product = Product.objects.get(id = int(product_id))

            choose_product, created = OrderItem.objects.get_or_create(order = order, product = product)
            print('>>>>>>>>>>>>>>>>>>>>>> Vào Add_cart', product_id, "<<<===>>>", order,"<<<===>>>", product,"<<<===>>>", choose_product)

            if created:
                choose_product.quantity = 1
                choose_product.save()
            else:
                OrderItem.objects.filter(order=order, product=product).update(quantity=F('quantity') + 1)
        return redirect('cart')


def incre_descrea(request):
    if(request.method == "POST"):
        action = request.POST['action_todo']
        product_id = request.POST['id']

        order = Order.objects.get(customer = request.user)
        choose_product = OrderItem.objects.get(order = order, id = product_id)

        if str(action) == "increase":
            choose_product.quantity +=1
            choose_product.save()
        elif str(action) == "descrease":
            choose_product.quantity -=1
            choose_product.save()
            
            #Nếu sản phẩm nhỏ hơn hoặc bằng 0 thì xóa nó khỏi giỏ hàng
            if choose_product.quantity <=0 :
                choose_product.delete()
    return redirect('cart')


def cart(request):
    if(request.user.is_authenticated):
        order = Order.objects.get(customer = request.user)
        orderItem = OrderItem.objects.filter(order = order)
        # print("user_CART: ", request.user,'; orderitem: ', orderItem)
        context = {'products': orderItem, 'total_price': order.get_total_price} 
        return render(request, "app/cart.html",context) 
    return redirect('login')
    

def checkout(request):
    return render(request, "app/checkout.html")



#Create product
def create_product(request):
    product = Product.objects.all()

    if request.method == 'POST':
        form = CreateProduct(request.POST, request.FILES)
        context = {'form': form, 'products': product}

        print(">>>>>>>>>> requesst CREATE_PRODUCT >>>>>>>: ", form)
        if form.is_valid():
            print(">>>>>>>>>> POST IS_VALID CREATE_PRODUCT >>>>>>>: ", request.POST, '; ' ,request.FILES)
            form.save() 

            return redirect('create_product') 
        else:
            print('Không VALID CREATE_PRODUCT thông tin người dùng')
    else:
        form = CreateProduct()
        context = {'form': form, 'products': product}
    return render(request, "app/create_product.html", context)



def edit_product(request):
    if(request.method =="POST"):
        render 
    


def delete_product(request):
    if(request.method == "POST"):
        product_id = request.POST['id']
        
        product_del = Product.objects.filter(id = product_id)
        product_del.delete()
    return  redirect('create_product')