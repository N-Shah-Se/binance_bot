from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
import razorpay
from django.http import JsonResponse

# Create your views here.
@api_view(['POST'])
def createOrder(request):
    global client
    data = request.data
    
    amount = int(float(data['amount'])) * 100
    try:
        client = razorpay.Client(auth=(data['key_id'], data['key_secret']))
        request.session['client'] = client
        data = {"amount" : amount, "currency" : "INR"}
        payment = client.order.create(data=data)
    except Exception as ex:
        return JsonResponse({'status':False,"massage":f"{ex}"})
    
    data = {'order_id': payment['id'], 'amount': payment['amount'], 'currency':payment['currency']}
    return JsonResponse({"status":True,"data":data})

@api_view(['POST'])
def verifySignature(request):
    res = request.data

    params_dict = {
        'razorpay_payment_id' : res['razorpay_payment_id'],
        'razorpay_order_id' : res['razorpay_order_id'],
        'razorpay_signature' : res['razorpay_signature']
    }
    client = request.session.get('client')
    # verifying the signature
    try:
        res = client.utility.verify_payment_signature(params_dict)
    except Exception as ex:
        return JsonResponse({'status':False,"massage":f"{ex}"})    
    if res == True:
        
        return JsonResponse({'status':True,"massage":"Payment Successfull"})
    return JsonResponse({'status':True,"massage":'Payment Failed'})