from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,DetailView
from .import models
from symptom_checker.diagnosis import load_symptoms
from symptom_checker.forms import Form,SearchForm
from django.template.defaulttags import register
#----------------------------------------------------------------------------------------------------------------------------------------------------------
ob=load_symptoms() # ob is the object of the load_symptoms class imported from Diagnosis file.
user_name='' #user_name stores the user name taken in the index page
gender='' #gender stores the gender
yob='' #yob stores the year of birthYear
# gender and yob are required to be given as parameters to one of
#the API requests while username is taken to increase user interest and interactivity.

#--------------------------------------------------------------------------------------------------------------------------------------------------------
# <summary>
# template filter to get the dictionary value corresponding to a key
# </summary>
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# <summary>
# A Django template view that defines the view of the index page(first page)
# </summary>
class IndexView(TemplateView):
    
    template_name='symptom_checker/index.html'

    def get(self,request):
        form=Form()
        models.Details.objects.all().delete()
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=Form(request.POST)
        if form.is_valid(): #if the form is valid
            global user_name
            user_name=form.cleaned_data['name'] #retrieving the name entry
            global yob
            yob=form.cleaned_data['birthYear']#retrieving the birthYear entry
            global gender
            gender=form.cleaned_data['gender']#retrieving the gender entry
            models.Details.objects.get_or_create(name=user_name.lower(),yearofbirth=yob,gender=gender)[0]
            return redirect('symptom_checker:list') # after validating the form and populating the fields in the Details
                                                    # table redirect me to the Symptom ListView page.
        args={'form':form,'name':user_name}
        return render(request,self.template_name,args)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
# <summary>
#This is the helper method that generates a list of all the issue objects related
#to the clicked symptom and maps each issue_id with a list of related specialisationsself.
#It attaches the data strutures to a dictionary context as values which will be later injected
#into the html.
# </summary>

def perform_task(symptom):
    issues_ids=symptom.issues_id.split(',')
    issues_ids=[int(x) for x in issues_ids] #issues_ids is a list of all issues ids corresponding to the given symptom.
    maps={} #issue id and related list of specialisation names mapping.
    issues=list()
    for i in issues_ids:
        issue=models.Issues.objects.get(issue_id=i)
        issues.append(issue)
        sp=issue.specializations.split(',')
        spz=list() #spz is used to contain specialization names related to an issue.
        for i in sp:
            specialization=models.Specialization.objects.get(s_id=int(i))
            spz.append(specialization.name)
        maps[issue.issue_id]=spz
    context={}
    context['map']=maps
    context['issues']=issues
    return context
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
# <summary>
#A Django class based view to display the detail corresponding to the selected symtom from the listView.
# </summary>
class SymptomDetailView(DetailView):

    context_object_name='symptom_detail'
    template_name='symptom_checker/symptom_detail.html'

    # <summary>
    #overriding the get_context_data method to inject the content into HTML.
    # </summary>
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        object_clicked=super().get_object()
        name_id=object_clicked.name_id
        x=models.Details.objects.all()
        ob.get_issue_and_specialists(yob,gender,name_id)
        symptom=models.Symptoms.objects.get(name_id=name_id)
        context=perform_task(symptom)
        return context

    def get_queryset(self):
        return models.Symptoms.objects.all()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
# <summary>
# A Django class based view to list all the symptoms recieved through a request from the API and each list item is clickable.
# </summary>
class SymptomsListview(ListView):

    context_object_name='symptoms'
    model=models.Symptoms
    template_name='symptom_checker/symptoms_list.html'

    def get(self,request):
        global ob
        ob.load()
        form=SearchForm()
        symptoms=models.Symptoms.objects.all()
        details=models.Details.objects.all()
        return render(request,self.template_name,{'symptoms':symptoms,'form':form,'user_name':user_name})

    # <summary>
    #This method is executed when the user presses the search button on the DetailView page.
    #Each symptom is converted to lower case and matched word by word with the searched text and
    #the symptom that contains maximum number of matched words will have its detail displayed on
    #DetailView page.
    # </summary>
    def post(self,request):
        global ob #ob is an object of load_symptoms class imported from Diagnosis module.
        ob.load() #this method  is used fetch the symptoms from the API.
        symptoms=models.Symptoms.objects.all()
        form=SearchForm(request.POST)
        if form.is_valid():
            search_text=form.cleaned_data['text']
            search_text=search_text.replace(" ","").lower()
            sym=models.Symptoms.objects.all()
            max=0 #max is used to store maximum number of word matches per symptom.
            sym_max="" #sym_max is used to store the symptom that has its maximum words in the searched text.
            for symptom in sym:
                count=0;
                sym_list=symptom.name.split(' ')# sym_list is used to store all the words in a symptom name
                for x in sym_list:
                    if x.lower() in search_text:
                        count+=1
                if count>max:
                    max=count
                    sym_max=symptom
            if sym_max != "":
                x=models.Details.objects.all()
                ob.get_issue_and_specialists(yob,gender,sym_max.name_id)
                symptom=models.Symptoms.objects.get(name_id=sym_max.name_id)
                context=perform_task(symptom)
                context['user_name']=user_name
                return render(request,'symptom_checker/symptom_detail.html',context) #render me to the symptom_detail(DetailView) page.
        args={'form':form,'symptoms':symptoms,'user_name':user_name}
        return render(request,self.template_name,args)
