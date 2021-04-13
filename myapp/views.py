from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import  datetime
from django.core.paginator import Paginator
import random

########## line notify ################
from songline import Sendline
token ='ktYscgsHtdAt46d42uOfavUNAAlnJPx8MgZFx8rhBzv'
messenger = Sendline(token)
#######################################

def GenerateToken(domain='http://127.0.0.1:8000/confirm/'):
	allchar = [chr(i) for i in range(65,91)]
	allchar.extend([chr(i) for i in range(97,123)])
	allchar.extend([str(i) for i in range(10)])
	emailtoken = ''
	for i in range(40):
		emailtoken += random.choice(allchar)

	url = domain + emailtoken
	#print(url)
	return (url,emailtoken) #ส่งออก 2 ค่า

def Confirm(request,token):
	try:
		check = VerifyEmail.objects.get(token=token)
		status = 'found'
		check.approved = True
		check.save()
		context = {'status': statust,'email':check.user.username, 'name': check.user.first_name}
	except:
		status = 'notfound'
		context = {'status':status}

	return render(request, 'myapp/confirm.html',context)


##############Email#########################
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendthai(sendto,subj="ทดสอบส่งเมลลล์",detail="สวัสดี!\nคุณสบายดีไหม?\n"):

	myemail = 'aoftest.django50@gmail.com'
	mypassword = 'Cleoja027'
	receiver = sendto

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subj
	msg['From'] = 'Admin EAFOREXQUANT'
	msg['To'] = receiver
	text = detail

	part1 = MIMEText(text, 'plain')
	msg.attach(part1)

	s = smtplib.SMTP('smtp.gmail.com:587')
	s.ehlo()
	s.starttls()

	s.login(myemail, mypassword)
	s.sendmail(myemail, receiver.split(','), msg.as_string())
	s.quit()


###########Start sending#############
def EmailConfirm(email,name,token):
	subject = 'ยืนยันการสมัครเวปไซต์ซื้อ EA ของ EAFOREXQUANT'
	newmember_name = name
	content = 'เนื่องจากทางด้านความปลอดภัย กรุณายืนยันผ่านลิ้งด้านล่างนี้'
	link = token

	msg = 'สวัสดีครับ {} \n\n {} \n verify link: {}'.format(newmember_name,content,link)
	sendthai(email,subject,msg)

# sendthai('aofwittawat@gmail.com,wittawatb@g.swu.ac.th',subject,msg)
######################################



######################################

def Home(request):
	product = Allproduct.objects.all().order_by('id').reverse()[:3] # ดึงข้อมูลมาทั้งหมด แล้วเอาใหม่ขึ้นก่อนด้วย ดึง 3 items ล่าสุด
	preoder = Allproduct.objects.filter(quantity__lte=0) # quantity__lte (หาค่าที่ <=0)
	context = {'product': product,'preoder': preoder}
	return render(request, 'myapp/home.html', context)

def About(request):
	return render(request, 'myapp/about.html')

def Contact(request):
	return render(request, 'myapp/contact.html')

def Quant(request):
	return render(request, 'myapp/Gold SuperTrend Quant.html')

from django.core.files.storage import FileSystemStorage

def Addproduct(request):

	if request.user.profile.usertype != 'admin':
		return redirect('home-page')



	if request.method == 'POST' and request.FILES['imageupload']:
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')
		quantity = data.get('quantity')
		unit = data.get('unit')

		new = Allproduct()
		new.name =name
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.quantity = quantity
		new.unit = unit
		#############################save image#################
		file_image = request.FILES['imageupload']
		file_image_name = request.FILES['imageupload'].name.replace(' ','')
		print('FILE_IMAGE:' ,file_image)
		print('IMAGE_NAME:',file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name,file_image)
		upload_file_url = fs.url(filename)
		new.image = upload_file_url[6:]
		########################################################
		new.save()

	return render(request, 'myapp/addproduct.html')



def Product(request):
	product = Allproduct.objects.all().order_by('id').reverse() # ดึงข้อมูลมาทั้งหมด แล้วเอาใหม่ขึ้นก่อนด้วย
	paginator = Paginator(product,2) # 1 หน้าแสดงแค่ 3 ชิ้นเท่านั้น product คือข้อมูลที่เรา get มาทั้งหมด
	page = request.GET.get('page') # เป็นการ get page เข้ามา ##http://127.0.0.1:8000/allproduct/?page=2##
	product = paginator.get_page(page)
	context = {'product': product}
	return render(request, 'myapp/allproduct.html', context)


def Register(request):
	if request.method == 'POST':
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')

		newuser = User()
		newuser.username= email
		newuser.first_name=first_name
		newuser.last_name=last_name
		newuser.set_password(password)
		newuser.save()

		profile = Profile()
		profile.user = User.objects.get(username=email)
		profile.save()
################# send mail for verification ###########

		#sendthai(email,subject,msg)
		token,token_code = GenerateToken()
		EmailConfirm(email,first_name,token)
		getuser = User.objects.get(username=email)
		addverify = VerifyEmail()
		addverify.user = getuser
		addverify.token = token_code
		addverify.save()

########################################################

		#from django.contrib.auth import authenticate, login
		user = authenticate(username=email, password=password)
		login(request,user)

	return render(request, 'myapp/register.html')

def AddtoCart(request, pid):
	# การเรียก rquest ตาม id
	username = request.user.username
	user = User.objects.get(username=username)
	check = Allproduct.objects.get(id=pid)

	try:
		# กรณีที่ตัวสินค้ามีซ้ำ
		newcart = Cart.objects.get(user=user,productid=str(pid))
		newquan = newcart.quantity + 1
		newcart.quantity = newquan
		calculate = newcart.price * newquan
		newcart.total = calculate
		newcart.save()

		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

		return redirect('allproduct-page')
	except: # ถ้าไม่ซ้ำก็ update new cart in model
		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price = int(check.price)
		newcart.quantity = 1
		calculate = int(check.price) * 1
		newcart.total = calculate
		newcart.save()
#################### update ใน badge ######################
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
############################################################
		return redirect('allproduct-page')


def MyCart(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}
	if request.method == 'POST':
		#ใช้สำหรับการลบเท่านั้น
		data = request.POST.copy()
		productid = data.get('productid')
		item = Cart.objects.get(user=user,productid=productid)
		item.delete()
		context['status'] = 'delete'
#################### update ใน badge ######################
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
############################################################
	mycart = Cart.objects.filter(user=user)
	count = sum([c.quantity for c in mycart])
	total = sum([c.total for c in mycart])
	context['mycart'] =  mycart
	context['count'] =  count
	context['total'] =  total
	return render(request, 'myapp/mycart.html', context)


def MyCartEdit(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}
	if request.method == 'POST':
		data = request.POST.copy()
		#print(data)
		if data.get('clear') == 'clear':
			Cart.objects.filter(user=user).delete()
			count = Cart.objects.filter(user=user)
			# หลังจากลบแล้ว update จำนวนที่ mycart
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()

			return redirect('mycart-page')

		editlist=[]
		for k,v in data.items():
			#print([k,v])
			# ค่าที่ได้จะเป็น pd_XX
			if k[:2] == 'pd':
				pid = int(k.split('_')[1])
				dt =[pid,int(v)]
				editlist.append(dt)
				# editlist จะได้ [[9,10],[7,8]] = เป็น list ซ้อน list
		for ed in editlist:
			edit = Cart.objects.get(productid=ed[0], user=user)
			edit.quantity = ed[1] 
			calculate = edit.price * ed[1]
			edit.total = calculate
			edit.save()
 
 #################### update ใน badge ######################
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()

############################################################
		return redirect('mycart-page')

	mycart = Cart.objects.filter(user=user)
	context['mycart'] =  mycart
	return render(request, 'myapp/mycartedit.html', context)


def Checkout(request):
	username = request.user.username
	user = User.objects.get(username=username)
	# generate oder number to save in Order Models 
	# save productin cart to OrderProduct Models
	# clear cart 
	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		tel = data.get('tel')
		address = data.get('address')
		shipping = data.get('shipping')
		payment = data.get('payment')
		other = data.get('other')
		page = data.get('page')
		if page == 'information':
			context = {}
			context['name'] = name
			context['tel'] = tel
			context['address'] = address
			context['shipping'] = shipping
			context['payment'] = payment
			context['other'] = other

			mycart = Cart.objects.filter(user=user)
			count = sum([c.quantity for c in mycart])
			total = sum([c.total for c in mycart])
			
			context['mycart'] =  mycart
			context['count'] =  count
			context['total'] =  total
			return render(request, 'myapp/checkout2.html',context)
		if page == 'confirm':
			print ('confirm')
			print(data)

			mycart = Cart.objects.filter(user=user)

			# orderid จะใช้เวลาแทน เพื่อให้มัน generate ค่าให้เอง เช่น
			# id = OD 0007 20200903220030
			# ใช้วิธี Zero-pad หาได้ใน stackoverflow
			mid = str(user.id).zfill(4)
			dt = datetime.now().strftime('%Y%m%d%H%M%S')
			orderid = 'OD' + mid +dt
			
			productorder = ''
			producttotal = 0
			
			for pd in mycart: #ไม่สามารถ save ตรงๆ ได้เนื่องจากค่าที่จะเป็น list ยาวๆ ต้อง for loop แตกออกมาก่อน
				order = OrderList()
				order.orderid = orderid
				order.productid = pd.productid
				order.productname = pd.productname
				order.price = pd.price
				order.quantity = pd.quantity
				order.total = pd.total
				order.save()
				productorder = productorder +' {}\n'.format(pd.productname) #รายการสินค้า
				producttotal += pd.total

			texttoline = 'ODID: {}\n-------\n{}ยอดรวม: {:,.2f} บาท\n ({})'.format(orderid,productorder,producttotal,name)
			
			if producttotal > 10000:
				messenger.sticker(14,1,texttoline)
			else:
				messenger.sendtext(texttoline)

			odp = OrderPending()
			odp.orderid = orderid
			odp.user = user
			odp.name = name
			odp.tel = tel
			odp.address = address
			odp.shipping = shipping
			odp.payment = payment
			odp.other = other
			odp.save()
			# พอ save แล้วต้อง clear mycart = 0
			Cart.objects.filter(user=user).delete()
			count = Cart.objects.filter(user=user)
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')	
			# redirect to order list page

	return render(request, 'myapp/checkout1.html')


def OrderListPage(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}

	order = OrderPending.objects.filter(user=user) 

	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		total = sum([c.total for c in odlist])# sum จำนวนที่เป็น order มาจาก id เดียวกัน
		od.total = total #เพิ่มค่าเข้าใน class ชั่วคราว ใน class orderpending ไม่มี total
		# สั่งนับจำนวน order
		
		count = sum([c.quantity for c in odlist])
		if od.shipping == 'ems':
			shipcost = sum([50 if i == 0 else 10 for i in range(count)])
		else:
			shipcost = sum([30 if i == 0 else 10 for i in range(count)])
		#ถ้าเก็บเงินปลายทางอาจต้องบวกอีก 20 บาท
		if od.payment == 'cod':
			shipcost += 20 # shipcost = shipcost + 20
		od.shipcost = shipcost #เพิ่มค่าเข้าใน class ชั่วคราว ใน class orderpending ไม่มี shipcost

	context['allorder'] = order

	return render(request, 'myapp/orderlist.html',context)




def AllOrderListPage(request):
	context = {}
	order = OrderPending.objects.all()

	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		total = sum([c.total for c in odlist])
		od.total = total
		count = sum([c.quantity for c in odlist])
		if od.shipping == 'ems':
			shipcost = sum([50 if i == 0 else 10 for i in range(count)])
		else:
			shipcost = sum([30 if i == 0 else 10 for i in range(count)])
		#ถ้าเก็บเงินปลายทางอาจต้องบวกอีก 20 บาท
		if od.payment == 'cod':
			shipcost += 20 # shipcost = shipcost + 20
		od.shipcost = shipcost #เพิ่มค่าเข้าใน class ชั่วคราว ใน class orderpending ไม่มี shipcost

	paginator = Paginator(order,2) # 1 หน้าแสดงแค่ 3 ชิ้นเท่านั้น product คือข้อมูลที่เรา get มาทั้งหมด
	page = request.GET.get('page') # เป็นการ get page เข้ามา ##http://127.0.0.1:8000/allproduct/?page=2##
	order = paginator.get_page(page)
	
	context['allorder'] = order
	return render(request, 'myapp/allorderlist.html',context)

	


def UploadSlip(request,orderid):
	#print('ORDER ID: ', orderid)
	if request.method == 'POST' and request.FILES['slip']:
			data = request.POST.copy()
			sliptime = data.get('sliptime')
			
			update = OrderPending.objects.get(orderid=orderid)
			update.sliptime = sliptime
			
	#############################save image#################
			file_image = request.FILES['slip']
			file_image_name = request.FILES['slip'].name.replace(' ','')
			print('FILE_IMAGE:' ,file_image)
			print('IMAGE_NAME:',file_image_name)
			fs = FileSystemStorage()
			filename = fs.save(file_image_name,file_image)
			upload_file_url = fs.url(filename)
			update.slip = upload_file_url[6:]
	########################################################
			update.save()

	odlist = OrderList.objects.filter(orderid=orderid)
	total = sum([c.total for c in odlist])
	oddetail = OrderPending.objects.get(orderid=orderid) # จะได้รู้ว่า เป็น EMS หรือ ลงทะเบียน
	# คำนวนค่าส่งการประเภทการส่ง จาก models: shipping
	count = sum([c.quantity for c in odlist])
	if oddetail.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
	else:
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	#ถ้าเก็บเงินปลายทางอาจต้องบวกอีก 20 บาท
	if oddetail.payment == 'cod':
		shipcost += 20 # shipcost = shipcost + 20

	context = {	'orderid':orderid, 
				'total':total,
				'shipcost':shipcost, 
				'grandtotal': total+shipcost,
				'count':count,
				'oddetail': oddetail}

	return render(request, 'myapp/uploadslip.html', context)


def UpdatePaid(request,orderid,status):
	
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
	
	order = OrderPending.objects.get(orderid=orderid) #ได้ piad status ของ id นั้นๆมาแล้ว
	if status == 'confirm':
		order.paid = True
	elif status == 'cancel':
		order.paid = False
	order.save()

	return redirect('allorderlist-page')



def UpdateTracking(request,orderid):
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')

	if request.method == 'POST':
		order = OrderPending.objects.get(orderid=orderid)
		data = request.POST.copy()
		trackingnumber = data.get('trackingnumber')
		order.trackingnumber = trackingnumber
		#print(trackingnumber)
		order.save()
		return redirect('allorderlist-page')

	order = OrderPending.objects.get(orderid=orderid)
	#จะได้ order 1 order ที่มาจาก orderid นี้
	odlist = OrderList.objects.filter(orderid=orderid) 
	# 1 orderlist อาจมีหลายสินค้าที่สั่งมาทีเดียวกัน เลยต้องใช้ filter
	### shipcost
	total = sum([c.total for c in odlist])
	order.total = total
	count = sum([c.quantity for c in odlist])
	if order.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
	else:
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	#ถ้าเก็บเงินปลายทางอาจต้องบวกอีก 20 บาท
	if order.payment == 'cod':
		shipcost += 20 # shipcost = shipcost + 20
	order.shipcost = shipcost #เพิ่มค่าเข้าใน class ชั่วคราว ใน class orderpending ไม่มี shipcost
	context = {'order':order,'odlist':odlist, 'total':total,'count':count}
	context['orderid'] = orderid
	
	return render(request, 'myapp/updatetracking.html', context)

def Myorder(request, orderid):
	username = request.user.username# เป็นการเช็ค username ว่าคนนี้เป็น user หรือไม่
	user = User.objects.get(username=username)
	
	order = OrderPending.objects.get(orderid=orderid)
	#จะได้ order 1 order ที่มาจาก orderid นี้
	# เช็คว่าเป็นของตัวเองไหม
	if user != order.user:
		return redirect('allproduct-page')

	odlist = OrderList.objects.filter(orderid=orderid) 
	# 1 orderlist อาจมีหลายสินค้าที่สั่งมาทีเดียวกัน เลยต้องใช้ filter
	### shipcost
	total = sum([c.total for c in odlist])
	order.total = total
	count = sum([c.quantity for c in odlist])
	if order.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
	else:
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])
	#ถ้าเก็บเงินปลายทางอาจต้องบวกอีก 20 บาท
	if order.payment == 'cod':
		shipcost += 20 # shipcost = shipcost + 20
	order.shipcost = shipcost #เพิ่มค่าเข้าใน class ชั่วคราว ใน class orderpending ไม่มี shipcost
	context = {'order':order,'odlist':odlist, 'total':total,'count':count}


	return render(request, 'myapp/myorder.html', context)
	