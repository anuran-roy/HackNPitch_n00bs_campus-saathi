# import torch
# from torch import nn
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk import PorterStemmer
# from nltk import WordNetLemmatizer
# from nltk.corpus import stopwords
# from sklearn.feature_extraction.text import CountVectorizer

import requests
import json

############# PyTorch Spam Filter Implementation #############

# class LogisticRegression(nn.Module):
#     def __init__(self):
#         super(LogisticRegression, self).__init__()
#         self.linear1 = nn.Linear(10000, 100)
#         self.linear2 = nn.Linear(100, 10)
#         self.linear3 = nn.Linear(10, 2)

#     def forward(self, x):
#         x = F.relu(self.linear1(x))
#         x = F.relu(self.linear2(x))
#         x = self.linear3(x)
#         return x


# def getResponse(text):
#     model = LogisticRegression()
#     model.load_state_dict(torch.load("spam_filter.pth"))
#     model.eval()

#     max_words = 10000
#     cv = CountVectorizer(max_features=max_words, stop_words='english')
#     sparse_matrix = cv.fit_transform(data['email']).toarray()

#     return model

############# End Implementation #############

############# Oopspam API Implementation #############

def oopspam(text, ip):
    pass
    url = "https://oopspam.p.rapidapi.com/v1/spamdetection"

    payload = '{\n    \"checkForLength\": true,\n    \"content\": \{text}\",\n    \"senderIP\": \"185.234.219.246\"\n}'
    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "oopspam.p.rapidapi.com",
        'x-rapidapi-key': "08f9acebcamshe0023f4887789f9p1656fejsnada539d5937e"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

############# End Oopspam API Implementation #############

############# Plino API Implementation #############

def plino(text):
    api_url = "https://plino.herokuapp.com/api/v1/classify/"
    payload = {
    'email_text': text
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        a = response.json()
        if __name__ == '__main__':
            print(type(a), end="\n\n\n")
            print(a)
        return a["email_class"] == "spam"
    else: return False

if __name__ == "__main__":
    m = input("Enter a message:")
    plino(m)

############# End Plino API Implementation #############
