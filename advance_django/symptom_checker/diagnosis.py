import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'advance_django.settings')
import django
django.setup()
import requests
import hmac, hashlib
import base64
import json
from symptom_checker.models import Symptoms,Issues,Specialization
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# <summary>
# A class that contains methods for requesting services from the api
# </summary>
class Diagnosis:
    # <summary>
    # DiagnosisClient constructor
    # </summary>
    # <param name="username">api user username</param>
    # <param name="password">api user password</param>
    # <param name="authServiceUrl">priaid login url (https://sandbox-authservice.priaid.ch/login)</param>
    # <param name="language">language</param>
    # <param name="healthServiceUrl">priaid healthservice url(https://sandbox-healthservice.priaid.ch)</param>
    def __init__(self, username, password, authServiceUrl, language, healthServiceUrl):
        self._handleRequiredArguments(username, password, authServiceUrl, healthServiceUrl, language)
        self._language = language
        self._healthServiceUrl = healthServiceUrl
        self._token = self._loadToken(username, password, authServiceUrl)


    def _loadToken(self, username, password, url):
        rawHashString = hmac.new(bytes(password, encoding='utf-8'), url.encode('utf-8')).digest()
        computedHashString = base64.b64encode(rawHashString).decode()
        bearer_credentials = username + ':' + computedHashString
        postHeaders = {
                'Authorization': 'Bearer {}'.format(bearer_credentials)
        }
        responsePost = requests.post(url, headers=postHeaders)
        data=json.loads(responsePost.text)
        return data

    def _loadFromWebService(self, action):
        extraArgs = "token=" + self._token["Token"] + "&language=" + self._language
        if "?" not in action:
            action += "?" + extraArgs
        else:
            action += "&" + extraArgs

        url=self._healthServiceUrl+"/"+action
        response = requests.get(url)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print ("----------------------------------")
            print ("HTTPError: " + e.response.text )
            print ("----------------------------------")
            raise

        try:
            dataJson = response.json()
        except ValueError:
            raise requests.exceptions.RequestException(response=response)

        data = json.loads(response.text)
        return data

    # <summary>
    # Load all symptoms
    # </summary>
    # <returns>Returns list of all symptoms</returns>
    def loadSymptoms(self):
        return self._loadFromWebService("symptoms")

    def _handleRequiredArguments(self, username, password, authUrl, healthUrl, language):
        if not username:
            raise ValueError("Argument missing: username")

        if not password:
            raise ValueError("Argument missing: username")

        if not authUrl:
            raise ValueError("Argument missing: authServiceUrl")

        if not healthUrl:
            raise ValueError("Argument missing: healthServiceUrl")

        if not language:
            raise ValueError("Argument missing: language")

    # <summary>
    # Load all diagnosis details related to list of selected symptoms or a given symptom
    # </summary>
    # <returns>This endpoint returns an array of the generated health diagnosis. Each element consists of the relative accuracy ..
    #..(in %) and issue (ID, Name, ProfName, Icd and IcdName).
    #</returns>
    def loadDiagnosis(self, selectedSymptoms, gender, yearOfBirth):
        if not selectedSymptoms:
            raise ValueError("selectedSymptoms can not be empty")

        serializedSymptoms = json.dumps(selectedSymptoms)
        action = "diagnosis?symptoms={0}&gender={1}&year_of_birth={2}".format(serializedSymptoms, gender,
                                                                              yearOfBirth)
        return self._loadFromWebService(action)

    # <summary>
    # Issue info can be called to receive all information about a health issue.
    # The short description gives a short overview.
    # A longer information can consist of "Description", "MedicalCondition", "TreatmentDescription"
    # </summary>
    def loadIssueInfo(self, issueId):
        if isinstance( issueId, int ):
            issueId = str(issueId)
        action = "issues/{0}/info".format(issueId)
        return self._loadFromWebService(action)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# <summary>
# A class that contain core methods for manipulating and storing data in the database
# </summary>
class load_symptoms:

    # <summary>
    # Constructor to create the object of the Diagnosis class and generate the  token for the Authorization purpose
    # </summary>
    def __init__(self):
        self.ob = Diagnosis("srivastava2511@gmail.com","Do76BnSf5g3KMa28N","https://sandbox-authservice.priaid.ch/login","en-gb","https://sandbox-healthservice.priaid.ch")

    # <summary>
    # Method that loops over the a list of dictionaries each containing symptom id
    # and symptom name as keys and their corresponding values.
    # </summary>
    def save_symptoms(self,sym_data):
        for x in sym_data:
            Symptoms.objects.get_or_create(name_id=x['ID'],name=x['Name'])[0]

    # <summary>
    # Helper method to save the diagnosis details in the corresponding tables.
    # </summary>
    def save_data(self,diag_data,clicked_symptom_id):
        iids=list()
        for item in diag_data:
            issue_id=item['Issue']['ID']
            iids.append(str(issue_id))
            issue_name=item['Issue']['Name']
            specializations=item['Specialisation']
            sids=list()
            for x in specializations:
                id=x['ID']
                name=x['Name']
                Specialization.objects.get_or_create(s_id=id,name=name)[0]
                sids.append(str(id))
            sp=','.join(sids)
            Issues.objects.get_or_create(issue_id=issue_id,name=issue_name,specializations=sp)[0]
        x=Symptoms.objects.get(name_id=clicked_symptom_id)
        ids=','.join(iids)
        x.issues_id=ids
        x.save()

    # <summary>
    # Helper method to save the issue information to a given row in the Issues table
    # </summary>
    def issue_save_data(self,issue_data,issue_id):
        x=Issues.objects.get(issue_id=issue_id)
        x.short_description=issue_data['DescriptionShort']
        x.treatement_description=issue_data['TreatmentDescription']
        x.related_symptoms=issue_data['PossibleSymptoms']
        x.medical_condition=issue_data['MedicalCondition']
        x.save()

    # methods that requests the API to return the list of all the symptoms
    def load(self):
        sym_data=self.ob.loadSymptoms()
        self.save_symptoms(sym_data)

    # <summary>
    # The main purpose of this method is to the populate the
    # issues_id column of the Symptoms table and populate Issues and Specialization table.
    # </summary>
    def get_issue_and_specialists(self,yob,gender,clicked_symptom_id):
        # x contains the symptom that was clicked in the apps ListView page
        x=Symptoms.objects.get(name_id=clicked_symptom_id)
        if x.issues_id=='':
            s_id_list=[clicked_symptom_id]
            diag_data=self.ob.loadDiagnosis(s_id_list,gender,yob)
            self.save_data(diag_data,clicked_symptom_id)
            symptom=Symptoms.objects.get(name_id=clicked_symptom_id)
            issues_ids=symptom.issues_id.split(',')
            issues_ids=[int(x) for x in issues_ids]
            for i in issues_ids:
                issue_info_data=self.ob.loadIssueInfo(i)
                self.issue_save_data(issue_info_data,i)
