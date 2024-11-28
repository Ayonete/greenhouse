from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Crop
from .forms import EditCropForm, DiagnosticsForm
from .crophealthlib import CropHealth, CareAdvice, NutrientDeficiencyDetector, rules
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from .utils import add_item_to_dynamodb, CropHealth, PlantDiagnosis
from decimal import Decimal
import boto3
import json



# this is a view for listing all the crops
def home(request):
    crops = Crop.objects.all()
    context = {'crops': crops}
    return render(request, 'crops/home.html', context)

# this is a view for listing a single crop,it will take id as an argument
def crop_detail(request, id):
    crop = Crop.objects.get(pk=id)
    context = {'crop': crop}
    return render(request, 'crops/crop-detail.html', context)

# this is a list for adding a crop
# def add_crop(request):
#     if request.method == 'POST':
#         data = request.POST
#         image = request.FILES.get('image-file')
        
#         crop = Crop.objects.create(
#             name = data['name'],
#             #planted_on = data['planted_on'],
#             description = data['description'],
#             temperature = data['temperature'],
#             moisture = data['moisture'],
#             image = image
            
#             )

def add_crop(request):
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image-file')
        
        # Data validation and conversion 
        name = data.get('name')
        description = data.get('description')
        moisture = data.get('moisture')    
        temperature = data.get('temperature')
        
        # Create Crop instance
        crop = Crop.objects.create(
            name=name,
            description=description,
            temperature=temperature,
            moisture=moisture,
            image=image
        )
        
        # # Add the data to DynamoDB
        # add_item_to_dynamodb(name, description, moisture, temperature)
        
        # moisture = Decimal(data.get('moisture', '0'))
        # temperature = Decimal(data.get('temperature', '0'))

        # # Analyze crop health
        # crop_health = CropHealth(moisture, temperature)
        # health_status = crop_health.analyse_health()

        # # Send an email notification with health status
        # TopicArn='arn:aws:sns:eu-west-1:250738637992:23119233-GREENHOUSE'
        
        # CropHealth.publish_to_sns(TopicArn,'Crop Health Status', health_status)
        # return redirect('home')

    return render(request, 'crops/add-crop.html')


def send_message_to_sqs(name, health_status):
    # Initialize SQS client
    sqs_client = boto3.client('sqs')
    queue_url = 'https://sqs.eu-west-1.amazonaws.com/250738637992/23119233-queue'  

    # Construct message
    message = {
        'CropName': name,
        'HealthStatus': health_status
    }

    # Send message to SQS queue
    sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))


def edit_crop(request, id):
    crop = Crop.objects.get(pk=id)
    
    form = EditCropForm(instance=crop)
    
    if request.method == 'POST':
        form = EditCropForm(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('home')
            
    context = {'form': form}
    return render(request, 'crops/update-crop.html', context)


# this is a view for deleting a crop
def delete_crop(request, id):
    # getting the book to be deleted
    crop = Crop.objects.get(pk=id)
    # checking if the method is POST
    if request.method == 'POST':
        # delete the book
        crop.delete()
        # return to home after a success delete
        return redirect('home')
    context = {'crop': crop}
    return render(request, 'crops/delete-crop.html', context)


def diagnostics(request):
    if request.method == 'POST':
        form = DiagnosticsForm(request.POST)
        if form.is_valid():
            #form.save()
            return HttpResponse('nothing for now, check back later')
    else:
        form = DiagnosticsForm()
    return render(request, 'crops/diagnostics.html', {'form': form})